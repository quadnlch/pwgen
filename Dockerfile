FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5069
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:5069", "app:app_asgi"]
