FROM python:3.12.1 as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12.1-slim
WORKDIR /work/docker-builds/na_hruk_bot

COPY --from=builder /root/.local /root/.local
COPY ./ .

ENV PATH=/root/.local:$PATH

RUN python ./main.py