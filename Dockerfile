# image de base volontairement ancienne, pour que Trivy ait des failles a trouver
FROM python:3.6-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
