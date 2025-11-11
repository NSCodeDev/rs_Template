# Changelog

All notable changes to this Django microservices template will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-11

### Added

- Initial release of Advensis Django Microservices Template
- Copier-based template generation system
- Django 5.2+ with Django REST Framework
- JWT Authentication using Simple JWT
- Auto-generated API documentation with drf-spectacular
- PostgreSQL and SQLite database support
- Docker and Docker Compose configurations
- Multiple environment support (development, staging, production)
- Optional Celery integration for background tasks
- Optional Redis integration for caching/sessions
- CORS configuration
- Comprehensive logging setup
- WhiteNoise for static file serving
- Base models and utilities in core module
- Example Django apps structure
- Environment-specific settings management
- Automated migration and static file collection in entrypoint
- Docker network setup for microservices architecture
- Configurable ports for services
- Comprehensive README documentation
- Usage guide for template users and maintainers
- Test scripts for template validation

### Template Files

- `Dockerfile.jinja` - Production Docker configuration
- `Dockerfile.stage.jinja` - Staging Docker configuration
- `docker-compose.yml.jinja` - Production compose file
- `docker-compose.dev.yml.jinja` - Development compose file
- `docker-compose.stage.yml.jinja` - Staging compose file
- `requirements.txt.jinja` - Python dependencies with optional packages
- `entrypoint.sh.jinja` - Container startup script
- `config/settings.py.jinja` - Django settings with environment support
- `.env.example.jinja` - Production environment template
- `.env.development.jinja` - Development environment template
- `.env.staging.jinja` - Staging environment template
- `.gitignore.jinja` - Git ignore patterns
- `README.md.jinja` - Project documentation template

### Configuration

- `copier.yml` - Template configuration with validation
- `.copierignore` - Files to exclude from generation
- `test-template.sh` - Unix test script
- `test-template.bat` - Windows test script

### Features

- Automatic project name to slug conversion
- PostgreSQL version selection (15, 16, 17, 17.4, 18)
- Python version selection (3.10, 3.11, 3.12+)
- Conditional dependency inclusion based on selections
- Docker resource limits for production
- Volume persistence for databases
- Hot-reload for development environment
- Separate networks for different environments
- Celery worker and beat configurations
- Redis caching setup
- API documentation at `/api/schema/swagger-ui/`
- Admin panel at `/admin`

### Documentation

- Comprehensive README with quick start guide
- Usage documentation for users and maintainers
- Troubleshooting section
- Best practices guide
- CI/CD integration suggestions
- Example project structures

## [Unreleased]

### Planned

- GitHub Actions workflow templates
- Pre-commit hooks configuration
- Additional database options (MySQL, MongoDB)
- Message queue alternatives (RabbitMQ)
- Monitoring setup (Prometheus, Grafana)
- OpenTelemetry integration
- Kubernetes deployment templates
- Testing framework setup (pytest, coverage)
- Code quality tools (black, flake8, mypy)
- API versioning examples
- WebSocket support with Django Channels
- GraphQL integration option
- Multi-stage Docker builds
- Health check endpoints
- Rate limiting middleware
- Custom user model template
- Email configuration templates
- File upload handling examples
- Internationalization setup

---

## Version History

- **1.0.0** (2025-11-11) - Initial release

## Migration Guide

### Updating Existing Projects

When a new version of the template is released, update your project:

```bash
cd your-project
copier update
```

Review the changes and resolve any conflicts.

### Breaking Changes

None yet (initial release)

## Support

For questions or issues:

- GitHub Issues: [Your Repo URL]
- Email: contact@advensis.com
- Documentation: See README.md and USAGE.md
