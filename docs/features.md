# ForgeCore Feature Overview

This document summarizes the capabilities provided by the modules in this repository.

## Core Modules

### Inventory Manager
Manages raw stock lengths, logs cuts and can assign material to jobs. It exposes a CLI for listing materials, adding new stock, cutting pieces and tracking overall remaining length.

### CSV Importer
Allows bulk creation of inventory records from comma separated value files. Intended for rapid onboarding of existing stock catalogs.

### Customer Manager
Stores customer contact information. New customers can be added and listed through a simple command line interface.

### Drawing Parser
Example drawing parser that demonstrates how CAD files might be scanned to populate part information. The current implementation logs the drawing file and records a single example part length.

### Drawing Submittal Logger
Keeps a record of drawing submittals including who submitted them and their status. Useful for tracking the review process of shop drawings.

### Cutlist Optimizer
Loads required parts and available materials from the database and pairs them together to minimize waste.

### Job Tracker
Lists active jobs stored in the database. Additional job management functionality can be built on top of this module.

### Label Printer
Placeholder utility that shows where barcode or part labels could be generated from the command line.

### Report Engine
Provides a starting point for reporting on jobs and materials. The example method prints a simple job summary.

### Visual Debugger
Command line visualization helper that prints a concise summary of jobs in the database.

### Agent API
Internal API example that returns drawing information. This is meant as a hook for future AI integrations or remote tools.

## Frontend
The `frontend` directory contains demonstration PHP forms such as a basic customer entry page. It is not intended to be production ready but shows how the backend can be accessed via web requests.

## Database
`forgecore/database/schema.sql` defines tables for jobs, materials, cut parts, drawings, customers and drawing submittals. The structure is deliberately minimal so new tables can be added easily.

## Future Work
The project is a scaffold for larger fabrication management systems. Potential extensions include quoting tools, automated scheduling, real label printing, refined security controls and a modern web UI.
