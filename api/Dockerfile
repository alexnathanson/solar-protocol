FROM localhost/solar-protocol/base:beta AS builder
RUN apt-get --quiet update && apt-get --quiet upgrade --yes

WORKDIR /api
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --quiet --no-cache-dir --requirement requirements.txt
RUN pip install --quiet --no-cache-dir /common

FROM localhost/solar-protocol/base:beta
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /api
COPY . .

CMD python -m uvicorn api:app --proxy-headers --host 0.0.0.0 --port 80 --reload
