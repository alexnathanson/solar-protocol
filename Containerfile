## we have to use linux/amd64 for aarm64 macs, because python-skia will not make wheels 
## see https://github.com/kyamagu/skia-python/issues/173#issuecomment-1136571578
#FROM --platform=linux/amd64 python:3.10
FROM python:3.10
ENV TERM xterm-256color

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir --requirement requirements.txt
