# Modular Steel Inventory Management System – Detailed Design Plan

## Overview
This document outlines the architecture and feature set for a modular steel inventory management system developed with PHP, MySQL, and Apache. The system is intended for steel fabrication shops handling both standard AISC shapes and custom profiles. It supports inventory tracking, CSV imports, real-time stock updates, role-based permissions, and is structured for future expansion into quoting, cut tracking, and ERP integration.

## Core Features
- **Inventory Tracking** – Tracks standard and custom steel shapes in lengths of 20–60 ft (5 ft increments), using inches internally.
- **CSV Import** – Admins can bulk import inventory using CSVs.
- **Live Stock Status** – Real-time view of available and reserved stock.
- **Stock Reservation** – Allows authorized users to reserve stock, locking it from general use.
- **Role-Based Security** – Admins, Estimators, and Viewers have tiered access.
- **Modular System** – Built for extendibility into quotes, cuts, and scheduling.

## Database Schema
- **Users:** `user_id`, `username`, `password_hash`, `role`, `name`, `email`
- **Roles (optional):** `role_id`, `role_name`, `permissions`
- **SteelShapes:** `shape_id`, `designation`, `type`, `material`
- **Inventory:** `inventory_id`, `shape_id`, `length_in`, `quantity_total`, `quantity_reserved` (UNIQUE `shape_id` + `length_in`)
- **Reservations:** `reservation_id`, `shape_id`, `length_in`, `quantity`, `reserved_by`, `reserved_at`, `status`

## Module Architecture (MVC-inspired)
- **Config Module:** `config.php` with DB credentials, allowed lengths, constants.
- **Database Access Layer:** PDO/MySQLi, reusable CRUD functions.
- **Auth Module:** Login, logout, session validation, role checking.
- **User Management:** Admin tools to manage accounts/roles.
- **Inventory Module:**
  - Shapes Controller: Add/edit AISC/custom shapes
  - Inventory Controller: List, search, add, update stock
- **Reservation Module:** Atomic reserve/release transactions
- **CSV Module:** Upload & parse CSV, validate, update DB, show results
- **Views/UI:** Modular templates, navigation, form/action pages, AJAX updates

## UI/UX
- **Design:**
  - High-contrast, large fonts, bold key values
  - Fixed nav (sidebar or topbar), page breadcrumbs
  - Responsive desktop-first layout with optional mobile fallback
- **Pages:**
  - Login
  - Dashboard (quick stats, alerts)
  - Inventory (search, filter, reserve, admin edits)
  - Shapes (admin only)
  - CSV Import (admin only, summary of result)
  - Reservations (admin view, user-specific view)
  - User Management (admin only)
- **Behavioral Elements:**
  - Sorting, tooltips, confirm dialogs
  - Color-coded status rows
  - Auto-refresh or push-updates
  - Printable summaries

## Processes
### Reservation Flow
1. User selects item and enters quantity.
2. System checks availability and performs a transactional insert into Reservations and Inventory updates.
3. UI confirms the reservation.

### CSV Import
1. Admin uploads a CSV file.
2. File is parsed line-by-line and shapes are matched or created.
3. Inventory is updated accordingly and an import report is shown.

## Security & Integrity
- All inputs sanitized
- Passwords hashed (e.g., bcrypt)
- Server-side role checks enforced
- Transactions used for all inventory updates
- Regular DB backups recommended

## Future-Ready Extensions
- Quotes module: reserve stock via quoting
- Cut Logs: track remaining lengths/remnants
- ERP Integration: import/export material needs
- API layer: expose inventory for other tools

