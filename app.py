from flask import Flask, request, redirect
import time

app = Flask(__name__)

DURATION = 60
queue = []

def update_queue():
    now = int(time.time())
    while queue and queue[0][2] <= now:
        queue.pop(0)

@app.route("/", methods=["GET", "POST"])
def index():
    update_queue()
    now = int(time.time())

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            start = queue[-1][2] if queue else now
            end = start + DURATION
            queue.append((text, start, end))
        return redirect("/")

    current = queue[0] if queue and queue[0][1] <= now < queue[0][2] else None

    text = current[0] if current else "BU DAKİKA BOŞ"
    remaining = current[2] - now if current else 0
    waiting = len(queue) - (1 if current else 0)

    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>1 Dakika Sahne Senin</title>
</head>
<body style="background:black;color:white;text-align:center;font-family:Arial">
<h1>{text}</h1>
<p>{'Kalan süre: ' + str(remaining) + ' sn' if current else ''}</p>
<p>Sırada {waiting} kişi var</p>
<form method="post">
<input name="text" maxlength="120" placeholder="1 dakika ne yazılsın?" required>
<button>Gönder</button>
</form>
</body>
</html>
"""

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
