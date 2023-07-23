FROM jedahan/solar-protocol-base:beta AS builder

COPY requirements.txt .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt

FROM jedahan/solar-protocol-base:beta
COPY api.py .
COPY --from=builder /root/.local /root/.local

CMD python -m uvicorn api:app --proxy-headers --host 0.0.0.0 --port 80 --reload