# Advensis Django Microservices Template

A production-ready Django REST Framework template for creating microservices with Docker support, powered by [Copier](https://copier.readthedocs.io/).

## Features

- 🚀 Django 5.2+ with Django REST Framework
- 🔐 JWT Authentication (Simple JWT)
- 📚 Auto-generated API documentation (drf-spectacular)
- 🐘 PostgreSQL or SQLite database support
- 🐳 Docker and Docker Compose ready
- 🔄 Optional Celery for background tasks
- ⚡ Optional Redis for caching/sessions
- 🌍 CORS configuration
- 📝 Comprehensive logging
- 🎨 Multiple environments (development, staging, production)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Template Structure](#template-structure)
- [Configuration Options](#configuration-options)
- [Environment Variables](#environment-variables)
- [Docker Deployment](#docker-deployment)
- [Common Tasks](#common-tasks)
- [For Template Maintainers](#for-template-maintainers)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Support](#support)

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Copier](https://copier.readthedocs.io/) - `pip install copier`
- [Docker](https://www.docker.com/) and Docker Compose (optional but recommended)

## Quick Start

### 1. Install Copier

```bash
pip install copier
```

### 2. Generate a New Project

```bash
# From local directory
copier copy path/to/this/template /path/to/your/new/project

# From Git repository
copier copy https://github.com/NSCodeDev/rs_Template.git /path/to/your/new/project
```

### 3. Answer the Prompts

Copier will ask you several questions:

- **project_name**: The name of your project (e.g., "auth-service")
- **project_slug**: Python package name (auto-generated from project_name)
- **project_description**: Brief description of your service
- **author_name**: Your name or organization
- **author_email**: Contact email
- **python_version**: Python version to use (3.10, 3.11, 3.12)
- **use_postgres**: Use PostgreSQL? (Yes/No, default: Yes)
- **postgres_version**: PostgreSQL version if using PostgreSQL
- **use_celery**: Add Celery for background tasks? (Yes/No)
- **use_redis**: Add Redis for caching? (Yes/No)
- **docker_name**: Docker Compose project name
- **docker_api_container_name**: API container name
- **server_port**: Port to expose the service (required)
- **db_port**: Database port (if using PostgreSQL)

### 4. Navigate to Your Project

```bash
cd /path/to/your/new/project
```

### 5. Set Up the Project

#### Option A: Using Docker (Recommended)

```bash
# Create Docker network
docker network create app_dev_network

# Copy and configure environment file
cp .env.development .env.development

# Build and start services
docker-compose -f docker-compose.dev.yml up --build
```

#### Option B: Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.development .env.development

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 6. Access Your Application

- **API**: http://localhost:{server_port}
- **Admin Panel**: http://localhost:{server_port}/admin
- **API Docs (Swagger)**: http://localhost:{server_port}/api/schema/swagger-ui/
- **API Docs (ReDoc)**: http://localhost:{server_port}/api/schema/redoc/

## Template Structure

```
your-project/
├── apps/                          # Django applications
│   ├── exampleapp/               # Example app (can be deleted)
│   └── anotherapp/               # Another example
├── config/                        # Project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                  # URL routing
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
├── core/                         # Core utilities
│   ├── models/                  # Base models
│   └── utils/                   # Utility functions
├── middlewares/                  # Custom middlewares
├── docker-compose.yml           # Production compose
├── docker-compose.dev.yml       # Development compose
├── docker-compose.stage.yml     # Staging compose
├── Dockerfile                   # Production Dockerfile
├── Dockerfile.stage             # Staging Dockerfile
├── requirements.txt             # Python dependencies
├── manage.py                    # Django CLI
├── entrypoint.sh               # Container entrypoint
├── .env.example                # Environment template
├── .env.development            # Dev environment
├── .env.staging                # Staging environment
└── README.md                   # Project documentation
```

## Configuration Options

### Python Version

Choose from:

- `3.10` - Python 3.10
- `3.11` - Python 3.11 (recommended)
- `3.12` - Python 3.12+

### Database Options

- **PostgreSQL**: Production-ready relational database
  - Versions: 15, 16, 17, 17.4, 18
  - Recommended for production
- **SQLite**: Lightweight, file-based database
  - Good for development/testing
  - Not recommended for production

### Optional Services

- **Celery**: For background tasks and async processing
  - Requires Redis as message broker
  - Includes celery-worker and celery-beat containers
- **Redis**: For caching and session storage
  - Can be used independently or with Celery
  - Improves application performance

## Environment Variables

The template generates appropriate `.env` files for each environment:

### Development (.env.development)

- `DEBUG=True`
- Verbose logging
- Development-friendly settings

### Staging (.env.staging)

- `DEBUG=False`
- Production-like environment
- For testing before production

### Production (.env)

- `DEBUG=False`
- Optimized for performance
- Security hardened

## Docker Deployment

### Development

```bash
docker network create app_dev_network
docker-compose -f docker-compose.dev.yml up
```

### Staging

```bash
docker network create app_stage_network
docker-compose -f docker-compose.stage.yml up -d
```

### Production

```bash
docker network create app_network
docker-compose up -d
```

## Updating Your Project

To update your project when the template changes:

```bash
copier update
```

This will prompt you to review and accept changes.

## Customization

After generating your project:

1. **Remove example apps**: Delete `apps/exampleapp` and `apps/anotherapp`
2. **Update settings**: Modify `config/settings.py` for your needs
3. **Add your apps**: Create new Django apps in the `apps/` directory
4. **Configure URLs**: Update `config/urls.py` with your routes
5. **Update README**: Customize the generated `README.md`

## Common Tasks

### Create a New App

```bash
docker-compose exec your-api-container python manage.py startapp myapp apps/myapp
```

### Run Migrations

```bash
docker-compose exec your-api-container python manage.py migrate
```

### Create Superuser

```bash
docker-compose exec your-api-container python manage.py createsuperuser
```

### Collect Static Files

```bash
docker-compose exec your-api-container python manage.py collectstatic
```

### Run Tests

```bash
docker-compose exec your-api-container python manage.py test
```

## CI/CD Integration

The template is designed to work with:

- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

Example workflows can be added to `.github/workflows/` directory.

## Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use environment variables** - Keep secrets out of code
3. **Regular updates** - Keep dependencies up to date
4. **Docker for consistency** - Use Docker in all environments
5. **Code reviews** - Review all changes before merging
6. **Testing** - Write tests for all new features
7. **Documentation** - Keep API docs updated

## Troubleshooting

### Port Already in Use

Change the port in `docker-compose.yml` and `.env` file.

### Database Connection Failed

- Check database credentials in `.env`
- Ensure PostgreSQL container is running
- Verify network connectivity

### Permission Denied (entrypoint.sh)

```bash
chmod +x entrypoint.sh
```

## For Template Maintainers

### Testing the Template

**Windows:**

```bash
test-template.bat
```

**Linux/Mac:**

```bash
chmod +x test-template.sh
./test-template.sh
```

### Template Structure

```
rp_template/
├── copier.yml              # Template configuration
├── .copierignore          # Files to exclude
├── README.md              # This documentation
├── test-template.sh       # Unix test script
├── test-template.bat      # Windows test script
└── template/              # Template files
    ├── apps/
    ├── config/
    ├── core/
    ├── middlewares/
    ├── *.jinja            # Templated files
    └── ...
```

### Adding New Features

1. Modify `copier.yml` to add new questions
2. Add conditional logic in `.jinja` files
3. Test with test scripts
4. Document in README.md

### Common Jinja Patterns

```jinja
{# Conditional blocks #}
{%- if use_postgres %}
    # PostgreSQL configuration
{%- else %}
    # SQLite configuration
{%- endif %}

{# Variable substitution #}
{{ project_name }}
{{ server_port }}

{# Comments (not included in output) #}
{# This is a comment #}
```

### Configuration Variables

| Variable                    | Type | Description         | Default                 |
| --------------------------- | ---- | ------------------- | ----------------------- |
| `project_name`              | str  | Project name        | my-project              |
| `project_slug`              | str  | Python package name | Auto-generated          |
| `project_description`       | str  | Description         | "A Service of Advensis" |
| `author_name`               | str  | Author              | Advensis                |
| `author_email`              | str  | Email               | contact@advensis.com    |
| `python_version`            | str  | Python version      | 3.11                    |
| `use_postgres`              | bool | Use PostgreSQL      | true                    |
| `postgres_version`          | str  | PostgreSQL version  | 17.4                    |
| `use_celery`                | bool | Add Celery          | false                   |
| `use_redis`                 | bool | Add Redis           | false                   |
| `docker_name`               | str  | Docker project name | Auto-generated          |
| `docker_api_container_name` | str  | Container name      | Auto-generated          |
| `server_port`               | int  | Server port         | Required                |
| `db_port`                   | int  | Database port       | 5433                    |

### Generated Files from Templates

These files are generated with Jinja templating:

- `Dockerfile` - From `Dockerfile.jinja`
- `docker-compose.yml` - From `docker-compose.yml.jinja`
- `docker-compose.dev.yml` - From `docker-compose.dev.yml.jinja`
- `docker-compose.stage.yml` - From `docker-compose.stage.yml.jinja`
- `Dockerfile.stage` - From `Dockerfile.stage.jinja`
- `entrypoint.sh` - From `entrypoint.sh.jinja`
- `requirements.txt` - From `requirements.txt.jinja`
- `config/settings.py` - From `config/settings.py.jinja`
- `.env.example` - From `.env.example.jinja`
- `.env.development` - From `.env.development.jinja`
- `.env.staging` - From `.env.staging.jinja`
- `.gitignore` - From `.gitignore.jinja`
- `README.md` - From `README.md.jinja`

### Best Practices for Template Development

1. **Version Control**: Commit template changes regularly
2. **Testing**: Always test generation before committing
3. **Documentation**: Update README when adding features
4. **Backwards Compatibility**: Be careful with breaking changes
5. **Validation**: Add validators in copier.yml
6. **Defaults**: Provide sensible defaults for all questions

### Deployment to Repository

```bash
# Commit changes
git add .
git commit -m "Update template"
git push origin main

# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Users can use tagged versions
copier copy --vcs-ref=v1.0.0 https://github.com/NSCodeDev/rs_Template.git ../my-project
```

## Contributing

If you want to improve this template:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Copier
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Support

For issues and questions:

- **Email**: contact@advensis.com
- **Repository**: https://github.com/NSCodeDev/rs_Template
- **Issues**: https://github.com/NSCodeDev/rs_Template/issues

## License

MIT License - See LICENSE file for details

---

**Created by Advensis** - Building scalable microservices
