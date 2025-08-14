try:
    from flask import Flask, Response
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, Response

import random

app = Flask(__name__)

messages = [
    "Sakshi, I love you ❤️",
    "I love you, Sakshi 💖",
    "Forever yours, Sakshi ❤️",
    "Sakshi ❤️ You mean the world to me",
    "Sakshi 💕 My heart belongs to you",
    "I can't stop loving you, Sakshi 💗",
    "Always and forever, Sakshi ❤️",
]

@app.route('/')
def love():
    return Response((random.choice(messages) + " " for _ in iter(int, 1)))

if __name__ == "__main__":
    app.run()
