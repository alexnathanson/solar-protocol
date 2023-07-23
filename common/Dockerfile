FROM docker.io/library/python:3.11-slim AS builder
RUN apt-get --quiet update && apt-get --quiet upgrade --yes

COPY . .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt
RUN pip install --user .

FROM docker.io/library/python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
