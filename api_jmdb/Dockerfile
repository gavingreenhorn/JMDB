FROM python:3.7-slim

WORKDIR /app

COPY api_jmdb/requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./api_jmdb/ .

CMD ["gunicorn", "api_jmdb.wsgi:application", "--bind", "0:8000"]