from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")

def init_db():
    conn = sqlite3.connect("/tmp/shop.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        description TEXT
    )""")
    products = [
        (1, "Laptop Pro X1", "Electronics", 999.99, "High performance laptop with 16GB RAM"),
        (2, "Wireless Mouse", "Electronics", 29.99, "Ergonomic wireless mouse"),
        (3, "Mechanical Keyboard", "Electronics", 89.99, "RGB mechanical keyboard"),
        (4, "Coffee Mug", "Kitchen", 14.99, "Large ceramic coffee mug"),
        (5, "Notebook A5", "Stationery", 5.99, "Lined notebook 200 pages"),
        (6, "Python Book", "Books", 39.99, "Learn Python programming"),
    ]
    c.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?,?)", products)
    # Secret table with flag
    c.execute("""CREATE TABLE IF NOT EXISTS admin_secrets (
        id INTEGER PRIMARY KEY,
        key_name TEXT,
        key_value TEXT
    )""")
    c.execute(f"INSERT OR IGNORE INTO admin_secrets VALUES (1, 'secret_flag', '{FLAG}')")
    c.execute("INSERT OR IGNORE INTO admin_secrets VALUES (2, 'admin_pass', 'sup3r_s3cr3t_p4ss!')")
    conn.commit()
    conn.close()

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDU Shop - Product Search</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            color: #e2e8f0;
        }
        .topbar {
            background: linear-gradient(90deg, #1a1a2e, #16213e);
            border-bottom: 1px solid rgba(99, 102, 241, 0.3);
            padding: 16px 40px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .topbar h1 {
            font-size: 1.4rem;
            font-weight: 700;
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .badge-medium {
            background: rgba(251,146,60,0.15);
            color: #fb923c;
            border: 1px solid rgba(251,146,60,0.4);
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
        }
        .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
        .search-card {
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(168,85,247,0.05));
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 28px;
        }
        .search-card h2 { font-size: 1rem; color: #a5b4fc; margin-bottom: 16px; font-weight: 600; }
        .search-row { display: flex; gap: 12px; }
        .search-row input {
            flex: 1;
            padding: 12px 16px;
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(99,102,241,0.3);
            border-radius: 10px;
            color: #e2e8f0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-row input:focus { border-color: #818cf8; }
        .search-row button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.9rem;
            transition: opacity 0.2s, transform 0.1s;
        }
        .search-row button:hover { opacity: 0.85; transform: translateY(-1px); }
        .hint-box {
            background: rgba(251, 191, 36, 0.07);
            border: 1px solid rgba(251, 191, 36, 0.25);
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 0.82rem;
            color: #fcd34d;
            margin-bottom: 28px;
        }
        .hint-box code {
            background: rgba(0,0,0,0.3);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.8rem;
            color: #f9a8d4;
        }
        .results-label {
            font-size: 0.8rem;
            color: #6b7280;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }
        thead {
            background: rgba(99,102,241,0.15);
        }
        thead th {
            padding: 12px 16px;
            text-align: left;
            color: #a5b4fc;
            font-weight: 600;
            border-bottom: 1px solid rgba(99,102,241,0.2);
        }
        tbody tr {
            border-bottom: 1px solid rgba(255,255,255,0.04);
            transition: background 0.15s;
        }
        tbody tr:hover { background: rgba(99,102,241,0.05); }
        tbody td {
            padding: 12px 16px;
            color: #cbd5e1;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #6b7280;
            font-style: italic;
        }
        .error-box {
            background: rgba(239,68,68,0.1);
            border: 1px solid rgba(239,68,68,0.3);
            border-radius: 10px;
            padding: 14px 18px;
            color: #fca5a5;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            margin-top: 12px;
        }
        .query-display {
            font-family: 'Courier New', monospace;
            font-size: 0.78rem;
            color: #4b5563;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="topbar">
        <h1>🛒 GDU Shop</h1>
        <span class="badge-medium">SQL Injection [Medium]</span>
    </div>

    <div class="container">


        <div class="search-card">
            <h2>🔍 Search Products</h2>
            <form method="GET">
                <div class="search-row">
                    <input type="text" name="q" placeholder="Search product name..." value="{{ query | e }}" id="search-input">
                    <button type="submit">Search</button>
                </div>
            </form>
            {% if query %}
            <p class="query-display">SQL: SELECT * FROM products WHERE name LIKE '%{{ query | e }}%'</p>
            {% endif %}
        </div>

        {% if error %}
        <div class="error-box">⚠️ Database Error: {{ error }}</div>
        {% elif results is not none %}
        <p class="results-label">{{ results|length }} result(s) found</p>
        {% if results %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {% for row in results %}
                <tr>
                    {% for col in row %}
                    <td>{{ col }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="no-results">No products found matching your search.</div>
        {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")
    results = None
    error = None

    if query:
        try:
            conn = sqlite3.connect("/tmp/shop.db")
            c = conn.cursor()
            # VULNERABLE: UNION-based SQL Injection
            sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
            c.execute(sql)
            results = c.fetchall()
            conn.close()
        except Exception as e:
            error = str(e)

    return render_template_string(TEMPLATE, query=query, results=results, error=error)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
