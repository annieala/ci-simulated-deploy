FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make output unbuffered (important for container logs)
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "data_analysis.py"]