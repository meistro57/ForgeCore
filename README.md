# ForgeCore

ForgeCore is a modular steel fabrication management system intended to run on a LAMP stack with a MySQL backend. The backend logic is written in Python while the frontend will be composed of PHP/HTML/JS.

This repository provides a foundational scaffold with separate modules for common fabrication tasks such as drawing parsing and cutlist optimization. Each module contains a small CLI harness to test functionality directly.

## Layout

```
forgecore/
├── backend/                # Python modules for all fabrication tasks
│   ├── cutlist_optimizer/
│   ├── drawing_parser/
│   ├── inventory_manager/
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

## Getting Started

1. Set the following environment variables before running any module:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
2. Install Python dependencies (mysql-connector-python).
3. Import `database/schema.sql` into your MySQL server.
4. Run individual modules with `python3 backend/<module>/main.py` to test functionality.

This scaffold is intentionally simple and is meant to serve as a base for advanced extensions such as AI-assisted optimizations and a production-ready UI.
