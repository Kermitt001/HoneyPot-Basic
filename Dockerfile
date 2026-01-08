FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate a host key if not present (will be done by server.py or manually)
# But for safety, we can pre-generate one or let the app do it.
# The app does it.

EXPOSE 2222

CMD ["python", "honeypot/server.py"]
