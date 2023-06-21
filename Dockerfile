FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONPATH .

CMD ["gunicorn", "crm_api.wsgi:application", "--bind", "0:8000", "--workers", "3", "--reload"]

EXPOSE 8000