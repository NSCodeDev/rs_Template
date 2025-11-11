# Quick Reference Guide

## Copier Commands

### Generate New Project

```bash
# Interactive mode
copier copy path/to/rp_template /path/to/new/project

# With pre-filled answers
copier copy --data project_name="my-service" path/to/rp_template /path/to/new/project

# From Git repository
copier copy https://github.com/NSCodeDev/rs_Template.git /path/to/new/project
```

### Update Existing Project

```bash
cd /path/to/your/project
copier update
```

### Recopy with Force

```bash
copier copy --force path/to/rp_template /path/to/new/project
```

## Docker Commands

### Development Environment

```bash
# Create network (first time only)
docker network create app_dev_network

# Start services
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose -f docker-compose.dev.yml up -d

# Rebuild and start
docker-compose -f docker-compose.dev.yml up --build

# Stop services
docker-compose -f docker-compose.dev.yml down

# Stop and remove volumes
docker-compose -f docker-compose.dev.yml down -v

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# View specific service logs
docker-compose -f docker-compose.dev.yml logs -f {container-name}
```

### Production Environment

```bash
# Create network (first time only)
docker network create app_network

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Staging Environment

```bash
# Create network (first time only)
docker network create app_stage_network

# Start services
docker-compose -f docker-compose.stage.yml up -d

# Stop services
docker-compose -f docker-compose.stage.yml down
```

## Django Management Commands

### Inside Docker Container

```bash
# Run any Django command
docker-compose exec {container-name} python manage.py <command>

# Make migrations
docker-compose exec {container-name} python manage.py makemigrations

# Run migrations
docker-compose exec {container-name} python manage.py migrate

# Create superuser
docker-compose exec {container-name} python manage.py createsuperuser

# Django shell
docker-compose exec {container-name} python manage.py shell

# Collect static files
docker-compose exec {container-name} python manage.py collectstatic

# Run tests
docker-compose exec {container-name} python manage.py test

# Create new app
docker-compose exec {container-name} python manage.py startapp myapp apps/myapp
```

### Local Development (without Docker)

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run development server
python manage.py runserver

# All other commands same as above
python manage.py migrate
python manage.py createsuperuser
# etc.
```

## Environment Files

### Development (.env.development)

```env
DEBUG=True
SECRET_KEY=dev-secret-key
DB_HOST=postgres-dev
ALLOWED_HOSTS=*
```

### Staging (.env.staging)

```env
DEBUG=False
SECRET_KEY=stage-secret-key
DB_HOST=postgres-stage
ALLOWED_HOSTS=staging.example.com
```

### Production (.env)

```env
DEBUG=False
SECRET_KEY=production-secret-key
DB_HOST=advensis_postgres
ALLOWED_HOSTS=api.example.com,example.com
```

## Common Ports

| Service    | Development Port               | Production Port |
| ---------- | ------------------------------ | --------------- |
| API        | Configurable                   | Configurable    |
| PostgreSQL | 5433 (host) → 5432 (container) | Internal only   |
| Redis      | 6379                           | Internal only   |

## Template Variables Reference

| Variable                    | Example            | Description           |
| --------------------------- | ------------------ | --------------------- |
| `project_name`              | "auth-service"     | Human-readable name   |
| `project_slug`              | "auth_service"     | Python package name   |
| `python_version`            | "3.11"             | Python version        |
| `postgres_version`          | "17.4"             | PostgreSQL version    |
| `server_port`               | 8001               | API server port       |
| `db_port`                   | 5433               | Database exposed port |
| `docker_name`               | "auth_service_dev" | Docker Compose name   |
| `docker_api_container_name` | "auth-api"         | Container name        |

## File Structure After Generation

```
your-project/
├── apps/                    # Your Django apps
├── config/                  # Project settings
│   ├── settings.py         # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── core/                   # Core utilities
│   ├── models/            # Base models
│   └── utils/             # Helper functions
├── middlewares/           # Custom middleware
├── logs/                  # Log files (auto-created)
├── staticfiles/           # Collected static files
├── docker-compose.yml     # Production
├── docker-compose.dev.yml # Development
├── docker-compose.stage.yml # Staging
├── Dockerfile             # Production
├── Dockerfile.stage       # Staging
├── requirements.txt       # Dependencies
├── manage.py             # Django CLI
├── entrypoint.sh         # Container startup
├── .env                  # Production env (create manually)
├── .env.development      # Dev env (create manually)
├── .env.staging          # Stage env (create manually)
├── .gitignore           # Git ignore rules
└── README.md            # Project docs
```

## API Endpoints (Default)

| Endpoint                  | Description              |
| ------------------------- | ------------------------ |
| `/admin/`                 | Django admin panel       |
| `/api/schema/`            | OpenAPI schema (JSON)    |
| `/api/schema/swagger-ui/` | Swagger UI documentation |
| `/api/schema/redoc/`      | ReDoc documentation      |

## Troubleshooting Quick Fixes

### Port Already in Use

```bash
# Find process using port
lsof -i :8001  # Linux/Mac
netstat -ano | findstr :8001  # Windows

# Kill the process or change port in .env
```

### Permission Denied

```bash
# Make script executable
chmod +x entrypoint.sh
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check database credentials in .env
cat .env.development

# Restart database
docker-compose restart postgres-dev
```

### Module Not Found

```bash
# Rebuild containers
docker-compose up --build

# Check requirements.txt
cat requirements.txt
```

### Clear Everything and Start Fresh

```bash
# Stop and remove everything
docker-compose down -v

# Remove images (optional)
docker-compose down --rmi all

# Rebuild
docker-compose up --build
```

## Git Workflow

### Initial Setup

```bash
git init
git add .
git commit -m "Initial commit from Advensis template"
git remote add origin <your-repo-url>
git push -u origin main
```

### Regular Commits

```bash
git add .
git commit -m "Your commit message"
git push
```

### Branching

```bash
# Create feature branch
git checkout -b feature/new-feature

# Push feature branch
git push -u origin feature/new-feature

# Merge to main
git checkout main
git merge feature/new-feature
git push
```

## Testing

### Run Tests

```bash
# All tests
docker-compose exec {container-name} python manage.py test

# Specific app
docker-compose exec {container-name} python manage.py test apps.exampleapp

# With coverage (if installed)
docker-compose exec {container-name} coverage run manage.py test
docker-compose exec {container-name} coverage report
```

## Performance

### View Container Stats

```bash
docker stats
```

### View Logs Size

```bash
du -sh logs/
```

### Clear Logs

```bash
rm logs/*.log
```

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use strong database passwords
- [ ] Enable HTTPS in production
- [ ] Set up proper CORS origins
- [ ] Review security middleware
- [ ] Keep dependencies updated
- [ ] Don't commit .env files
- [ ] Use environment variables for secrets

## Useful Links

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Docker Docs: https://docs.docker.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Copier Docs: https://copier.readthedocs.io/

---

**Keep this file handy for quick reference!**
