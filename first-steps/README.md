# Mini Blog API

An in-progress learning project built while taking DevTalles' FastAPI course on Udemy. The code and features are being developed as part of the course, so the project may change over time and is intended for educational purposes rather than production use.

## About

This repository contains a small blog API built with FastAPI. It is used to practice backend development concepts, including:

- Creating and managing blog posts and tags
- Searching, filtering, sorting, and paginating results
- Validating request and response data with Pydantic
- Persisting data with SQLAlchemy (SQLite by default)
- Authenticating users with bearer tokens
- Uploading and serving media files

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Getting started

From the project directory, install the dependencies declared in `pyproject.toml`:

```bash
uv sync
```

`uv sync` creates the `.venv` virtual environment and installs the versions recorded in `uv.lock`.

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

`uv run` executes the command in the project's environment. Alternatively, start the server with FastAPI's development command:

```bash
uv run fastapi dev app/main.py
```

The API is available at <http://127.0.0.1:8000>. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

## Configuration

The application uses SQLite at `./blog.db` by default. Settings can be provided through environment variables or a `.env` file:

| Variable | Description | Default |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy database connection URL | `sqlite:///./blog.db` |
| `MAX_UPLOAD_MB` | Maximum upload size in megabytes | `10` |

JWT settings are read from the process environment:

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Secret used to sign access tokens | `change-my-in-prod` |
| `ACCESS_TOKEN_EXPIRES_MINUTES` | Access-token lifetime in minutes | `30` |

Set a strong, private `SECRET_KEY` before using the application beyond local learning. The default value is for development only.

## Project structure

```text
app/
├── api/v1/       # Authentication, posts, tags, and upload endpoints
├── core/         # Database, configuration, and security setup
├── models/       # SQLAlchemy models
├── services/     # Shared services, including file storage and pagination
└── main.py       # FastAPI application setup
```
