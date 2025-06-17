# ForgeCore

ForgeCore is a modular steel fabrication management system intended to run on a LAMP stack with a MySQL backend. The backend logic is written in Python while the frontend will be composed of PHP, HTML and JavaScript.

This repository provides a foundational scaffold with separate modules for common fabrication tasks such as drawing parsing and cutlist optimization. Each module contains a small CLI harness to test functionality directly.

## Layout

```
forgecore/
├── backend/                # Python modules for all fabrication tasks
│   ├── cutlist_optimizer/
│   ├── drawing_parser/
│   ├── inventory_manager/
│   ├── csv_importer/
│   ├── job_tracker/
│   ├── visual_debugger/
│   ├── label_printer/
│   ├── report_engine/
│   └── agent_api/
├── frontend/               # Placeholder for future PHP interface
│   ├── index.php
│   ├── dashboard/
│   └── mobile_kiosk/
├── database/
│   └── schema.sql          # MySQL schema
├── config/
│   └── config.py           # Database connection helpers
└── README.md
```

## Requirements

- Python 3.8 or newer
- MySQL server with access credentials
- Python packages listed in `requirements.txt`

## WSL Installation
For a fresh Ubuntu WSL environment you can install Apache, MySQL, PHP and phpMyAdmin with:
```bash
./scripts/install_wsl.sh
```
This script also creates the `forgecore` database and user and links phpMyAdmin under `/phpmyadmin`.
After installation load the database schema with:
```bash
php scripts/setup_database.php
```


## Getting Started

1. Set the following environment variables before running any module:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Import `database/schema.sql` into your MySQL server and ensure it is running.
4. Run individual modules with `python3 backend/<module>/main.py` to test functionality.
   For example, the inventory manager exposes a small CLI:
   ```bash
   python3 backend/inventory_manager/main.py list
   # cut 40 inches from material id 1 and record the part
   python3 backend/inventory_manager/main.py cut 1 40
   ```
   You can also bulk add materials using the CSV importer:
   ```bash
   python3 backend/csv_importer/main.py inventory.csv
   ```

This scaffold is intentionally simple and is meant to serve as a base for advanced extensions such as AI-assisted optimizations and a production-ready UI.
