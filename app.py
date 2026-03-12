from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{sql1_1nj3ct10n_1s_fun_and_easy}")

# Init DB
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        role TEXT
    )""")
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'supersecret123', 'admin')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'password123', 'user')")
    c.execute("INSERT OR IGNORE INTO users VALUES (3, 'bob', 'letmein', 'user')")
    # Flag hidden in secret table
    c.execute("""CREATE TABLE IF NOT EXISTS secrets (
        id INTEGER PRIMARY KEY,
        name TEXT,
        value TEXT
    )""")
    c.execute(f"INSERT OR IGNORE INTO secrets VALUES (1, 'flag', '{FLAG}')")
    conn.commit()
    conn.close()

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - BookStore</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Courier New', monospace; background: #0d1117; color: #c9d1d9; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 40px; width: 400px; }
        h1 { color: #58a6ff; margin-bottom: 8px; font-size: 1.5rem; }
        .hint { color: #8b949e; font-size: 0.8rem; margin-bottom: 24px; }
        input { width: 100%; padding: 10px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; margin-bottom: 12px; font-family: inherit; }
        button { width: 100%; padding: 10px; background: #238636; border: none; border-radius: 6px; color: white; cursor: pointer; font-family: inherit; font-size: 1rem; }
        button:hover { background: #2ea043; }
        .result { margin-top: 16px; padding: 12px; border-radius: 6px; font-size: 0.85rem; }
        .success { background: #0f2a1a; border: 1px solid #238636; color: #3fb950; }
        .error { background: #2a0f0f; border: 1px solid #f85149; color: #f85149; }
        .info { background: #0d2137; border: 1px solid #388bfd; color: #79c0ff; margin-bottom: 16px; padding: 10px; border-radius: 6px; font-size: 0.8rem; }
    </style>
</head>
<body>
<div class="container">
    <h1>📚 BookStore Login</h1>
    <p class="hint">Challenge: SQL Injection [Easy]</p>
    <div class="info">💡 Hint: Try to login as admin without knowing the password...</div>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" value="{{ username }}">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    {% if result %}
    <div class="result {{ result_class }}">{{ result }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    result_class = None
    username = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            conn = sqlite3.connect("/tmp/users.db")
            c = conn.cursor()
            # VULNERABLE: string formatting instead of parameterized query
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            c.execute(query)
            user = c.fetchone()
            conn.close()

            if user:
                if user[3] == "admin":
                    result = f"🎉 Welcome Admin! Here's your flag: {FLAG}"
                    result_class = "success"
                else:
                    result = f"Welcome {user[1]}! But you're not admin..."
                    result_class = "error"
            else:
                result = "❌ Invalid credentials!"
                result_class = "error"
        except Exception as e:
            result = f"DB Error: {str(e)}"
            result_class = "error"

    return render_template_string(TEMPLATE, result=result, result_class=result_class, username=username)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
