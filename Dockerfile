# 1. Base Image
FROM python:3.12-slim

# 2. Environment variables to optimize Python for Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=2.0.1

# 3. Set the working directory
WORKDIR /app

# 4. Install system dependencies (curl for healthchecks)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 5. Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# 6. Configure Poetry: Don't create a virtualenv inside the container
RUN poetry config virtualenvs.create false

# 7. Copy only dependency files first (Leverage Docker Cache)
COPY pyproject.toml poetry.lock* /app/

# 8. Install dependencies
# --no-root means don't install the project itself yet, just dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# 9. Copy the rest of the application code
COPY . /app

# 10. Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]