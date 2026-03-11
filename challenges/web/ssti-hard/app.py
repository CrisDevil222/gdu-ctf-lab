from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{ssti_j1nj4_t3mpl4t3_1nj3ct10n}")

WRAPPER = """
<!DOCTYPE html>
<html>
<head>
    <title>Greeting Card - SSTI Challenge</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Courier New', monospace; background: #13111a; color: #e2e0f0; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; }}
        .card {{ background: #1e1a2e; border: 1px solid #4a3f6b; border-radius: 12px; padding: 40px; max-width: 600px; width: 100%; }}
        h1 {{ color: #c084fc; margin-bottom: 8px; }}
        .sub {{ color: #7c6fa0; font-size: 0.8rem; margin-bottom: 24px; }}
        .info {{ background: #2a1f4a; border-left: 3px solid #c084fc; padding: 14px; border-radius: 4px; font-size: 0.8rem; line-height: 1.7; margin-bottom: 24px; color: #b8a9d9; }}
        input {{ width: 100%; padding: 12px; background: #13111a; border: 1px solid #4a3f6b; border-radius: 6px; color: #e2e0f0; font-family: inherit; margin-bottom: 12px; }}
        button {{ width: 100%; padding: 12px; background: #7c3aed; border: none; border-radius: 6px; color: white; cursor: pointer; font-family: inherit; font-size: 1rem; }}
        button:hover {{ background: #9333ea; }}
        .result {{ margin-top: 20px; padding: 16px; background: #13111a; border: 1px solid #4a3f6b; border-radius: 8px; line-height: 1.6; }}
        code {{ background: #2a1f4a; padding: 2px 6px; border-radius: 3px; color: #c084fc; font-size: 0.85rem; }}
    </style>
</head>
<body>
<div class="card">
    <h1>🎴 Greeting Card Generator</h1>
    <p class="sub">Challenge: SSTI (Server-Side Template Injection) [Hard]</p>
    <div class="info">
        💡 <strong>Objective:</strong> Read the FLAG environment variable from the server.<br>
        The app renders your name directly into a Jinja2 template.<br>
        Try: <code>{{{{ 7*7 }}}}</code> to test if SSTI is possible.<br>
        Then escalate to: <code>{{{{config}}}}</code> → RCE → flag!
    </div>
    <form method="POST">
        <input type="text" name="name" placeholder="Enter your name..." value="{name_val}">
        <button type="submit">Generate Card 🎨</button>
    </form>
    {result_html}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result_html = ""
    name_val = ""

    if request.method == "POST":
        name = request.form.get("name", "World")
        name_val = name
        try:
            # VULNERABLE: user input rendered directly as template
            template = f"<div class='result'>Hello, {name}! Your greeting card is ready 🎉</div>"
            result_html = render_template_string(template)
        except Exception as e:
            result_html = f"<div class='result' style='color:#f87171;'>Error: {str(e)}</div>"

    return WRAPPER.format(name_val=name_val, result_html=result_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
