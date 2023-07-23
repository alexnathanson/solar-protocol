FROM jedahan/solar-protocol-base:beta AS builder

COPY requirements.txt .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt

FROM jedahan/solar-protocol-base:beta
COPY --from=builder /root/.local /root/.local
COPY csv_datalogger.py .

CMD python csv_datalogger.py
