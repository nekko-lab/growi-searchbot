FROM python:3.12.13-bookworm

WORKDIR /app 
COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y 
RUN pip install -r requirements.txt