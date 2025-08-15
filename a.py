try:
    from flask import Flask
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1" />
<title>Sakshi, I Love You — Infinite 🌹</title>
<style>
  :root {
    --bg: #07070a;
    --fg: #ffd6e7;
    --accent: #ff4d94;
    --card: #101018;
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    margin: 0; background: radial-gradient(1200px 700px at 50% -20%, #1a0f1f 0%, var(--bg) 60%);
    color: var(--fg); font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji";
    overflow: hidden;
  }
  #ui {
    position: fixed; left: 50%; transform: translateX(-50%);
    bottom: 16px; width: min(940px, calc(100% - 16px));
    background: color-mix(in srgb, var(--card) 85%, #000 15%);
    border: 1px solid #26263a; backdrop-filter: blur(10px);
    border-radius: 16px; padding: 12px;
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,.45);
  }
  #ui .group { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
  label { font-size: 12px; opacity: .8; }
  input[type="range"] { width: 180px; }
  button, .pill {
    border: 1px solid #2c2c44; background: #171727; color: var(--fg);
    padding: 8px 12px; border-radius: 999px; cursor: pointer; font-weight: 600;
  }
  button:hover { border-color: #3f3f66 }
  #msgBar {
    position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
    width: min(860px, calc(100% - 24px)); text-align: center;
    padding: 12px 16px; background: rgba(23,23,39,.65);
    border: 1px solid #2e2e4e; border-radius: 14px; backdrop-filter: blur(8px);
    box-shadow: 0 10px 30px rgba(0,0,0,.35);
  }
  #typed {
    font-size: clamp(18px, 4vw, 32px); font-weight: 800;
    letter-spacing: .3px; text-shadow: 0 2px 16px rgba(255, 77, 148, .35);
  }
  #cursor { display: inline-block; width: .6ch; animation: blink 1s step-end infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  #stage { position: fixed; inset: 0; }
  /* Mobile tweaks */
  @media (max-width: 720px) {
    #ui { grid-template-columns: 1fr; gap: 8px; padding: 10px }
    input[type="range"] { width: 140px; }
  }
</style>
</head>
<body>
<canvas id="stage"></canvas>

<div id="msgBar">
  <span id="typed">Sakshi, I love you</span><span id="cursor">|</span>
</div>

<div id="ui" role="group" aria-label="controls">
  <div class="group">
    <label for="density">Flower storm</label>
    <input id="density" type="range" min="1" max="200" value="80" />
    <span class="pill" id="burst">💥 Burst</span>
  </div>
  <div class="group">
    <label for="speed">Wind / speed</label>
    <input id="speed" type="range" min="0" max="200" value="70" />
    <label for="spin">Spin</label>
    <input id="spin" type="range" min="0" max="360" value="120" />
  </div>
  <div class="group">
    <input id="custom" placeholder="Add a custom message…" style="flex:1; min-width:180px; background:#0f0f1b; color:var(--fg); border:1px solid #2c2c44; border-radius:999px; padding:8px 12px" />
    <button id="add">➕ Add</button>
    <button id="apologize">🙏 Sorry mode</button>
  </div>
</div>

