# Python MircroService Logger

![Repo Size](https://img.shields.io/github/repo-size/drussell33/Python-MircroService-Logger)
![Last Commit](https://img.shields.io/github/last-commit/drussell33/Python-MircroService-Logger)
![Top Language](https://img.shields.io/github/languages/top/drussell33/Python-MircroService-Logger)

## Project Description

Python MircroService Logger is a small Flask-based REST microservice for storing and retrieving activity log records in MongoDB. The project exposes HTTP endpoints for creating new activity entries and reading recent activity data, with deployment-oriented files for local development and Gunicorn-based hosting. The repository is structured as a proof-of-concept API service rather than a full multi-tier application.

## Key Features

- Exposes a REST API for creating and retrieving activity log records
- Persists activity data to MongoDB through `mongoengine`
- Defines an `activity_log` document model with `user_id`, `username`, `timestamp`, and `details`
- Returns recent activity records ordered by newest timestamp first
- Accepts JSON POST requests for new activity ingestion
- Adds a generated record location and UTC timestamp during insert flow
- Supports environment-variable-based configuration for database connectivity and delay simulation
- Includes a `rundev.sh` helper script for local Flask development
- Includes a `Procfile` for Gunicorn-based deployment
- Includes a pytest test module for basic API behavior validation

## Tech Stack

### Backend
- Python 3.8
- Flask
- Gunicorn
- MongoEngine
- PyMongo/BSON utilities used through MongoDB-related libraries

### Frontend
- None in this repository  
  This project is API-only and is intended to be consumed by external services or HTTP clients.

### Database
- MongoDB

### Tools / Services
- Pipenv for dependency management
- Pytest for tests
- Shell script-based local startup
- Heroku-style process definition via `Procfile`

## Architecture Overview

This repository implements a simple API-first microservice:

1. A client or upstream service sends HTTP requests to the Flask application.
2. The Flask app validates and processes incoming JSON payloads.
3. MongoEngine establishes the MongoDB connection using environment variables.
4. New activity records are inserted into the backing MongoDB collection.
5. Read endpoints query MongoDB, sort records by descending timestamp, and return JSON responses.

### Request Flow

- `POST /api/activities`
  - Accepts a JSON activity payload
  - Requires `user_id` and `username`
  - Inserts the document into MongoDB
  - Adds a UTC timestamp and a resource-style location field
  - Returns a `201 Created` response

- `GET /api/activities`
  - Returns the 10 most recent activity records

- `GET /api/activities/<activity_id>`
  - Returns the most recent records up to the numeric limit supplied in the route parameter, based on the current implementation

### Visible Patterns in the Code

- **Document model pattern:** the `activity_log` class defines the persisted schema
- **Environment-based configuration:** database settings and delay values come from environment variables
- **Thin route handlers:** route functions directly query or write to the database
- **No dedicated service/controller layering yet:** core logic currently lives in `app.py`

## Project Structure

```tree
Python-MircroService-Logger/
├── evidence/
│   ├── hw3/
│   ├── hw4/
│   ├── hw6/
│   └── hw7/
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── Procfile
├── README.md
├── app.py
├── rundev.sh
└── test_app.py
```

### Important Files and Folders

- `app.py` - Main Flask application, routes, MongoDB connection, and document model
- `test_app.py` - Pytest-based API tests for basic endpoint behavior
- `Pipfile` - Project dependencies and Python version requirement
- `Procfile` - Production process entry using Gunicorn
- `rundev.sh` - Development startup script with environment variable exports
- `evidence/` - Supplemental project artifacts grouped into homework-related folders

## Getting Started

### Prerequisites

- Python 3.8
- Pipenv
- MongoDB instance available locally or remotely
- Access to set the following environment variables:
  - `DB`
  - `DB_HOST`
  - `DB_USER`
  - `DB_PASSWORD`
  - `SLEEP_TIME` (optional)

### Installation

```bash
git clone https://github.com/drussell33/Python-MircroService-Logger.git
cd Python-MircroService-Logger
pipenv install
```

### Configuration

Set the required environment variables before starting the app.

Example values you will need to provide:

```bash
export DB="your_database_name"
export DB_HOST="your_mongodb_host"
export DB_USER="your_mongodb_user"
export DB_PASSWORD="your_mongodb_password"
export SLEEP_TIME=0
```

### Usage

#### Run the backend with Flask

```bash
pipenv run flask --app app.py run
```

#### Run the backend with the included development script

```bash
chmod +x rundev.sh
./rundev.sh 5000
```

#### Run tests

```bash
pipenv run pytest
```

#### Example API requests

Get the latest activities:

```bash
curl http://localhost:5000/api/activities
```

Get the latest activities up to a route-supplied numeric limit:

```bash
curl http://localhost:5000/api/activities/5
```

Create a new activity:

```bash
curl -X POST http://localhost:5000/api/activities \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "username": "Derek", "details": "Doing stuff related to this assignment"}'
```

## Roadmap

- [x] Create a Flask-based REST API
- [x] Connect the service to MongoDB
- [x] Define a persisted activity log document model
- [x] Implement activity creation endpoint
- [x] Implement recent activity retrieval endpoints
- [x] Add basic pytest coverage
- [x] Add a Gunicorn process entry for deployment
- [ ] Split routing, data access, and business logic into separate modules
- [ ] Add stronger request validation for required fields such as `details`
- [ ] Improve error handling and align tests with actual endpoint behavior
- [ ] Add pagination and clearer single-resource lookup semantics
- [ ] Add configuration and infrastructure files for reverse proxy/load balancing
- [ ] Remove unused dependencies and prune the dependency manifest
- [ ] Add authentication, authorization, and audit access controls
- [ ] Add containerization and environment-specific deployment guidance

## Contributing

Contributions should follow a standard GitHub workflow:

1. Fork the repository
2. Create a feature branch
3. Make and test your changes
4. Commit with clear messages
5. Push your branch
6. Open a pull request describing the change

When contributing, keep changes focused, document behavior clearly, and add or update tests where appropriate.

## Screenshots / Demo

Screenshots, example responses, or a hosted demo URL can be added here.

Suggested additions:
- API response samples
- MongoDB document examples
- Deployment screenshot
- Postman or HTTP client screenshots

## Contact

GitHub: [drussell33](https://github.com/drussell33)
