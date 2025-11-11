# Contributing to Advensis Django Template

Thank you for considering contributing to the Advensis Django Microservices Template! This document provides guidelines for contributing to the template.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Template Structure](#template-structure)
- [Testing Changes](#testing-changes)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports:

- Check existing issues
- Test with the latest version
- Provide clear reproduction steps

Include in your bug report:

- Template version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Environment details (OS, Python version, Docker version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:

- Clear use case
- Expected behavior
- Why this would benefit users
- Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

### Prerequisites

```bash
# Install required tools
pip install copier
pip install jinja2
```

### Clone the Repository

```bash
git clone https://github.com/NSCodeDev/rs_Template.git
cd rs_Template
```

### Make Changes

Edit files in the `template/` directory:

- Use `.jinja` extension for templated files
- Update `copier.yml` for new configuration options
- Update documentation as needed

## Template Structure

### Key Files

- `copier.yml` - Template configuration and questions
- `.copierignore` - Files to exclude from generation
- `template/` - Template files with Jinja syntax

### Jinja Syntax

```jinja
{# Comments - not included in output #}
{# This is a comment #}

{# Variables #}
{{ project_name }}
{{ server_port }}

{# Conditionals #}
{% if use_postgres %}
    PostgreSQL configuration
{% else %}
    SQLite configuration
{% endif %}

{# Loops (if needed) #}
{% for item in items %}
    {{ item }}
{% endfor %}
```

## Testing Changes

### 1. Test Template Generation

**Windows:**

```bash
test-template.bat
```

**Linux/Mac:**

```bash
chmod +x test-template.sh
./test-template.sh
```

### 2. Manual Testing

```bash
# Generate test project
copier copy . ../test-project

# Navigate to project
cd ../test-project

# Test development environment
docker network create app_dev_network
docker-compose -f docker-compose.dev.yml up --build

# Verify:
# - Services start correctly
# - No errors in logs
# - API is accessible
# - Documentation works
# - Database connections work
```

### 3. Test Different Configurations

Test with various options:

**Minimal (SQLite, no extras):**

```bash
copier copy --force \
  --data use_postgres=false \
  --data use_celery=false \
  --data use_redis=false \
  . ../test-minimal
```

**Full (PostgreSQL, Celery, Redis):**

```bash
copier copy --force \
  --data use_postgres=true \
  --data use_celery=true \
  --data use_redis=true \
  . ../test-full
```

### 4. Validate Generated Files

Check that generated files:

- Have no Jinja syntax errors
- Are syntactically valid (Python, YAML, Dockerfile)
- Follow best practices
- Include all necessary configurations

## Submitting Changes

### Commit Message Format

```
type(scope): brief description

Detailed explanation of what changed and why.

Fixes #issue_number
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:

```
feat(docker): add support for Docker Compose v2

Added compatibility with Docker Compose v2 syntax while
maintaining backward compatibility with v1.

Fixes #123
```

```
docs(readme): update quick start guide

Clarified Docker network creation steps and added
troubleshooting for common port conflicts.
```

### Pull Request Process

1. **Update Documentation**: If you change functionality, update:

   - README.md
   - USAGE.md
   - CHANGELOG.md
   - Any affected documentation

2. **Test Thoroughly**: Run all test scripts and verify different configurations

3. **Update CHANGELOG**: Add your changes under `[Unreleased]` section

4. **Create PR**:

   - Use clear title and description
   - Reference related issues
   - Describe testing performed
   - Include screenshots if relevant

5. **Code Review**: Address feedback constructively

6. **Merge**: Maintainer will merge when approved

## Style Guidelines

### Python Code

Follow PEP 8:

```python
# Good
def my_function(param1, param2):
    """Clear docstring."""
    return param1 + param2

# Bad
def myFunction( param1,param2 ):
    return param1+param2
```

### Jinja Templates

```jinja
{# Good #}
{% if use_postgres %}
DB_ENGINE=django.db.backends.postgresql
{% else %}
DB_ENGINE=django.db.backends.sqlite3
{% endif %}

{# Bad #}
{%if use_postgres%}DB_ENGINE=django.db.backends.postgresql{%else%}DB_ENGINE=django.db.backends.sqlite3{%endif%}
```

### YAML Files

```yaml
# Good
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8001:8001"

# Bad
services:
  api:
    build: {context: ., dockerfile: Dockerfile}
    ports: ["8001:8001"]
```

### Documentation

- Use clear, concise language
- Include code examples
- Add troubleshooting sections
- Keep formatting consistent
- Update table of contents

## Adding New Features

### Adding a New Configuration Option

1. **Update copier.yml**:

```yaml
use_new_feature:
  type: bool
  help: "Enable new feature?"
  default: false
```

2. **Update Template Files**:

```jinja
{% if use_new_feature %}
# New feature configuration
NEW_FEATURE_ENABLED=True
{% endif %}
```

3. **Update Documentation**:

- Add to README.md features list
- Document in USAGE.md
- Add example in QUICKREF.md
- Update CHANGELOG.md

4. **Test**:

- Test with feature enabled
- Test with feature disabled
- Verify no conflicts with other options

### Adding a New Service (e.g., RabbitMQ)

1. Add question to `copier.yml`
2. Update `requirements.txt.jinja` with dependencies
3. Add service to `docker-compose.*.yml.jinja` files
4. Update `settings.py.jinja` with configuration
5. Update `.env.*.jinja` files with variables
6. Update documentation
7. Test thoroughly

## What to Contribute

### High Priority

- Bug fixes
- Security improvements
- Performance optimizations
- Documentation improvements
- Test coverage

### Welcome Additions

- New database options (MySQL, MongoDB)
- Message queue alternatives (RabbitMQ, Kafka)
- Monitoring tools (Prometheus, Grafana)
- Testing frameworks (pytest setup)
- CI/CD templates
- Code quality tools

### Nice to Have

- Additional Python versions
- Alternative web servers
- GraphQL support
- WebSocket support
- API versioning examples

## Questions?

- Open an issue for discussion
- Email: contact@advensis.com
- Check existing documentation

## Recognition

Contributors will be recognized in:

- CHANGELOG.md
- GitHub contributors page
- Project documentation

Thank you for contributing! 🎉
