# Mini Blog API

REST API built with FastAPI as a practical project during the DevTalles FastAPI course on Udemy. The project is under development and is intended for learning, not production use.

## Features

- User registration and login
- JWT authentication and role-based authorization
- Post and tag CRUD operations
- Search, filtering, sorting, and pagination
- Request and response validation with Pydantic
- Persistence with SQLAlchemy and SQLite by default
- Media file uploads

## Roles

The API recognizes three roles:

| Role     | Main permissions                              |
| -------- | --------------------------------------------- |
| `user`   | Access protected resources available to users |
| `editor` | Create and update posts and tags              |
| `admin`  | Delete posts and tags and update user roles   |

Role changes must be deliberate and can be performed through `/api/v1/auth/role/{user_id}` by an administrator.

## Requirements

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation and execution

From `first-steps`, install the dependencies and create the virtual environment:

```bash
uv sync
```

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

You can also use FastAPI's development command:

```bash
uv run fastapi dev app/main.py
```

The API will be available at <http://127.0.0.1:8000>.

- Swagger documentation: <http://127.0.0.1:8000/docs>
- ReDoc documentation: <http://127.0.0.1:8000/redoc>

When the application starts, FastAPI automatically creates SQLAlchemy tables that do not exist yet in the configured SQLite database.

## Configuration

The application uses SQLite at `./blog.db` by default. Variables can be declared in the environment or in a `.env` file located in `first-steps`:

| Variable                           | Description                            | Default               |
| ---------------------------------- | -------------------------------------- | --------------------- |
| `DATABASE_URL`                     | SQLAlchemy connection URL              | `sqlite:///./blog.db` |
| `JWT_SECRET_KEY`                   | Private key used to sign JWT tokens    | `change-my-in-prod`   |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | Access-token lifetime in minutes       | `30`                  |
| `JWT_ALGORITHM`                    | Algorithm used to sign tokens          | `HS256`               |
| `MAX_UPLOAD_MB`                    | Maximum size of each file in megabytes | `10`                  |

Example `.env`:

```dotenv
DATABASE_URL=sqlite:///./blog.db
JWT_SECRET_KEY=replace-this-with-a-private-secret
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=30
JWT_ALGORITHM=HS256
MAX_UPLOAD_MB=10
```

> Replace `JWT_SECRET_KEY` with a strong, private value before using the API outside a local environment.

## Authentication usage

1. Register a user with `POST /api/v1/auth/register`.
2. Log in with `POST /api/v1/auth/login`.
3. Copy the `access_token` value from the response.
4. In Swagger, click **Authorize**, enter the token, and confirm.

You can also obtain a token through the OAuth2-compatible flow at `POST /api/v1/auth/token`. Query the authenticated user with `GET /api/v1/auth/me`.

Registration example:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password123",
    "full_name": "Example User"
  }'
```

Login example:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password123"
  }'
```

To call a protected endpoint, send this header:

```text
Authorization: Bearer <access_token>
```

## Main routes

All routes include the prefixes defined by the application. Use `/docs` to inspect exact parameters, models, and permissions.

| Resource       | Base route     | Main operations                                                  |
| -------------- | -------------- | ---------------------------------------------------------------- |
| Authentication | `/api/v1/auth` | Registration, login, OAuth2 token, profile, and role updates     |
| Posts          | `/posts`       | Listing, search, tags, retrieval, creation, update, and deletion |
| Tags           | `/tags`        | Listing, creation, update, deletion, and popularity ranking      |
| Uploads        | `/upload`      | Byte reception, file metadata, and persistent storage            |

Saved files are available at `/media/<file-name>`.

## Post examples

Query one page of posts:

```bash
curl "http://127.0.0.1:8000/posts?page=1&per_page=10&order_by=id&direction=desc"
```

Search by title:

```bash
curl "http://127.0.0.1:8000/posts?search=fastapi"
```

Filter by multiple tags:

```bash
curl "http://127.0.0.1:8000/posts/by-tags?tags=python&tags=fastapi"
```

Creation and update operations may require authentication and a specific role.

## Project structure

```text
app/
├── api/v1/
│   ├── auth/       # Registration, login, JWT, and role management
│   ├── posts/      # Post endpoints and repository
│   ├── tags/       # Tag endpoints and repository
│   └── uploads/    # Upload and storage examples
├── core/           # Configuration, database, and security
├── models/         # SQLAlchemy models
├── services/       # File storage and shared services
├── media/          # Stored media files
└── main.py         # Application setup and router mounting
```

## Development

Run the application with automatic reload during development:

```bash
uv run uvicorn app.main:app --reload
```

Use Swagger at `/docs` to test endpoints and review their input and output schemas.
