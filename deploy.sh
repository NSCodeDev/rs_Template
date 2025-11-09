#!/bin/bash

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_debug() { echo -e "${BLUE}[DEBUG]${NC} $1"; }

# Parse arguments
VM_HOST=""
VM_USER=""
SSH_KEY_PATH=""
DEPLOY_PATH=""
ENV_FILE=""
VERSION=""
ENVIRONMENT=""


while [[ $# -gt 0 ]]; do
    case $1 in
        --vm-host)
            VM_HOST="$2"
            shift 2
            ;;
        --vm-user)
            VM_USER="$2"
            shift 2
            ;;
        --ssh-key-path)
            SSH_KEY_PATH="$2"
            shift 2
            ;;
        --deploy-path)
            DEPLOY_PATH="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validation of arguments
if [[ -z "$VM_HOST" || -z "$VM_USER" || -z "$SSH_KEY_PATH" || -z "$DEPLOY_PATH" || -z "$VERSION" ]]; then
    log_error "All arguments --vm-host, --vm-user, --ssh-key, --deploy-path, and --version are required."
    exit 1
fi

# SSH connection function with error handling
ssh_connect() {
    if ! ssh -o StrictHostKeyChecking=no \
        -o ConnectTimeout=10 \
        -o BatchMode=yes \
        -i "$SSH_KEY_PATH" \
        "$VM_USER@$VM_HOST" \
        "$@"; then
        log_error "SSH connection failed to $VM_USER@$VM_HOST"
        return 1
    fi
}

# Test SSH connection before deployment
test_ssh_connection() {
    log_info "Testing SSH connection to $VM_USER@$VM_HOST..."
    
    if ssh -o StrictHostKeyChecking=no \
        -o ConnectTimeout=10 \
        -o BatchMode=yes \
        -i "$SSH_KEY_PATH" \
        "$VM_USER@$VM_HOST" \
        "echo 'SSH connection successful'" > /dev/null 2>&1; then
        log_info "SSH connection test passed"
        return 0
    else
        log_error "SSH connection test failed"
        log_error "Please check:"
        log_error "  - VM is running and accessible"
        log_error "  - SSH key is correct and has proper permissions (chmod 600)"
        log_error "  - User '$VM_USER' exists on the remote host"
        log_error "  - Host '$VM_HOST' is reachable"
        return 1
    fi
}

