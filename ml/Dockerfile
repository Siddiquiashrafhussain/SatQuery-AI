FROM python:3.11-slim

# Install system dependencies for rasterio and basic tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdal-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model to cache it in the image (optional but good for speed)
# We can do this in app.py or a prep script.

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
