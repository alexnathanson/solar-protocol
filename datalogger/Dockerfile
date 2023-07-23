FROM solar-protocol/base AS builder

COPY requirements.txt .
RUN pip install --user --quiet --no-cache-dir --requirement requirements.txt

FROM solar-protocol/base
COPY --from=builder /root/.local /root/.local
COPY csv_datalogger.py .

CMD python csv_datalogger.py
