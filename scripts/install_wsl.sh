#!/bin/bash
set -e

# Update package lists
sudo apt-get update

# Install Apache, MySQL, PHP, and phpMyAdmin
sudo apt-get install -y apache2 mysql-server php libapache2-mod-php php-mysql phpmyadmin

# Enable and start services
sudo systemctl enable apache2
sudo systemctl start apache2
sudo systemctl enable mysql
sudo systemctl start mysql

# Basic MySQL setup
DB_USER="forgecore"
DB_PASS="forgecore"
DB_NAME="forgecore"

sudo mysql <<MYSQL
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
MYSQL

# Link phpMyAdmin to Apache document root
if [ ! -e /var/www/html/phpmyadmin ]; then
    sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin
fi

echo "Installation complete. Access phpMyAdmin at http://localhost/phpmyadmin"
