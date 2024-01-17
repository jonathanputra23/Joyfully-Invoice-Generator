# Joyfully Invoice Generator

This is a simple Invoice Generator using Python, Flask, PyInstaller, and FPDF.

## Features

- **Generate Invoices:** Create professional invoices with a customizable layout.
- **Automatic Invoice Numbering:** The system automatically increments the invoice number for each generated invoice.
- **Itemized List:** Include a detailed itemized list with quantities, prices, and subtotals.
- **Total Calculation:** The system calculates the total amount based on the itemized list.
- **Background Image:** Customize the invoice with an A4 background image.
- **Pagination:** Automatically create new pages if the itemized list exceeds a specified limit.
- **Date Stamping:** Stamp the current date on the invoice.
- **Download PDF:** Download the generated invoice as a PDF file.
- **Cross-Platform Execution:** Use PyInstaller to create standalone executables for both Windows and macOS.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Building Executable](#building-executable)

## Installation

To run this project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/jonathanputra23/Joyfully-Invoice-Generator.git

# Navigate to the project directory
cd invoice-generator

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

## Usage

To use the Invoice Generator, run the Flask app:

```bash
# Run the Flask app
python app.py
```

Open your web browser and visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Building Executable

To build an executable using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Navigate to the project directory
cd invoice-generator

# Generate the executable
python -m PyInstaller --onefile --add-data "templates;templates" --add-data "background;background" --add-data "invoice_number.txt;." app.py
```