# Check if docker-compose command was successful
check_docker_compose_status() {
    local release_path=$1
    local max_attempts=3
    local attempt=1
    
    log_info "Checking Docker Compose deployment status..."
    
    # Define services that should keep running (exclude one-time jobs)
    local expected_services=("kong" "kong-database" "konga")
    local expected_count=${#expected_services[@]}
    
    while [ $attempt -le $max_attempts ]; do
        log_debug "Attempt $attempt/$max_attempts - Checking container status..."
        
        local status=$(ssh_connect "cd $release_path && docker compose ps --format json 2>/dev/null" || echo "")
        
        if [ -z "$status" ]; then
            log_warning "Unable to get container status. Retrying..."
            sleep 5
            ((attempt++))
            continue
        fi
        
        local container_info=$(ssh_connect "cd $release_path && docker compose ps")
        echo "$container_info"
        
        # Count running containers (excluding exited ones)
        local running_containers=$(ssh_connect "cd $release_path && docker compose ps --filter 'status=running' --format json | wc -l")
        
        log_debug "Running containers: $running_containers / Expected: $expected_count"
        
        # Check if expected services are running
        if [ "$running_containers" -ge "$expected_count" ]; then
            log_info "All required containers are running successfully!"
            return 0
        fi
        
        sleep 5
        ((attempt++))
    done
    
    log_error "Deployment verification failed after $max_attempts attempts"
    return 1
}

# Check service health endpoints
check_service_health() {
    local release_path=$1
    
    log_info "Checking service health endpoints..."
    
    local kong_health=$(ssh_connect "curl -s -o /dev/null -w '%{http_code}' http://localhost:8474/status || echo '000'")
    if [ "$kong_health" = "200" ]; then
        log_info "Kong Admin API is healthy (HTTP $kong_health)"
    else
        log_warning "Kong Admin API returned HTTP $kong_health"
    fi
    
    local konga_health=$(ssh_connect "curl -s -o /dev/null -w '%{http_code}' http://localhost:1337 || echo '000'")
    if [ "$konga_health" = "200" ] || [ "$konga_health" = "302" ]; then
        log_info "Konga is healthy (HTTP $konga_health)"
    else
        log_warning "Konga returned HTTP $konga_health"
    fi
}

# Get and display container logs
show_container_logs() {
    local release_path=$1
    
    log_info "Fetching recent container logs..."
    ssh_connect "cd $release_path && docker compose logs --tail=20"
}

# Rollback function
rollback_deployment() {
    local release_path=$1
    
    log_error "Deployment failed. Rolling back..."
    ssh_connect "cd $release_path && docker compose down || true"
    
    local previous_release=$(ssh_connect "ls -1dt $DEPLOY_PATH/releases/* | sed -n '2p'")
    if [ -n "$previous_release" ]; then
        log_info "Rolling back to previous release: $previous_release"
        ssh_connect "ln -sfn $previous_release $DEPLOY_PATH/current"
        ssh_connect "cd $previous_release && docker compose up -d"
    fi
}

# Main deployment function
deploy() {
    log_info "Starting deployment..."
    log_info "Target: $VM_USER@$VM_HOST"
    log_info "Deploy Path: $DEPLOY_PATH"
    log_info "Version: $VERSION"
    
    # Test SSH connection first
    if ! test_ssh_connection; then
        log_error "Cannot proceed with deployment due to SSH connection failure"
        exit 1
    fi
    
    # Create timestamp for this release
    RELEASE_NAME=$(date +%Y%m%d_%H%M%S)
    RELEASE_PATH="$DEPLOY_PATH/releases/$RELEASE_NAME"
    log_info "Release name: $RELEASE_NAME"
    log_info "Release path: $RELEASE_PATH"
    
    # Create directories
    log_info "Creating release directory on remote server..."
    if ! ssh_connect "mkdir -p ${DEPLOY_PATH}/{releases,shared/{uploads,logs}}"; then
        log_error "Failed to create release directory structure"
        exit 1
    fi
    
    log_info "Creating new release directory: $RELEASE_PATH"
    if ! ssh_connect "mkdir -p $RELEASE_PATH"; then
        log_error "Failed to create release directory"
        exit 1
    fi
    
    # Create .env file from GitHub secret
    if [ -n "${ENV_FILE:-}" ]; then
        log_info "Creating .env file from GitHub secret..."
        if ssh_connect "cat > $RELEASE_PATH/.env << 'EOF'
$ENV_FILE
EOF"; then
            ssh_connect "chmod 600 $RELEASE_PATH/.env"
            log_info ".env file created successfully"
        else
            log_error "Failed to create .env file"
            exit 1
        fi
    else
        log_warning "ENV_FILE not provided, skipping .env creation"
    fi
    
    # Transfer files to the new release directory
    log_info "Transferring files to release directory..."
    if ! rsync -avz --delete \
        -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no" \
        --exclude 'deploy.sh' \
        --exclude '.git/' \
        --exclude 'README.md' \
        --exclude '.github/' \
        --exclude '.env' \
        --exclude 'node_modules/' \
        ./ "$VM_USER@$VM_HOST:$RELEASE_PATH/"; then
        log_error "File transfer failed"
        exit 1
    fi
    log_info "Files transferred successfully"
    
    # Create Docker network if it doesn't exist
    log_info "Ensuring Docker network exists..."
    ssh_connect "docker network create app_network 2>/dev/null || true"
    
    # Stop old containers
    log_info "Stopping old containers..."
    ssh_connect "cd $RELEASE_PATH && docker compose down || true"

    # Deploy with Docker Compose
    log_info "Starting Docker Compose deployment..."
    if ssh_connect "cd $RELEASE_PATH && docker compose up -d --build 2>&1"; then
        log_info "Docker Compose command executed successfully"
    else
        log_error "Docker Compose command failed"
        rollback_deployment "$RELEASE_PATH"
        exit 1
    fi
    
    # Verify deployment
    if check_docker_compose_status "$RELEASE_PATH"; then
        log_info "Deployment verification passed"
    else
        log_error "Deployment verification failed"
        show_container_logs "$RELEASE_PATH"
        rollback_deployment "$RELEASE_PATH"
        exit 1
    fi
    
    # Check service health
    sleep 10
    check_service_health "$RELEASE_PATH"
    
    # Create symlinks for shared resources
    log_info "Creating symlinks for shared resources..."
    ssh_connect "ln -sfn $DEPLOY_PATH/shared/uploads $RELEASE_PATH/uploads"
    ssh_connect "ln -sfn $DEPLOY_PATH/shared/logs $RELEASE_PATH/logs"
    log_info "Symlinks created successfully"
    
    # Update symlink to point to the new release
    log_info "Updating current symlink to point to the new release..."
    ssh_connect "ln -sfn $RELEASE_PATH $DEPLOY_PATH/current"
    log_info "Symlink updated successfully"
    
    # Display final status
    log_info "===================================="
    log_info "Deployment Status:"
    ssh_connect "cd $RELEASE_PATH && docker compose ps"
    log_info "===================================="
    
    # Keep only last 5 releases
    log_info "Cleaning up old releases..."
    ssh_connect "cd $DEPLOY_PATH/releases && ls -1dt */ | tail -n +6 | xargs -r rm -rf"
    log_info "Old releases cleaned up successfully"
    
    log_info "Deployment completed successfully!"
    log_info "Version: $VERSION"
    log_info "Release: $RELEASE_NAME"
}

# Run deployment
deploy