#!/bin/bash
set -euo pipefail

# ForgeCore installation script
# Installs Python requirements and initializes MySQL database

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

DB_USER="${DB_USER:-forgecore}"
DB_PASSWORD="${DB_PASSWORD:-forgecore}"
DB_NAME="${DB_NAME:-forgecore}"
DB_HOST="${DB_HOST:-localhost}"
MYSQL_ROOT_USER="${MYSQL_ROOT_USER:-root}"
MYSQL_ROOT_PASS="${MYSQL_ROOT_PASS:-}"

echo "[1/3] Installing Python packages"
pip3 install --user -r "$ROOT_DIR/requirements.txt"

if ! command -v mysql >/dev/null; then
    echo "MySQL client not found. Please install MySQL server and rerun." >&2
    exit 1
fi

echo "[2/3] Configuring MySQL database"
mysql -u "$MYSQL_ROOT_USER" ${MYSQL_ROOT_PASS:+-p"$MYSQL_ROOT_PASS"} <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL

mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$ROOT_DIR/forgecore/database/schema.sql"

echo "[3/3] Setup complete"
cat <<EOM

Add the following to your shell profile (~/.bashrc or similar):
export DB_HOST=$DB_HOST
export DB_USER=$DB_USER
export DB_PASSWORD=$DB_PASSWORD
export DB_NAME=$DB_NAME
EOM

