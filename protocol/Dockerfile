FROM jedahan/solar-protocol-base:beta AS builder

RUN apt-get --quiet install \
  build-essential \
  libffi-dev \
  libjpeg-dev \
  zlib1g-dev --yes

COPY requirements.txt .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt

FROM jedahan/solar-protocol-base:beta AS builder
COPY . .

FROM jedahan/solar-protocol-base:beta
COPY --from=builder /root/.local /root/.local
COPY api.py .

CMD python -m uvicorn api:app --proxy-headers --host 0.0.0.0 --port 80 --reload