FROM python:3.10-slim

# Install system dependencies for CairoSVG
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2-dev \
    libpango1.0-dev \
    libffi-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Set up work directory
WORKDIR /app

# Copy pyproject.toml and install dependencies
COPY pyproject.toml README.md ./
COPY svg_to_pdf ./svg_to_pdf

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Set the workdir to /work when the container runs
WORKDIR /work

# Define entrypoint
ENTRYPOINT ["python", "-m", "svg_to_pdf.converter"]