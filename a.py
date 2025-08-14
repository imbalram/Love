try:
    from flask import Flask, Response
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, Response

import random, time

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
    def generate():
        while True:
            msg = random.choice(messages)
            for word in msg.split():
                yield word + " "
                time.sleep(0.3)  # typing speed
            yield "\n"  # new line after message
            time.sleep(0.5)  # small pause before next line
    return Response(generate(), mimetype='text/plain')

if __name__ == "__main__":
    app.run()
