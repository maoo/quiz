FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    inkscape \
    librsvg2-bin \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY tests ./tests

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Set entrypoint
ENTRYPOINT ["python", "-m"] 