# Library Service API

A RESTful API for managing a library system built with Django REST Framework, PostgreSQL, Celery, and Docker.

## 🚀 Getting Started

### 📦 Requirements
- Docker  
- Docker Compose  
- (Optional) Make sure ports 8000, 5432, and 6379 are free

### ⚙️ Project Structure
```
library_service_api/
│
├── library_service_api/    # Django project settings
├── telegram_bot/           # Telegram bot app
├── Dockerfile              # Docker config for Django
├── docker-compose.yaml     # Services: Django, Postgres, Redis, Celery
├── requirements.txt
└── .env.sample             # Environment variables
```
### ⚒️ Setup & Run

1. Clone the repository

```bash
  git clone https://github.com/ngayka/library_service_api.git
  cd library_service_api
```
2. Create .env file
Use .env.sample as a template to create your own .env file
```bash
  cp .env.sample .env
```

3. Build and run the project
```bash
  docker-compose up --build
```
This will build the Django app image and start the following services:

Django app (port 8000)

PostgreSQL database

Redis (for Celery broker)

Celery worker

Celery Beat scheduler

4. Apply migrations and create superuser (in another terminal)
```bash
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py createsuperuser
```
### 📬 API Endpoints
API root: http://localhost:8000/api/

Admin panel: http://localhost:8000/admin/

### 🔄 Celery Tasks
Celery is used for asynchronous tasks like notifications and scheduled jobs.

Worker runs in celery service

Periodic tasks are managed by celery-beat service

View logs with:
```bash
  docker-compose logs -f celery
  docker-compose logs -f celery-beat
```

### ✅ Useful Commands
# Run tests
```bash
  docker-compose exec web python manage.py test
```
# Open Django shell
```bash
  docker-compose exec web python manage.py shell
```
# Stop all services
```bash
  docker-compose down
```
# Stop and remove volumes (e.g. Postgres data)
```bash
  docker-compose down -v
```

