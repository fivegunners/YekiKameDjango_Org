# Base image
FROM python:3.10-slim

# Ensure sources.list exists and switch to a reliable mirror
RUN echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat \
    libpq-dev \
    gcc \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Add and configure wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy project files
COPY . /app/

# Collect static files if necessary (uncomment if Django project)
# RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Set default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
