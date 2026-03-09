FROM python:3.11-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY unfollow.py .

# Set entrypoint
ENTRYPOINT ["python", "unfollow.py"]
