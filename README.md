# Document Extraction System

## Overview

This project is an offline document extraction system built with FastAPI.

It supports:

- PDF
- Scanned PDF
- JPG / PNG
- XLS / XLSX

The system extracts purchase order information and stores structured data in MSSQL.

---

## Features

- File upload API
- Automatic file type detection
- PDF text extraction
- OCR for scanned PDFs and images
- Excel multi-sheet parsing
- Purchase order data extraction
- MSSQL storage
- Status tracking
- Export to JSON / CSV / Excel
- Logging
- Offline deployment support

---

## Tech Stack

Backend:
- FastAPI

Database:
- MSSQL
- SQLAlchemy
- pyodbc

OCR:
- Tesseract OCR

Document Processing:
- PyMuPDF
- pdfplumber
- Pillow


Excel:
- pandas
- openpyxl

Logging:
- loguru

---

## Project Structure

app/
    router/
    service/
    utils/

uploads/
exports/
logs/

---

## API Endpoints

### Upload

POST /upload

Upload:
- PDF
- PNG
- JPG
- XLSX

---

### Status

GET /status/{document_id}

Returns:
- PENDING
- PROCESSING
- COMPLETED
- FAILED

---

### Export JSON

GET /export/json/{document_id}

---

### Export CSV

GET /export/csv/{document_id}

---

### Export Excel

GET /export/excel/{document_id}

---

## Installation

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn app.main:app --reload

Swagger:

http://127.0.0.1:8000/docs
