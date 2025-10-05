FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy CSV files first (explicit)
COPY All_Diets.csv ./
COPY *.csv ./

# Copy Python scripts
COPY *.py ./

# Copy everything else
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "data_analysis.py"]