FROM python:3.12-slim AS base

# Install Poetry (the project's dependency manager)
RUN pip install --no-cache-dir poetry==2.4.1

# Poetry should install dependencies into the system environment inside
# the container -- there's no need for a separate virtualenv when the
# whole container already IS the isolated environment.
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Copy only dependency-related files first. Docker caches each step: as
# long as these two files don't change, dependency installation is
# skipped on subsequent builds, making rebuilds much faster.
COPY pyproject.toml poetry.lock ./

# Install only production dependencies (skip dev tools like ruff, mypy,
# pytest -- not needed to run the application itself).
RUN poetry install --no-root --only main


COPY bridgeit ./bridgeit

# The port Uvicorn will listen on inside the container.
EXPOSE 8000

CMD ["uvicorn", "bridgeit.adapters.api.main:app", "--host", "0.0.0.0", "--port", "8000"]