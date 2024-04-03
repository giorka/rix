FROM python:3.8

WORKDIR /web
COPY . /web

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install gunicorn
RUN pip install -r requirements.txt
RUN python manage.py migrate
