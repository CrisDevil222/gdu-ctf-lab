from flask import Flask, request, render_template_string, session, redirect
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
FLAG = os.environ.get("FLAG", "")

USERS = {
    1: {"name": "Alice", "email": "alice@example.com", "role": "user", "note": "My shopping list: milk, eggs"},
    2: {"name": "Bob", "email": "bob@example.com", "role": "user", "note": "Reminder: fix the bike"},
    3: {"name": "Admin", "email": "admin@ctf.local", "role": "admin", "note": f"SECRET FLAG: {FLAG}"},
    4: {"name": "Charlie", "email": "charlie@example.com", "role": "user", "note": "Nothing interesting here"},
}

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>UserPanel - IDOR Challenge</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; min-height: 100vh; }
        .navbar { background: #1e3a5f; color: white; padding: 16px 40px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { font-size: 1.2rem; }
        .container { max-width: 800px; margin: 40px auto; padding: 0 20px; }
        .card { background: white; border-radius: 12px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 24px; }
        .info-box { background: #e8f4fd; border-left: 4px solid #1e90ff; padding: 16px; border-radius: 4px; margin-bottom: 24px; font-size: 0.85rem; line-height: 1.7; }
        .field { margin-bottom: 16px; }
        .label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
        .value { font-size: 1rem; color: #333; padding: 10px; background: #f8f9fa; border-radius: 6px; }
        .role-badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
        .role-admin { background: #fee2e2; color: #dc2626; }
        .role-user { background: #e0f2fe; color: #0284c7; }
        .flag-box { background: #052e16; color: #4ade80; padding: 20px; border-radius: 8px; font-family: monospace; font-size: 1.1rem; margin-top: 12px; border: 1px solid #16a34a; }
        .nav-links { display: flex; gap: 8px; margin-top: 16px; }
        .nav-links a { padding: 8px 16px; background: #1e3a5f; color: white; border-radius: 6px; text-decoration: none; font-size: 0.85rem; }
        .nav-links a:hover { background: #2d5a8e; }
    </style>
</head>
<body>
<div class="navbar">
    <h1>🔒 UserPanel</h1>
    <span style="color:#90caf9;font-size:0.85rem;">Logged in as: {{ current_user.name }}</span>
</div>
<div class="container">
    <div class="info-box">
        💡 <strong>Challenge: IDOR (Insecure Direct Object Reference) [Medium]</strong><br>
        You are logged in as <strong>Alice (user_id=1)</strong>. Each user has a profile page at <code>/profile?id=X</code>.<br>
        Can you access another user's private notes? The admin might be hiding something...
    </div>

    <div class="card">
        <h2 style="margin-bottom:20px;color:#1e3a5f;">👤 Profile: {{ profile.name }}</h2>
        <div class="field">
            <div class="label">User ID</div>
            <div class="value">{{ profile_id }}</div>
        </div>
        <div class="field">
            <div class="label">Email</div>
            <div class="value">{{ profile.email }}</div>
        </div>
        <div class="field">
            <div class="label">Role</div>
            <div class="value">
                <span class="role-badge role-{{ profile.role }}">{{ profile.role }}</span>
            </div>
        </div>
        <div class="field">
            <div class="label">Private Note</div>
            <div class="value">{{ profile.note }}</div>
        </div>
        {% if profile.role == 'admin' %}
        <div class="flag-box">🎉 {{ profile.note }}</div>
        {% endif %}
    </div>

    <div class="nav-links">
        <a href="/profile?id=1">My Profile (id=1)</a>
        <a href="/profile?id=2">User id=2</a>
        <a href="/profile?id=3">User id=3</a>
        <a href="/profile?id=4">User id=4</a>
    </div>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return redirect("/profile?id=1")

@app.route("/profile")
def profile():
    # IDOR: no authorization check, just fetches any user by ID
    try:
        profile_id = int(request.args.get("id", 1))
    except:
        profile_id = 1

    profile = USERS.get(profile_id, USERS[1])
    current_user = USERS[1]  # always "logged in" as Alice

    return render_template_string(TEMPLATE,
        profile=profile,
        profile_id=profile_id,
        current_user=current_user
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
