# Python 'local' stage
FROM python:3.11-slim-bullseye as python

# 1. Force Python stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS requirements
RUN apt-get update && apt-get install --no-install-recommends -y git curl postgresql-client gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
WORKDIR /root
RUN curl -sSL https://install.python-poetry.org/ | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Install the project requirements.
RUN poetry config virtualenvs.create false
WORKDIR /app
COPY poetry.lock pyproject.toml ./
COPY ./app ./
RUN PIP_NO_CACHE_DIR=false poetry install

# Port used by this container to serve HTTP.
EXPOSE 8000

# Serve Local
CMD ["python", "main.py"]