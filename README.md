# Movie Rating System (Back-End)

This project is a high-performance, asynchronous back-end system for managing a collection of movies, directors, and user ratings. Built with a focus on modern software engineering principles, it demonstrates a robust layered architecture, automated database migrations, and a fully containerized development environment.

The system comes pre-populated with real-world data, including 1,000 movies and metadata from the TMDB 5000 dataset, providing a realistic environment for testing and development.

## Key Features

- **Asynchronous RESTful API:** Built with **FastAPI** using `async/await` for non-blocking I/O operations.
- **Advanced Data Seeding:** Includes a custom ETL script to import 1,000 real movies, directors, and genres from the TMDB dataset.
- **Layered Architecture:** Strict separation of concerns across **Controllers** (API), **Services** (Business Logic), and **Repositories** (Data Access/CRUD).
- **Relational Complexity:** Manages One-to-Many (Director-Movie) and Many-to-Many (Movie-Genre) relationships.
- **Containerized Environment:** Fully orchestrated using **Docker** and **Docker Compose** for consistent execution across any OS.
- **Asynchronous ORM:** Leverages **SQLAlchemy 2.0** with the modern **Psycopg 3** driver for efficient PostgreSQL interactions.
- **Data Integrity & Validation:** Automated request/response validation using **Pydantic** and schema versioning via **Alembic**.

## Technologies Used

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Web Server:** Uvicorn (ASGI)
- **Database:** PostgreSQL 15+
- **ORM:** SQLAlchemy 2.0 (Async)
- **DB Driver:** Psycopg 3
- **Migrations:** Alembic
- **Dependency Management:** Poetry 2.0
- **Containerization:** Docker & Docker Compose

## How to Run

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Git](https://git-scm.com/) installed.

### 1. Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SadraaF/movie-rating-system.git
   cd movie-rating-system
   ```

2. **Configure Environment:**
   Create a `.env` file from the example. The application inside the Docker container is configured to use the database service name `db`.
   ```bash
   cp .env.example .env
   ```

### 2. Running with Docker

The entire stack (API and Database) is managed by Docker Compose.

1. **Build and start the containers:**
   ```bash
   docker compose up --build -d
   ```

2. **Apply Database Migrations:**
   Run Alembic inside the application container to create the table structures.
   ```bash
   docker compose exec app alembic upgrade head
   ```

3. **Seed the Database (Optional but Recommended):**
   To populate the system with 1,000 movies from the TMDB dataset:
   ```bash
   # Copy data files into the database container
   docker cp scripts/. movie_rating_db:/tmp/

   # Run the seeding script
   docker exec -it -w /tmp movie_rating_db psql -U movieuser -d moviedb -f /tmp/seeddb.sql
   ```

### 3. Accessing the API

Once the containers are running:
- **Interactive Documentation (Swagger UI):** Navigate to [http://localhost:8000/docs](http://localhost:8000/docs).
- **Alternative Documentation (ReDoc):** Navigate to [http://localhost:8000/redoc](http://localhost:8000/redoc).

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/v1/movies` | List movies with pagination and filters (title, year, genre). |
| **GET** | `/api/v1/movies/{id}` | Detailed view of a movie, including average rating and cast. |
| **POST** | `/api/v1/movies` | Add a new movie (requires valid director/genre IDs). |
| **PUT** | `/api/v1/movies/{id}` | Update movie info and synchronize genre relationships. |
| **DELETE**| `/api/v1/movies/{id}` | Remove a movie and cascade-delete its ratings. |
| **POST** | `/api/v1/movies/{id}/ratings` | Register a rating (1-10) for a specific movie. |

## Project Architecture

The project follows the architectural principles defined in the `project_bible.txt`:

- `app/api/`: Presentation layer (Controllers, Pydantic Schemas, and Router).
- `app/services/`: Business Logic layer (Orchestrates data flow and calculations).
- `app/repositories/`: Data Access layer (Direct SQLAlchemy queries).
- `app/models/`: SQLAlchemy ORM definitions and relationships.
- `app/db/`: Connection management and Async session factory.
- `app/exceptions/`: Custom application-specific error hierarchy.
- `alembic/`: Database version control and migration history.
- `scripts/`: SQL and Python scripts for database seeding and verification.
