base_template = """
<!DOCTYPE html>
<html>
<head>
    <title>POS System - Software Company</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
        }
        header {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
            padding: 1rem;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        nav a {
            margin: 0 15px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        nav a:hover {
            color: #00b4db;
        }
        .container {
            width: 85%;
            margin: 2rem auto;
            background: #1f1f1f;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #333;
            text-align: left;
        }
        th {
            background: #0f2027;
            color: white;
        }
        .btn {
            padding: 8px 16px;
            margin: 6px 0;
            background: #00b4db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: #0083b0;
            transform: scale(1.05);
        }
        .btn-danger {
            background: #e74c3c;
        }
        .btn-danger:hover {
            background: #c0392b;
            transform: scale(1.05);
        }
        .success {
            color: #2ecc71;
            font-weight: bold;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        .card {
            background: #2c2c2c;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        input, select {
            padding: 8px;
            margin: 6px 0;
            background: #333;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 6px;
        }
        @media (max-width: 768px) {
            .container {
                width: 95%;
            }
            nav a {
                display: block;
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>POS System - Software Company</h1>
        <nav>
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('view_catalog') }}">Catalog</a>
            <a href="{{ url_for('sell_product') }}">Sell Product</a>
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
    <h2>Welcome to the Software Company POS</h2>
    <p>Use the navigation bar above to manage products, sales, and reports.</p>
    <h3>Dashboard</h3>
    <p>Number of Products: {{ num_products }}</p>
    <p>Number of Sales: {{ total_sales }}</p>
    <p>Total Revenue: ${{ "%.2f"|format(total_revenue) }}</p>
    {% if labels %}
    <canvas id="myChart" width="600" height="300"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: {{ labels | tojson }},
            datasets: [{
                label: 'Revenue by Product',
                data: {{ data | tojson }},
                backgroundColor: 'rgba(0, 180, 219, 0.4)',
                borderColor: 'rgba(0, 180, 219, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#444' }
                },
                x: {
                    grid: { color: '#444' }
                }
            },
            plugins: {
                legend: { labels: { color: '#e0e0e0' } }
            }
        }
    });
    </script>
    {% endif %}
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
    <div class="product-grid">
        {% for name, price in catalog.items() %}
        <div class="card">
            <h3>{{ name }}</h3>
            <p>${{ "%.2f"|format(price) }}</p>
            <form method="post">
                <input type="hidden" name="action" value="update">
                <input type="hidden" name="name" value="{{ name }}">
                <input type="number" step="0.01" name="new_price" value="{{ "%.2f"|format(price) }}" required>
                <button type="submit" class="btn">Update Price</button>
            </form>
            <form method="post">
                <input type="hidden" name="action" value="delete">
                <input type="hidden" name="name" value="{{ name }}">
                <button type="submit" class="btn btn-danger">Delete</button>
            </form>
        </div>
        {% endfor %}
    </div>
    <br>
    <a class="btn" href="{{ url_for('export_catalog') }}">Export Catalog CSV</a>
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
        <button class="btn" type="submit">Sell</button>
    </form>
    <p id="total">Total: $0.00</p>
    {% if message %}
        <p class="success">{{ message }}</p>
    {% endif %}
    <script>
    var prices = {{ catalog | tojson }};
    function updateTotal() {
        var name = document.querySelector('select[name="name"]').value;
        var qty = parseInt(document.querySelector('input[name="quantity"]').value) || 1;
        var total = (prices[name] || 0) * qty;
        document.getElementById('total').innerHTML = 'Total: $' + total.toFixed(2);
    }
    document.querySelector('select[name="name"]').addEventListener('change', updateTotal);
    document.querySelector('input[name="quantity"]').addEventListener('input', updateTotal);
    updateTotal();
    </script>
{% endblock %}
"""

sales_template = """
{% extends "base.html" %}
{% block content %}
    <h2>Sales History</h2>
    <table>
        <tr><th>Product</th><th>Quantity</th><th>Total</th><th>License Key</th></tr>
        {% for sale in sales %}
        <tr>
            <td>{{ sale[0] }}</td>
            <td>{{ sale[1] }}</td>
            <td>${{ "%.2f"|format(sale[2]) }}</td>
            <td>{{ sale[3] }}</td>
        </tr>
        {% endfor %}
    </table>
    <p>Total Revenue: ${{ "%.2f"|format(total) }}</p>
    <br>
    <a class="btn" href="{{ url_for('export_sales') }}">Export Sales CSV</a>
{% endblock %}
"""