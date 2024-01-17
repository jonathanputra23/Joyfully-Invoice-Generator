from flask import Flask, render_template, request, send_file
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import sys
import webbrowser
from datetime import datetime  # Import the datetime module

app = Flask(__name__, template_folder='templates', static_folder='static')

# Get the current date
current_date = datetime.now().strftime("%d/%m/%Y")  # Format: DD/MM/YYYY

@app.route('/')
def index():
    return render_template('index.html')

# Function to get and update the invoice number
def get_and_update_invoice_number():
    invoice_number_file = 'invoice_number.txt'

    # Check if the file exists
    if not os.path.exists(invoice_number_file):
        with open(invoice_number_file, 'w') as file:
            file.write('1')  # Initialize with 1 if the file doesn't exist

    # Read the current invoice number
    with open(invoice_number_file, 'r') as file:
        current_invoice_number = int(file.read())

    # Increment the invoice number
    next_invoice_number = current_invoice_number + 1

    # Update the file with the next invoice number
    with open(invoice_number_file, 'w') as file:
        file.write(str(next_invoice_number))

    return current_invoice_number
def open_browser():
    # Open the default web browser with the Flask app URL
    webbrowser.open('http://127.0.0.1:5000/')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # Get form data
    client_name = request.form.get('client_name')
    invoice_number = get_and_update_invoice_number()
    # Extract items, quantities, prices, and subtotals from the form data
    items = request.form.getlist('item[]')
    quantities = [int(quantity) for quantity in request.form.getlist('quantity[]')]
    prices = [float(price) for price in request.form.getlist('price[]')]
    subtotals = [float(subtotal) for subtotal in request.form.getlist('subtotal[]')]
    
    # Validate that items, quantities, prices, and subtotals have the same length
    if len(items) != len(quantities) != len(prices) != len(subtotals):
        return "Error: Each item must have corresponding quantity, price, and subtotal."

    # Generate PDF invoice
    pdf = FPDF()
    pdf.add_page()

    # Add background image
    background_image_path = 'background/polos.jpg'  # Replace with the actual path to your image
    pdf.image(background_image_path, x=0, y=0, w=210, h=297)  # Adjust width (w) and height (h) as needed
    
    pdf.ln(45)
    # Set font style and size for the title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(50, 10, txt=current_date, border=0)  # Replace with the actual date
    pdf.cell(100, 10, txt=client_name, border=0, align='C')
    pdf.cell(50, 10, txt="      " + str(invoice_number), border=0, align='L')
    pdf.ln(30)

    # Add itemized list and calculate total
    total = 0
    items_on_page = 0  # Counter for items on the current page

    for item, quantity, price, subtotal in zip(items, quantities, prices, subtotals):
        # Check if there's enough space on the current page
        if pdf.get_y() > 240 or items_on_page >= 6:
            pdf.add_page()  # Start a new page
            pdf.image(background_image_path, x=0, y=0, w=210, h=297)  # Add background to the new page

            # Replicate the header information on the new page
            pdf.ln(45)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(50, 10, txt=current_date, border=0)  # Replace with the actual date
            pdf.cell(100, 10, txt=client_name, border=0, align='C')
            pdf.cell(50, 10, txt="      " + str(invoice_number), border=0, align='L')
            pdf.ln(30)

            items_on_page = 0  # Reset the counter for items on the new page
        
        # Set font style and size for the itemized list
        pdf.set_font("Arial", 'B', 12)

        pdf.set_x(20)
        pdf.cell(45, 10, txt=item, border=0, align='L')
        pdf.cell(75, 10, txt=f"x{quantity}", border=0, align='C')
        pdf.cell(50, 10, txt=f"@{price:.2f}\nSubtotal: Rp {subtotal:.2f}", border=0, align='L')
        pdf.ln(15)

        total += subtotal
        items_on_page += 1  # Increment the counter for items on the current page

    # Set font style and size for the itemized list
    pdf.set_font("Arial", 'B', 20)
    pdf.set_x(40)
    pdf.cell(110, 10, txt="Total", border=0, align='L')
    pdf.cell(30, 10, txt=f"@{total:.2f}", border=0, align='R', ln=True)

    # Save PDF to the static/invoices folder
    pdf_output_path = f"static/invoices/invoice_{client_name}.pdf"
    pdf.output(pdf_output_path)

    # Determine the user's download folder
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # Construct the path for the destination file in the download folder
    destination_path = os.path.join(download_folder, f"invoice_{client_name}.pdf")

    # Copy the generated PDF file to the user's download folder
    shutil.copy(pdf_output_path, destination_path)

    # Open the generated PDF file with the default PDF viewer
    webbrowser.open(destination_path)

    return "Invoice generated and saved to the Downloads folder."

if __name__ == '__main__':
    # Open the default web browser with the Flask app URL only once
    open_browser()

    # Run the Flask app
    app.run(debug=False)