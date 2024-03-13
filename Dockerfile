FROM python:3.9-slim as builder
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]