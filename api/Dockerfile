FROM solar-protocol/base AS builder

COPY requirements.txt .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt

FROM solar-protocol/base
COPY api.py .
COPY --from=builder /root/.local /root/.local

CMD python -m uvicorn api:app --proxy-headers --host 0.0.0.0 --port 80 --reload