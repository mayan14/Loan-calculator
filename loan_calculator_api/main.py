from datetime import datetime

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
app = Flask(__name__)

# CORS used by flask to allow access to these resources
CORS(app, resources={
    r"/calculate-loan": {"origins": "http://127.0.0.1:5500"},
    r"/download-pdf": {"origins": "http://127.0.0.1:5500"}
})

# Constants for bank rates and fees
BANK_RATES = {
    "Bank A": {"Flat Rate": 0.20, "Reducing Balance": 0.22},
    "Bank B": {"Flat Rate": 0.18, "Reducing Balance": 0.25}
}
# Constants for all the 2 banks
PROCESSING_FEES_PERCENTAGE = 0.03
EXCISE_DUTY_PERCENTAGE = 0.20
LEGAL_FEES = 10000


# Function to calculate the total interest
def calculate_interest(principal, rate, time, interest_type):
    if interest_type == "Flat Rate":
        return principal * rate * time
    elif interest_type == "Reducing Balance":
        #  interest is calculated on the remaining loan balance after each payment,
        #  so the interest amount decreases over time as the principal is gradually paid down.
        return principal * rate * (1 - (1 + rate) ** (-time)) / (1 - (1 + rate))


# Function to validate the date format
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False


# API route for calculating loan details
@app.route('/calculate-loan', methods=['POST'])
def calculate_loan():
    # Get loan data in json
    data = request.get_json()
    try:
        amount = float(data['amount'])  # Convert amount to float
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    frequency = data['frequency']
    period = data['period']
    start_date = data['start_date']
    interest_type = data['interest_type']
    bank = data['bank']

    processing_fees = amount * PROCESSING_FEES_PERCENTAGE
    excise_duty = processing_fees * EXCISE_DUTY_PERCENTAGE

    if frequency == "Annually":
        time = period
    elif frequency == "Quarterly":
        time = period * 4
    elif frequency == "Monthly":
        time = period * 12
    elif frequency == "Every 6 Months":
        time = period * 2
    else:
        return jsonify({"error": "Invalid payment frequency"}), 400

    if bank in BANK_RATES:
        bank_rates = BANK_RATES[bank]
        if interest_type in bank_rates:
            interest_rate = bank_rates[interest_type]
        else:
            return jsonify({"error": "Invalid interest type for the selected bank"}), 400
    else:
        return jsonify({"error": "Invalid bank selection"}), 400

    if not validate_date(start_date):
        return jsonify({"error": "Invalid date format. Use dd/mm/yyyy."}), 400

    total_interest = calculate_interest(amount, interest_rate, time, interest_type)

    # total_fees is the additional costs you incur when obtaining the loan, beyond the principal amount and interest.
    total_fees = processing_fees + excise_duty + LEGAL_FEES

    # total_cost is the comprehensive view of the overall financial impact of the loan
    total_cost = amount + total_interest + total_fees

    result = {
        "Amount to borrow": amount,
        "Payment frequency": frequency,
        "Loan period in years": period,
        "Start date": start_date,
        "Interest Type": interest_type,
        "Bank": bank,
        "Total Fees": total_fees,
        "Total Interest": total_interest,
        "Total Cost": total_cost
    }

    # To Generate and save the PDF uncomment below line
    generate_and_save_pdf(result, bank)

    return jsonify(result)


def generate_and_save_pdf(data, bank):
    pdf_file = "loan_computation.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []

    # Create a table for the loan details 2D list
    data = [
        ["Loan Details", "Values"],
        ["Amount to borrow", data["Amount to borrow"]],
        ["Payment frequency", data["Payment frequency"]],
        ["Loan period in years", data["Loan period in years"]],
        ["Start date", data["Start date"]],
        ["Interest Type", data["Interest Type"]],
        ["Bank", data["Bank"]],
        ["Total Fees", data["Total Fees"]],
        ["Total Interest", data["Total Interest"]],
        ["Total Cost", data["Total Cost"]],
    ]
    styles = getSampleStyleSheet()
    elements.append(Paragraph(datetime.now().strftime('%Y-%m-%d'), styles['Normal']))
    elements.append(Paragraph(bank, styles['Normal']))

    t = Table(data, colWidths=[200, 200], rowHeights=30)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
    ]))
    elements.append(t)

    doc.build(elements)


@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    pdf_file = "loan_computation.pdf"
    response = send_file(pdf_file, as_attachment=True)

    response.headers['Content-Disposition'] = f'attachment; filename={pdf_file}'
    # Add headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


if __name__ == '__main__':
    app.run(debug=True)