<script>
(() => {
  // ===== Canvas Setup =====
  const canvas = document.getElementById('stage');
  const ctx = canvas.getContext('2d');
  const DPR = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
  function resize() {
    canvas.width = Math.floor(innerWidth * DPR);
    canvas.height = Math.floor(innerHeight * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  }
  addEventListener('resize', resize, {passive:true});
  resize();

  // ===== Config =====
  const ROSES = ["🌹","🌹","🌹","🌸","💮","🌺","🌷","💐","🥀"];
  const HEARTS = ["💖","💗","💓","💞","💕","💘"];
  const MESSAGES_BASE = [
    "Sakshi, I love you ❤️",
    "Forever yours, Sakshi 💖",
    "You are my world, Sakshi 🌍",
    "With you, always 🌙",
    "Sakshi 🌹 my heart beats for you",
    "Every moment is you, Sakshi ✨",
    "Holding on to you, forever 🤝",
  ];
  const APOLOGIES = [
    "Sakshi, I'm sorry 😔",
    "Please forgive me, Sakshi 🙏",
    "I’ll do better for you, Sakshi 💞",
  ];

  let MESSAGES = [...MESSAGES_BASE];
  const typedEl = document.getElementById('typed');

  // ===== Flower Particles =====
  const rand = (a,b) => a + Math.random() * (b - a);
  const pick = arr => arr[(Math.random()*arr.length)|0];

  class Petal {
    constructor(edge) {
      // Spawn from a random edge: 'top','bottom','left','right'
      const w = innerWidth, h = innerHeight;
      if (!edge) edge = pick(['top','bottom','left','right']);
      this.char = Math.random() < .2 ? pick(HEARTS) : pick(ROSES);
      const size = rand(18, 44);
      this.size = size;
      this.alpha = rand(.65, 1);
      this.spin = rand(-2, 2);
      this.angle = rand(0, Math.PI*2);
      this.angularVel = (Math.random() < .5 ? -1 : 1) * (spinInput.value/360) * rand(.5, 1.2);
      const speedBase = (speedInput.value/100);
      const gustX = (speedBase - .5) * 4; // wind
      const spread = Math.max(0.5, densityInput.value/80);

      switch(edge) {
        case 'top':
          this.x = rand(0, w); this.y = -20;
          this.vx = rand(-1, 1) + gustX; this.vy = rand(1.5, 3.2) * spread; break;
        case 'bottom':
          this.x = rand(0, w); this.y = h + 20;
          this.vx = rand(-1, 1) + gustX; this.vy = -rand(1.6, 3.0) * spread; break;
        case 'left':
          this.x = -20; this.y = rand(0, h);
          this.vx = rand(1.2, 2.8) + gustX; this.vy = rand(-.8, .8) * spread; break;
        case 'right':
          this.x = w + 20; this.y = rand(0, h);
          this.vx = -rand(1.2, 2.8) + gustX; this.vy = rand(-.8, .8) * spread; break;
      }
    }
    step(dt) {
      this.angle += this.angularVel * dt;
      this.x += this.vx * dt * 60;
      this.y += this.vy * dt * 60;
      // gentle drift
      this.vx += Math.sin(this.angle) * 0.002;
      this.vy += Math.cos(this.angle) * 0.002;
    }
    draw(ctx) {
      ctx.globalAlpha = this.alpha;
      ctx.font = this.size + "px system-ui, Apple Color Emoji, Segoe UI Emoji";
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.angle * 0.2);
      ctx.fillText(this.char, -this.size*0.4, this.size*0.3);
      ctx.restore();
      ctx.globalAlpha = 1;
    }
    outOfBounds() {
      return this.x < -80 || this.x > innerWidth + 80 || this.y < -80 || this.y > innerHeight + 80;
    }
  }

  const petals = [];
  const densityInput = document.getElementById('density');
  const speedInput = document.getElementById('speed');
  const spinInput = document.getElementById('spin');
  const burstBtn = document.getElementById('burst');
  const addBtn = document.getElementById('add');
  const customInput = document.getElementById('custom');
  const apologizeBtn = document.getElementById('apologize');

  // Spawn stream
  let spawnAccumulator = 0;
  function spawnSome(dt) {
    const targetRate = parseInt(densityInput.value, 10); // particles/sec
    spawnAccumulator += dt * targetRate;
    while (spawnAccumulator > 1) {
      petals.push(new Petal());
      // occasionally spawn from multiple edges for "everywhere"
      if (Math.random() < 0.35) petals.push(new Petal('left'));
      if (Math.random() < 0.35) petals.push(new Petal('right'));
      spawnAccumulator -= 1;
    }
  }

  // Burst
  burstBtn.addEventListener('click', () => {
    const edges = ['top','bottom','left','right'];
    for (let i=0;i<120;i++) petals.push(new Petal(pick(edges)));
  });

  // Add custom message
  addBtn.addEventListener('click', () => {
    const t = customInput.value.trim();
    if (!t) return;
    MESSAGES.push(t);
    customInput.value = "";
    flash(typedEl);
  });

  // Apology mode toggle
  let sorryMode = false;
  apologizeBtn.addEventListener('click', () => {
    sorryMode = !sorryMode;
    if (sorryMode) {
      MESSAGES = [...MESSAGES_BASE, ...APOLOGIES];
      apologizeBtn.textContent = "💗 Love mode";
    } else {
      MESSAGES = [...MESSAGES_BASE];
      apologizeBtn.textContent = "🙏 Sorry mode";
    }
    flash(typedEl);
  });

  function flash(el) {
    el.style.transition = 'filter .25s ease, transform .25s ease';
    el.style.filter = 'drop-shadow(0 0 16px rgba(255,77,148,.6))';
    el.style.transform = 'scale(1.03)';
    setTimeout(()=>{ el.style.filter=''; el.style.transform=''; }, 300);
  }

  // ===== Typing Loop (infinite) =====
  async function typeLoop() {
    const delay = ms => new Promise(r=>setTimeout(r, ms));
    for (;;) {
      const msg = (Math.random()<.15 ? pick(HEARTS)+" " : "") + pick(MESSAGES);
      await typeText(msg);
      await delay(750);
      await eraseText();
      await delay(150);
    }
  }
  async function typeText(text) {
    typedEl.textContent = "";
    for (const ch of text) {
      typedEl.textContent += ch;
      await new Promise(r=>setTimeout(r, ch === ' ' ? 10 : 20)); // fast but readable
    }
  }
  async function eraseText() {
    const txt = typedEl.textContent;
    for (let i = txt.length; i >= 0; i--) {
      typedEl.textContent = txt.slice(0, i);
      await new Promise(r=>setTimeout(r, 6));
    }
  }

  // ===== Animation Loop =====
  let last = performance.now();
  function loop(t) {
    const dt = Math.min(0.05, (t - last) / 1000); // clamp for stability
    last = t;
    // physics & spawn
    spawnSome(dt);
    for (let i = petals.length - 1; i >= 0; i--) {
      const p = petals[i];
      p.step(dt);
      if (p.outOfBounds()) petals.splice(i, 1);
    }
    // draw
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    for (const p of petals) p.draw(ctx);

    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
  typeLoop();

  // iPhone performance safety: reduce density when tab hidden
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) densityInput.value = Math.max(15, densityInput.value|0);
  }, {passive:true});
})();
</script>
</body>
</html>
    """

if __name__ == "__main__":
    # Host on all interfaces so you can open from your iPhone on the same Wi-Fi.
    app.run(host="0.0.0.0", port=5000, threaded=True)
