# FileOrganizer

A Python Flask-based application to scan, log, and organize files on your system with a user-friendly web interface.

## Features

- Scan files and folders on specified drives or directories
- Log and track file metadata and changes
- Interactive web UI for viewing and managing scanned files
- Modular Python scripts for scanning, logging, and serving the web app

## Project Structure

- `app.py`: Main Flask application handling routes and web UI
- `file_scanner.py`: Script responsible for scanning files on disk
- `scan_logger.py`: Handles logging of scan results and file metadata
- `templates/`: HTML templates for Flask frontend
- `static/`: CSS, JS, and other static assets
- `.gitignore`: Specifies files and folders to exclude from Git tracking

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Flask (and other dependencies in `requirements.txt` if available)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mghpt/FileOrganizer.git
   cd FileOrganizer
