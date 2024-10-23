FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic

COPY . /app/
