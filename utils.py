import csv
import random
import string
import os

catalog_file = "catalog.csv"
sales_file = "sales.csv"

catalog = {}
sales = []

def load_catalog():
    global catalog
    if os.path.exists(catalog_file):
        with open(catalog_file, mode="r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    catalog[row[0]] = float(row[1])

def load_sales():
    global sales
    sales = []
    if os.path.exists(sales_file):
        with open(sales_file, mode="r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    sales.append([row[0], int(row[1]), float(row[2]), row[3]])

def save_catalog():
    with open(catalog_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        for name, price in catalog.items():
            writer.writerow([name, price])

def save_sales():
    with open(sales_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        for sale in sales:
            writer.writerow(sale)

def generate_license_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))