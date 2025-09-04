# Software Company POS System

This is a Flask-based Point of Sale (POS) system designed for a software company to manage product catalogs, sales, and license key generation. The application features a modern, dark-themed user interface with a dashboard, product management, sales tracking, and CSV export capabilities.

## Features
- **Dashboard**: Displays the number of products, total sales, total revenue, and a bar chart of revenue by product using Chart.js.
- **Product Catalog**: Add, update, or delete products with a grid-based card layout for easy management.
- **Sell Products**: Select products and quantities to record sales, with real-time total price calculation and license key generation.
- **Sales History**: View all sales with details and export them to CSV.
- **Export Functionality**: Export product catalog and sales data as CSV files.
- **Responsive Design**: Mobile-friendly layout with a sticky header and hover effects.

## Project Structure
```
├── app.py          # Main Flask application with routes and logic
├── utils.py        # Helper functions for data handling and CSV operations
├── templates.py    # In-memory HTML templates for the application
├── catalog.csv     # Generated file for storing product catalog (created on first use)
├── sales.csv       # Generated file for storing sales data (created on first use)
└── README.md       # This file
```

## Prerequisites
- **Python**: Version 3.6 or higher
- **Visual Studio Code**: For development and running the application
- **Flask**: Installed via pip
- **Internet Connection**: Required for loading Chart.js and Google Fonts (Roboto) from CDNs

## Setup Instructions
Follow these steps to run the application in Visual Studio Code:

1. **Clone or Create the Project Directory**:
   - Create a new directory for the project.
   - Save the provided `app.py`, `utils.py`, and `templates.py` files in this directory.

2. **Open the Project in VS Code**:
   - Launch VS Code and open the project directory (`File > Open Folder`).

3. **Set Up a Virtual Environment**:
   - Open the terminal in VS Code (`Ctrl+~` or `View > Terminal`).
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - Windows:
       ```bash
       venv\Scripts\activate
       ```
     - macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. **Install Dependencies**:
   - Install Flask:
     ```bash
     pip install flask
     ```

5. **Run the Application**:
   - In the terminal, run:
     ```bash
     python app.py
     ```
   - The Flask development server will start, typically at `http://127.0.0.1:5000`.

6. **Access the Application**:
   - Open a web browser and navigate to `http://127.0.0.1:5000`.
   - Use the navigation bar to access the Home, Catalog, Sell Product, and Sales pages.

## Usage
- **Home**: View the dashboard with key metrics and a revenue chart.
- **Catalog**: Add new products with a name and price, update existing product prices, or delete products. Export the catalog as a CSV file.
- **Sell Product**: Select a product and quantity to record a sale. A license key is generated, and the total price is displayed in real-time.
- **Sales**: View all recorded sales with product details, quantities, totals, and license keys. Export sales data as a CSV file.

## Notes
- The application uses in-memory templates defined in `templates.py`, so no separate HTML files are needed.
- Data is stored in `catalog.csv` and `sales.csv`, which are created automatically in the project directory when you add products or record sales.
- The application runs in debug mode (`debug=True`) for development. Disable this in production for security.
- Ensure an internet connection for the dashboard's Chart.js and Google Fonts to load correctly.

## Troubleshooting
- **Flask Not Found**: Ensure Flask is installed in the virtual environment (`pip install flask`).
- **Port Conflict**: If port 5000 is in use, Flask will show an error. Change the port by running `python app.py --port 5001` or terminate the conflicting process.
- **CSV Files Not Created**: Ensure the application has write permissions in the project directory.
- **Chart Not Displaying**: Verify your internet connection, as Chart.js is loaded from a CDN.

## License
This project is for educational purposes and does not include a specific license. Modify and use as needed for personal or learning purposes.
