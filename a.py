try:
    from flask import Flask
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask

app = Flask(__name__)

@app.route('/')
def love():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Love for Sakshi ❤️</title>
<style>
    body {
        margin: 0;
        background: black;
        overflow: hidden;
        color: pink;
        font-family: Arial, sans-serif;
        text-align: center;
    }
    h1 {
        font-size: 2em;
        margin-top: 20px;
        animation: fade 1.5s infinite alternate;
    }
    @keyframes fade {
        from { opacity: 0.5; }
        to { opacity: 1; }
    }
    .rose {
        position: absolute;
        width: 50px;
        height: 50px;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Red_rose.svg/1024px-Red_rose.svg.png');
        background-size: cover;
        animation: fall linear infinite;
    }
    @keyframes fall {
        to { transform: translateY(100vh); }
    }
</style>
</head>
<body>
<h1 id="message">Sakshi ❤️ I love you</h1>

<script>
const messages = [
    "Sakshi ❤️ I love you",
    "Forever yours, Sakshi 💖",
    "Sorry if I ever hurt you 😔",
    "Sakshi 🌹 You mean everything to me",
    "Hug me, Sakshi 🤗",
    "Always together ❤️"
];

function changeMessage() {
    const msgEl = document.getElementById("message");
    msgEl.textContent = messages[Math.floor(Math.random() * messages.length)];
}
setInterval(changeMessage, 1500);

function createRose() {
    const rose = document.createElement("div");
    rose.className = "rose";
    rose.style.left = Math.random() * 100 + "vw";
    rose.style.animationDuration = (3 + Math.random() * 2) + "s";
    document.body.appendChild(rose);
    setTimeout(() => rose.remove(), 5000);
}
setInterval(createRose, 200);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
