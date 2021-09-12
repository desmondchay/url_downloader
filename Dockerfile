FROM python:3.9.7-slim-buster

WORKDIR /app

COPY . /app/

# Install dependencies
RUN pip3 install -r requirements.txt