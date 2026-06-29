FROM php:8.3-apache

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libgl1 \
    libglib2.0-0 \
    libgles2 \
    libegl1 \
    && docker-php-ext-install pdo pdo_mysql

COPY python/requirements.txt /tmp/requirements.txt

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

WORKDIR /var/www/html