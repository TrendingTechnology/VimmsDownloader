FROM python:3.9-slim-buster
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install yapf