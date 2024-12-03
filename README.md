Repository link: https://github.com/bihunva/chi-articles-management-platform

## Articles Management Platform

<p>A web application built with Flask for managing users and articles with a secure authentication system and role-based access control</p>

### Technologies Used

**Backend:**

- **Flask**: Backend framework.
- **Flask-SQLAlchemy**: ORM for interaction with the database.
- **Flask-Migrate**: Database migrations.
- **Flask-Smorest**: OpenAPI documentation; Serialization, deserialization and validation using `marshmallow` Schema
  under the hood.
- **Flask-JWT-Extended**: JWT-based authentication and authorization.
- **Flask-Redis**: In-memory database for JWT blacklisting.
- **PostgreSQL**: Database for file information and user storage.

**DevOps:**

- **Docker**: Containerization.
- **GitHub Actions** Automates the CI process by running tests in a Dockerized environment on every push to the main branch or pull request to it.

### Features

- **JWT Authentication:** Provides secure user access using JWT access and refresh tokens, with token blacklisting for
  enhanced security. Flow:
    - **Register:** Users submit their credentials (username and password), which are securely stored in the database (
      passwords are hashed).
    - **Login:** Users provide their credentials (username and password), and upon successful validation, they receive
      access and refresh tokens.
    - **Refresh:** For most requests, users include their access token. For refresh and logout endpoints, users must
      send their refresh token. If the access token expires, the refresh endpoint allows users to obtain new access and
      refresh tokens, while the old tokens are added to the blacklist in the Redis database.
    - **Logout:** Users provide their refresh token, which is added to the blacklist to prevent any further use.
- **Role-Based Access Control:**
    - **Admin:** Can perform CRUD operations on all entities (Users, Articles).
    - **Editor:** Can manage own articles, see all articles, and only update others articles.
    - **Viewer:** Can manage own articles and see all articles.
    - All roles can search for articles by title (partial matches are supported) using the `/articles/search` endpoint.

### Installation and Setup

**Prerequisites**

- Docker installed on your system.

**Steps**

1. Clone repository:

```
git clone git@github.com:bihunva/chi-articles-management-platform.git
```

2. Go to the project directory:

```
cd chi-articles-management-platform
```

3. Create a .env file from .env.example (the default values in .env.example are already configured, so no changes are
   needed):

```
cp .env.example .env
```

3. Build and run containers (add `-d` to run in detached mode):

```
docker compose up --build
```

**Optional (after containers are running):**

- Populate the database with initial data (3 users with different roles, and one article for each user) by running the
  following command:

```
docker exec -it flask-app /bin/bash -c "export PYTHONPATH=/app && poetry run python scripts/populate_db.py"
```

Credentials:
```
Admin: username = password = "admin"
Editor: username = password = "editor"
Viewer: username = password = "viewer"
```
    

- Run tests for all endpoints with this command:

```
docker exec -it flask-app /bin/bash -c "poetry run pytest"
```

**Documentation**:

- Access the OpenAPI documentation at: http://127.0.0.1:5000/docs
