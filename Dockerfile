FROM php:8.1-apache

# Install Python and pip
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install php extensions for MySQL
RUN docker-php-ext-install mysqli pdo_mysql

# Copy application code
COPY . /opt/forgecore

# Install Python requirements
RUN pip3 install --no-cache-dir -r /opt/forgecore/requirements.txt

# Link PHP frontend to Apache document root
RUN rm -rf /var/www/html && ln -s /opt/forgecore/forgecore/frontend /var/www/html

WORKDIR /opt/forgecore

# Default environment values; can be overridden in docker-compose
ENV DB_HOST=db
ENV DB_USER=forgecore
ENV DB_PASSWORD=forgecore
ENV DB_NAME=forgecore

# Expose Apache port
EXPOSE 80

CMD ["apache2-foreground"]
