# Job Tracker System

Job Tracker System is a production-style Flask microservices platform built to streamline job discovery, application tracking, and personalized recruitment workflows. The project showcases a scalable service-oriented architecture with role-based access control, JWT-based authentication and authorization, secure API design, and clean separation of concerns across independent services.

Designed as a practical showcase of backend engineering best practices, the system brings together user management, job catalog operations, and application lifecycle tracking in a modular and maintainable way.

## Overview

This system allows:
- Users to register, log in, and manage their profile
- Users to save and apply for jobs
- Recruiters to create and close job listings
- Users to set job preferences for personalized recommendations
- Applications to be tracked through different lifecycle statuses

## Architecture

The project follows a microservices approach with three main services:

1. User Service
   - Handles authentication and user accounts
   - Manages user preferences
   - Issues and validates JWT tokens

2. Job Service
   - Stores and serves job listings
   - Supports recruiter operations such as creating and closing jobs
   - Provides personalized job ranking based on user preferences

3. Application Service
   - Tracks user applications to jobs
   - Supports saving, applying, deleting, and updating application status
   - Communicates with the job service to validate job availability

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate / Alembic
- Flask-JWT-Extended
- Marshmallow
- Requests
- python-dotenv
- Logging and error handling

## Microservices

### 1. User Service
Location: user-service/

Responsibilities:
- User registration and login
- JWT-based authentication
- User profile retrieval
- Preference management

Key modules:
- app/blueprints/auth
- app/blueprints/preferences
- app/models/user.py
- app/models/preferences.py

### 2. Job Service
Location: job-service/

Responsibilities:
- Job catalog management
- Job search and filtering
- Personalized job recommendations
- Recruiter actions such as creating and closing job posts

Key modules:
- app/blueprints/jobs
- app/models/job.py
- app/clients/user_client.py
- app/blueprints/jobs/recommendation.py

### 3. Application Service
Location: application-service/

Responsibilities:
- Save and apply for jobs
- Track application statuses
- Manage application lifecycle events
- Query job details from the job service

Key modules:
- app/blueprints/applications
- app/models/application.py
- app/clients/job_service.py

## Inter-Service Communication

The services communicate over HTTP using Flask routes and the requests library.

### Communication Flow
- The Job Service calls the User Service to fetch a user's preferences.
- The Application Service calls the Job Service to verify whether a job exists and is still open before allowing an application.
- JWT tokens are forwarded through the Authorization header so each service can identify the authenticated user.

### Example Communication Patterns
- Job Service -> User Service:
  - Retrieves user preference data for personalization
- Application Service -> Job Service:
  - Checks job existence and status during application submission

This design keeps each service focused on its responsibility while still allowing the system to behave as one application.

## Project Structure

```text
job-tracker-system/
├── application-service/
│   ├── app/
│   │   ├── blueprints/
│   │   │   └── applications/
│   │   ├── clients/
│   │   ├── models/
│   │   ├── validators/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── logging_config.py
│   ├── migrations/
│   ├── run.py
│   └── instance/
├── job-service/
│   ├── app/
│   │   ├── blueprints/
│   │   │   └── jobs/
│   │   ├── clients/
│   │   ├── models/
│   │   ├── validators/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── logging_config.py
│   ├── migrations/
│   ├── run.py
│   └── instance/
├── user-service/
│   ├── app/
│   │   ├── blueprints/
│   │   │   ├── auth/
│   │   │   └── preferences/
│   │   ├── models/
│   │   ├── utils/
│   │   ├── validators/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── logging_config.py
│   ├── migrations/
│   ├── run.py
│   └── instance/
├── LICENSE
└── README.md
```

## Suggested User Flow

A typical user journey in this system is:

1. Register a new account in the user service
2. Log in to receive a JWT token
3. Save or apply for jobs through the application service
4. View the status of saved or applied jobs in the application dashboard
5. Use preferences to improve job recommendations

## Notes

- Database configuration is driven by environment variables such as DATABASE_URL and JWT_SECRET_KEY.
- Each service uses Flask application factories and blueprints for modular structure.
- Migrations are handled with Alembic for schema changes.
