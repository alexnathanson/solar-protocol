FROM docker.io/library/python:3.11-slim AS builder
ENV TERM=screen-256color

WORKDIR /common
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --quiet --no-cache-dir --requirement requirements.txt

FROM docker.io/library/python:3.11-slim
ENV TERM=screen-256color
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /common
COPY . .
