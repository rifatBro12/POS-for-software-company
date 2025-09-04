from flask import Flask, render_template, request, redirect, url_for, send_file
from jinja2 import DictLoader
import csv, random, string, os, datetime
import json

app = Flask(__name__)

# -------------------------
# Data Files
# -------------------------
catalog_file = "catalog.csv"
sales_file = "sales.csv"
catalog = {}
sales = []

# -------------------------
# Helpers
# -------------------------
def load_catalog():
    if os.path.exists(catalog_file):
        with open(catalog_file, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    catalog[row[0]] = float(row[1])

def save_catalog():
    with open(catalog_file, "w", newline="") as f:
        writer = csv.writer(f)
        for k,v in catalog.items():
            writer.writerow([k,v])

def save_sales():
    with open(sales_file, "w", newline="") as f:
        writer = csv.writer(f)
        for s in sales:
            writer.writerow(s)

def generate_license_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def generate_demo_key():
    return "DEMO-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# -------------------------
# Templates
# -------------------------
base_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Software POS System</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family:'Segoe UI',sans-serif; margin:0; padding:0; background: linear-gradient(135deg,#74ebd5,#9face6); }
        header { background:#2c3e50; color:white; padding:1rem; text-align:center; }
        nav a { margin:0 15px; color:white; text-decoration:none; font-weight:bold; }
        .container { width:90%; max-width:1200px; margin:2rem auto; background:white; padding:2rem; border-radius:12px; box-shadow:0 6px 15px rgba(0,0,0,0.2);}
        h2 { color:#2c3e50; }
        table { width:100%; border-collapse:collapse; margin-top:1rem; }
        th,td { padding:12px; border-bottom:1px solid #ddd; text-align:left; }
        th { background:#3498db; color:white; }
        .btn { padding:8px 15px; margin:4px 5px; background:#3498db; color:white; border:none; border-radius:6px; cursor:pointer; }
        .btn:hover { background:#2980b9; }
        .danger { background:#e74c3c; }
        .danger:hover { background:#c0392b; }
        .success { color:green; }
        .card { display:inline-block; padding:20px; background:#f9f9f9; border-radius:10px; margin:10px; width:30%; box-shadow:0 3px 8px rgba(0,0,0,0.1); text-align:center; }
        input[type=text], input[type=number], select { padding:8px; margin:5px 0; width:40%; border:1px solid #ccc; border-radius:6px; }
    </style>
</head>
<body>
    <header>
        <h1>Software POS System</h1>
        <nav>
            <a href="{{ url_for('home') }}">Dashboard</a>
            <a href="{{ url_for('view_catalog') }}">Catalog</a>
            <a href="{{ url_for('sell_product') }}">Sell</a>
            <a href="{{ url_for('view_sales') }}">Sales</a>
        </nav>
    </header>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

home_template = """
{% extends "base.html" %}
{% block content %}
<h2>Dashboard</h2>
<div class="card">Total Products: <h3>{{ total_products }}</h3></div>
<div class="card">Total Sales: <h3>{{ total_sales }}</h3></div>
<div class="card">Revenue: <h3>${{ "%.2f"|format(revenue) }}</h3></div>
<br><br>
<h3>Sales by Product</h3>
<canvas id="barChart" width="400" height="200"></canvas>
<h3>Revenue Distribution</h3>
<canvas id="pieChart" width="400" height="200"></canvas>
<script>
var ctx = document.getElementById('barChart').getContext('2d');
var barChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: {{ product_names|tojson }},
        datasets: [{
            label: 'Units Sold',
            data: {{ product_sales|tojson }},
            backgroundColor: 'rgba(52, 152, 219,0.7)'
        }]
    },
    options: { responsive:true, plugins:{legend:{display:false}} }
});
var ctx2 = document.getElementById('pieChart').getContext('2d');
var pieChart = new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: {{ product_names|tojson }},
        datasets: [{
            data: {{ product_revenue|tojson }},
            backgroundColor: [
                'rgba(231,76,60,0.7)','rgba(46,204,113,0.7)','rgba(155,89,182,0.7)',
                'rgba(241,196,15,0.7)','rgba(52,152,219,0.7)','rgba(26,188,156,0.7)'
            ]
        }]
    },
    options: { responsive:true }
});
</script>
{% endblock %}
"""

catalog_template = """
{% extends "base.html" %}
{% block content %}
<h2>Product Catalog</h2>
<form method="post">
    <input type="text" name="name" placeholder="Product Name" required>
    <input type="number" step="0.01" name="price" placeholder="Price" required>
    <button class="btn" type="submit">Add Product</button>
</form>
<br>
<form method="get">
    <input type="text" name="search" placeholder="Search product">
    <button class="btn" type="submit">Search</button>
</form>
<br>
<table>
<tr><th>Product</th><th>Price</th><th>Actions</th></tr>
{% for name, price in catalog.items() %}
<tr>
<td>{{ name }}</td>
<td>${{ "%.2f"|format(price) }}</td>
<td>
<a class="btn" href="{{ url_for('edit_product', name=name) }}">Edit</a>
<a class="btn danger" href="{{ url_for('delete_product', name=name) }}">Delete</a>
</td>
</tr>
{% endfor %}
</table>
<br>
<a class="btn" href="{{ url_for('export_catalog') }}">Export CSV</a>
{% endblock %}
"""

edit_template = """
{% extends "base.html" %}
{% block content %}
<h2>Edit Product</h2>
<form method="post">
<input type="text" name="name" value="{{ name }}" readonly>
<input type="number" step="0.01" name="price" value="{{ price }}" required>
<button class="btn" type="submit">Update</button>
</form>
{% endblock %}
"""

sell_template = """
{% extends "base.html" %}
{% block content %}
<h2>Sell Product</h2>
<form method="post">
<select name="name" required>
{% for name in catalog.keys() %}
<option value="{{ name }}">{{ name }}</option>
{% endfor %}
</select>
<input type="number" name="quantity" min="1" value="1" required>
<input type="text" name="customer" placeholder="Customer Name" required>
<input type="text" name="location" placeholder="Location" required>
<button class="btn" type="submit">Sell</button>
</form>
{% if message %}
<p class="success">{{ message }}</p>
<a class="btn" href="{{ url_for('invoice', sale_id=sale_id) }}">View Invoice</a>
{% endif %}
{% endblock %}
"""

sales_template = """
{% extends "base.html" %}
{% block content %}
<h2>Sales History</h2>
<form method="get">
<input type="text" name="search" placeholder="Search by product">
<button class="btn" type="submit">Filter</button>
</form>
<table>
<tr><th>Product</th><th>Qty</th><th>Total</th><th>License</th><th>Customer</th><th>Location</th><th>Date</th><th>Invoice</th></tr>
{% for s in sales %}
<tr>
<td>{{ s[0] }}</td>
<td>{{ s[1] }}</td>
<td>${{ "%.2f"|format(s[2]) }}</td>
<td>{{ s[3] }}</td>
<td>{{ s[4] }}</td>
<td>{{ s[5] }}</td>
<td>{{ s[6] }}</td>
<td><a class="btn" href="{{ url_for('invoice', sale_id=loop.index0) }}">View</a></td>
</tr>
{% endfor %}
</table>
<a class="btn" href="{{ url_for('export_sales') }}">Export CSV</a>
{% endblock %}
"""

invoice_template = """
{% extends "base.html" %}
{% block content %}
<h2 style="text-align:center;">Invoice</h2>
<div style="border:2px solid #3498db; padding:20px; border-radius:10px;">
<p><strong>Customer:</strong> {{ sale[4] }}</p>
<p><strong>Location:</strong> {{ sale[5] }}</p>
<p><strong>Product:</strong> {{ sale[0] }}</p>
<p><strong>Quantity:</strong> {{ sale[1] }}</p>
<p><strong>Total:</strong> ${{ "%.2f"|format(sale[2]) }}</p>
<p><strong>License Key:</strong> {{ sale[3] }}</p>
<p><strong>Date:</strong> {{ sale[6] }}</p>
</div>
<br>
<button class="btn" onclick="window.print()">Print Invoice</button>
{% endblock %}
"""

# -------------------------
# Register templates
# -------------------------
app.jinja_loader = DictLoader({
    "base.html": base_template,
    "home.html": home_template,
    "catalog.html": catalog_template,
    "edit.html": edit_template,
    "sell.html": sell_template,
    "sales.html": sales_template,
    "invoice.html": invoice_template
})

# -------------------------
# Routes
# -------------------------
@app.route("/")
def home():
    revenue = sum(s[2] for s in sales)
    total_products = len(catalog)
    total_sales = len(sales)
    # Chart Data
    products = {}
    for s in sales:
        if s[0] not in products:
            products[s[0]] = [0,0]
        products[s[0]][0] += s[1]    # qty
        products[s[0]][1] += s[2]    # revenue
    product_names = list(products.keys())
    product_sales = [products[k][0] for k in product_names]
    product_revenue = [products[k][1] for k in product_names]
    return render_template("home.html", total_products=total_products, total_sales=total_sales,
                           revenue=revenue, product_names=product_names, product_sales=product_sales,
                           product_revenue=product_revenue)

@app.route("/catalog", methods=["GET","POST"])
def view_catalog():
    if request.method=="POST":
        name = request.form["name"]
        price = float(request.form["price"])
        catalog[name]=price
        save_catalog()
    search = request.args.get("search")
    filtered = {k:v for k,v in catalog.items() if not search or search.lower() in k.lower()}
    return render_template("catalog.html", catalog=filtered)

@app.route("/catalog/edit/<name>", methods=["GET","POST"])
def edit_product(name):
    if request.method=="POST":
        catalog[name]=float(request.form["price"])
        save_catalog()
        return redirect(url_for("view_catalog"))
    return render_template("edit.html", name=name, price=catalog[name])

@app.route("/catalog/delete/<name>")
def delete_product(name):
    catalog.pop(name,None)
    save_catalog()
    return redirect(url_for("view_catalog"))

@app.route("/sell", methods=["GET","POST"])
def sell_product():
    message = None
    sale_id = None
    if request.method=="POST":
        name = request.form["name"]
        qty = int(request.form["quantity"])
        customer = request.form["customer"]
        location = request.form["location"]
        if name in catalog:
            total = catalog[name]*qty
            key = generate_license_key()
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            sale = [name, qty, total, key, customer, location, date]
            sales.append(sale)
            save_sales()
            sale_id = len(sales)-1
            message = f"Sold {qty} x {name} for ${total:.2f}."
    return render_template("sell.html", catalog=catalog, message=message, sale_id=sale_id)

@app.route("/sales")
def view_sales():
    search = request.args.get("search")
    filtered = [s for s in sales if not search or search.lower() in s[0].lower()]
    return render_template("sales.html", sales=filtered)

@app.route("/invoice/<int:sale_id>")
def invoice(sale_id):
    return render_template("invoice.html", sale=sales[sale_id])

@app.route("/export/catalog")
def export_catalog():
    return send_file(catalog_file, as_attachment=True)

@app.route("/export/sales")
def export_sales():
    return send_file(sales_file, as_attachment=True)

# -------------------------
# Startup
# -------------------------
if __name__=="__main__":
    load_catalog()
    app.run(debug=True)
