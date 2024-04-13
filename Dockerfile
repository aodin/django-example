# syntax=docker/dockerfile:1

FROM python:3.11.9-bookworm

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "django_example.wsgi:application", "--workers", "2", "--threads", "2", "--max-requests", "5000", "--max-requests-jitter", "100", "--worker-tmp-dir", "/dev/shm", "--log-file=-", "--timeout", "15"]
