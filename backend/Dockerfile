# Start from a small Linux image with Python 3.12
FROM python:3.12-slim

# Print logs immediately and don't create .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# GDAL, GEOS and PROJ: the mapping libraries GeoDjango needs
RUN apt-get update \
    && apt-get install -y --no-install-recommends gdal-bin libgdal-dev binutils libproj-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages first (Docker caches this step, so rebuilds are fast)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the code
COPY . .

EXPOSE 8000

# Apply migrations, then start the development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]