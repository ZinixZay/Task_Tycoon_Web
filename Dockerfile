FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt && pip install psycopg2-binary
EXPOSE 8000
COPY task_tycoon ./
RUN ["python", "manage.py", "runserver", "0.0.0.0:8000"]