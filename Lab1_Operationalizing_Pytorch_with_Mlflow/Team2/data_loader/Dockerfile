FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN DEBIAN_FRONTEND=noninteractive && \
    pip install -U --no-cache-dir -r requirements.txt

COPY kaggle_creds/kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

RUN mkdir /project
WORKDIR /project
COPY . .
