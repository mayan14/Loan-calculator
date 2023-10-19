# Loan Calculator Web Application
This full-stack web application is designed to help users calculate loan instalments using either Flat Rate or Reducing Balance interest computation methods. It also allows users to compare loan rates offered by two financial institutions, Bank A and Bank B. The application provides a breakdown of charges, such as processing fees, excise duty, and legal fees, and displays the take-home amount for the user. In addition, users can download instalments as a PDF file. The API is also available for external parties to access this functionality.

# Requirements
To run this project, make sure you have the following components and libraries installed on your system:

* Python 3.10.7
* Flask~=3.0.0
* ReportLab~=4.0.6

# Project Structure
The project is divided into two parts: the frontend and the backend API.

1. Frontend: Located in the loan_calculator_frontend folder, it consists of HTML, jQuery, CSS, and JavaScript files that create the user interface for the loan calculator.

2. Backend API: Implemented using Flask, the backend is located in the loan_calculator_api folder. It provides the server-side processing for the loan calculations and handles requests from the frontend.

# Technologies Used
Frontend: HTML, jQuery, CSS, and JavaScript.
Backend: Flask (Python web framework).

# Running the Backend
To start the backend server, follow these steps:

1. Open your terminal.
2. Navigate to the 'loan_calculator_api' directory.
3. Ensure you have the required Python version and libraries installed.
4. Run the following command: `python main.py`
This command will start the Flask server, and it will be accessible at http://localhost:5000.

# Running the Frontend
To run the frontend, you can use a live server. If you don't have it installed, you can use extensions for popular code editors like Visual Studio Code.

Open the 'index.html' file from the loan_calculator_frontend folder in your code editor.
Right-click on 'index.html'.
Choose the "Open with Live Server" option.
The frontend will open in your web browser at http://localhost:5500. You can now interact with the loan calculator and compare rates between the two financial institutions.

# Accessing the API
The API is designed to be separate from the web application to facilitate external access. To use the API, send HTTP requests to its endpoints.

* POST /calculate-loan: Calculate loan instalments.
* GET /download-pdf: Download instalments as a PDF file.

You can access these endpoints by making HTTP requests to the API server, which runs at http://localhost:5000.
