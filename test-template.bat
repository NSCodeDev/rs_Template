@echo off
REM Test Template Generation Script for Windows
REM This script tests the Copier template generation

echo ==========================================
echo Testing Advensis Django Template
echo ==========================================

REM Set test output directory
set TEST_DIR=..\template-test-output

REM Remove old test directory if exists
if exist "%TEST_DIR%" (
    echo Removing old test directory...
    rmdir /s /q "%TEST_DIR%"
)

REM Generate project with default values
echo Generating test project...
copier copy --force ^
    --data project_name="test-service" ^
    --data project_slug="test_service" ^
    --data project_description="Test Service" ^
    --data author_name="Test Author" ^
    --data author_email="test@example.com" ^
    --data python_version="1.1.0" ^
    --data use_postgres=true ^
    --data postgres_version="17.4" ^
    --data use_celery=false ^
    --data use_redis=false ^
    --data docker_name="test_service_dev" ^
    --data docker_api_container_name="test-api" ^
    --data server_port=8001 ^
    --data db_port=5433 ^
    . "%TEST_DIR%"

if %errorlevel% equ 0 (
    echo ==========================================
    echo Template generation successful!
    echo ==========================================
    echo Test project created at: %TEST_DIR%
    echo.
    echo To test the generated project:
    echo   cd %TEST_DIR%
    echo   docker network create app_dev_network
    echo   docker-compose -f docker-compose.dev.yml up --build
    echo.
) else (
    echo ==========================================
    echo Template generation failed!
    echo ==========================================
    exit /b 1
)
