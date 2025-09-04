from flask import Flask, render_template, request, send_file
from jinja2 import DictLoader
from utils import load_catalog, load_sales, save_catalog, save_sales, generate_license_key, catalog, sales
from templates import base_template, home_template, catalog_template, sell_template, sales_template
from collections import defaultdict

app = Flask(__name__)

# Register in-memory templates
app.jinja_loader = DictLoader({
    "base.html": base_template,
    "home.html": home_template,
    "catalog.html": catalog_template,
    "sell.html": sell_template,
    "sales.html": sales_template,
})

# Routes
@app.route("/")
def home():
    sales_summary = defaultdict(float)
    for s in sales:
        sales_summary[s[0]] += s[2]
    labels = list(sales_summary.keys())
    data = list(sales_summary.values())
    num_products = len(catalog)
    total_sales = len(sales)
    total_revenue = sum(data)
    return render_template("home.html", num_products=num_products, total_sales=total_sales, total_revenue=total_revenue, labels=labels, data=data)

@app.route("/catalog", methods=["GET", "POST"])
def view_catalog():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "delete":
            name = request.form["name"]
            if name in catalog:
                del catalog[name]
                save_catalog()
        elif action == "update":
            name = request.form["name"]
            new_price = float(request.form["new_price"])
            if name in catalog:
                catalog[name] = new_price
                save_catalog()
        else:
            name = request.form["name"]
            price = float(request.form["price"])
            catalog[name] = price
            save_catalog()
    return render_template("catalog.html", catalog=catalog)

@app.route("/sell", methods=["GET", "POST"])
def sell_product():
    message = None
    if request.method == "POST":
        name = request.form["name"]
        qty = int(request.form["quantity"])
        if name in catalog:
            total = catalog[name] * qty
            key = generate_license_key()
            sales.append([name, qty, total, key])
            save_sales()
            message = f"Sold {qty} x {name} for ${total:.2f}. License: {key}"
    return render_template("sell.html", catalog=catalog, message=message)

@app.route("/sales")
def view_sales():
    total = sum(s[2] for s in sales)
    return render_template("sales.html", sales=sales, total=total)

@app.route("/export/catalog")
def export_catalog():
    return send_file("catalog.csv", as_attachment=True)

@app.route("/export/sales")
def export_sales():
    return send_file("sales.csv", as_attachment=True)

# Startup
if __name__ == "__main__":
    load_catalog()
    load_sales()
    app.run(debug=True)