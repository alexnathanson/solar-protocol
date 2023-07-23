FROM jedahan/solar-protocol-base:beta AS builder

COPY requirements.py .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt

FROM jedahan/solar-protocol-base:beta
COPY --from=builder /root/.local /root/.local
COPY api.py .

CMD python -m uvicorn api:app --proxy-headers --host 0.0.0.0 --port 80 --reload