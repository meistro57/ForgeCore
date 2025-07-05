# ForgeCore

ForgeCore is a modular steel fabrication management scaffold. It ships with a collection of Python CLI tools and a minimal PHP front end to demonstrate how each component interacts with a shared MySQL database.

The goal of the project is to provide a simple starting point for shops that want to track jobs, inventory and drawings while leaving plenty of room for custom extensions.

## Features
- Job, customer and drawing tracking
- Inventory management with cut logging
- CSV imports for bulk data entry
- Basic cut list optimization
- Simple reporting and visual debugging tools
- Placeholder API for future AI agents

A detailed list of modules and capabilities can be found in [docs/features.md](docs/features.md).

## Repository Layout
```text
forgecore/
├── backend/                # Python modules
│   ├── agent_api/
│   ├── csv_importer/
│   ├── customer_manager/
│   ├── cutlist_optimizer/
│   ├── drawing_parser/
│   ├── drawing_submittal_logger/
│   ├── inventory_manager/
│   ├── job_tracker/
│   ├── label_printer/
│   ├── report_engine/
│   └── visual_debugger/
├── config/                 # Database connection helpers
├── database/               # MySQL schema
├── frontend/               # Example PHP forms
└── scripts/                # Setup utilities
```

## Requirements
- Python 3.8+
- MySQL server
- Packages listed in `requirements.txt`

## Quick Start
1. Execute the install script which installs the Python requirements and
   initializes a local MySQL database:
   ```bash
   ./scripts/install.sh
   ```
   The script prints the database credentials it configured. Export these
   values so the backend modules can locate the database:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
2. Run a module to verify connectivity, for example:
   ```bash
   python3 forgecore/backend/inventory_manager/main.py list
   ```

For a turnkey Windows Subsystem for Linux setup see `scripts/install_wsl.sh`.

## Docker
To run the entire stack in containers, install Docker and execute:
```bash
docker-compose up -d
```
This starts the application, MySQL and phpMyAdmin. The default database credentials are:
- Host: `db`
- User: `forgecore`
- Password: `forgecore`
- Database: `forgecore`
phpMyAdmin is available on port 8080 and the PHP frontend on port 8000.


## License
This repository is released under the MIT license.
