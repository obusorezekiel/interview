FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY csv_processor.py .
COPY requirements.txt .
COPY .env .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python3", "csv_processor.py"]
