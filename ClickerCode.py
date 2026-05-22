import streamlit as st
import random
import time

st.set_page_config(page_title="Asian Life Simulator", layout="centered")

WORLD_SIZE = 11
PRESSURE_INTERVAL = 180
PRESSURE_DURATION = 120

# =========================================================
# GLOBAL CSS (FULL UI OVERHAUL)
# =========================================================
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }

    .game-container {
        background: #0b0f17;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #222;
        box-shadow: 0 0 20px rgba(0,0,0,0.4);
    }

    .header {
        text-align: center;
        padding: 18px;
        border-radius: 14px;
        background: linear-gradient(90deg, #111, #1b1b1b);
        margin-bottom: 15px;
    }

    .hud {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 10px 0;
    }

    .card {
        background: #151a22;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 12px;
        text-align: center;
    }

    .bar {
        width: 100%;
        background: #222;
        border-radius: 10px;
        overflow: hidden;
        height: 12px;
        margin-top: 5px;
    }

    .fill-hp {
        height: 100%;
        background: linear-gradient(90deg, #ff4b4b, #ff0000);
    }

    .fill-hunger {
        height: 100%;
        background: linear-gradient(90deg, #ffd000, #ff8c00);
    }

    .map {
        font-family: monospace;
        background: #0a0a0a;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #333;
        text-align: center;
        white-space: pre;
        box-shadow: inset 0 0 10px rgba(0,255,0,0.1);
    }

    .status {
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }

    .danger {
        background: rgba(255,0,0,0.15);
        border: 1px solid red;
    }

    .safe {
        background: rgba(0,255,0,0.08);
        border: 1px solid #2ecc71;
    }

    button {
        border-radius: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# INIT
# =========================================================
def init():
    defaults = {
        "x": 5,
        "y": 5,

        "iq": 50,
        "stress": 20,
        "happiness": 50,
        "money": 0,
        "grade": 70,

        "hunger": 100,
        "hp": 100,

        "message": "You were born into the system 🏫",

        "pressure_active": False,
        "last_pressure_time": time.time(),
        "pressure_start_time": 0,
        "pressure_type": None,

        "food": [(1,1),(3,7),(6,2),(9,9),(2,8)]
    }

    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# ZONES
# =========================================================
zones = {
    (5,5): "🏠 Home",
    (2,2): "🏫 School",
    (8,2): "📚 Tuition",
    (2,8): "🌳 Park",
    (8,8): "🏙️ City",
}

# =========================================================
# CLAMP
# =========================================================
def clamp():
    st.session_state.hp = max(0, min(100, st.session_state.hp))
    st.session_state.hunger = max(0, min(100, st.session_state.hunger))
    st.session_state.happiness = max(0, min(100, st.session_state.happiness))
    st.session_state.stress = max(0, min(200, st.session_state.stress))

# =========================================================
# MOVE
# =========================================================
def move(dx, dy):
    st.session_state.x = max(0, min(WORLD_SIZE-1, st.session_state.x+dx))
    st.session_state.y = max(0, min(WORLD_SIZE-1, st.session_state.y+dy))
    st.session_state.hunger -= 1
    st.session_state.stress += 1
    check_food()

# =========================================================
# FOOD
# =========================================================
def check_food():
    pos = (st.session_state.x, st.session_state.y)
    if pos in st.session_state.food:
        st.session_state.food.remove(pos)
        st.session_state.hunger += 25
        st.session_state.hp += 10
        st.session_state.message = "🍜 You ate food"

# =========================================================
# PRESSURE SYSTEM
# =========================================================
def pressure():
    now = time.time()

    if not st.session_state.pressure_active:
        if now - st.session_state.last_pressure_time > PRESSURE_INTERVAL:
            st.session_state.pressure_active = True
            st.session_state.pressure_start_time = now
            st.session_state.pressure_type = random.choice([
                "📚 Exam Week",
                "🧑‍🏫 Tuition Overload",
                "👨‍👩‍👧 Parental Expectations",
            ])

    else:
        if now - st.session_state.pressure_start_time > PRESSURE_DURATION:
            st.session_state.pressure_active = False
            st.session_state.last_pressure_time = now

# =========================================================
# EFFECTS
# =========================================================
def effects():
    st.session_state.hunger -= 0.2

    if st.session_state.hunger < 20:
        st.session_state.hp -= 0.4

    if st.session_state.pressure_active:
        st.session_state.stress += 0.4

# =========================================================
# MAP
# =========================================================
def draw_map():
    out = ""
    for y in range(WORLD_SIZE):
        for x in range(WORLD_SIZE):

            if (x,y) == (st.session_state.x, st.session_state.y):
                out += "🧍"
            elif (x,y) in st.session_state.food:
                out += "🍜"
            elif (x,y) in zones:
                out += "🏫"
            else:
                out += "⬜"
        out += "\n"
    return out

# =========================================================
# GAME LOOP
# =========================================================
pressure()
effects()
clamp()

# =========================================================
# HEADER (HTML)
# =========================================================
st.markdown(
    """
    <div class="header">
        <h1>🎓 Asian Life Simulator</h1>
        <p style="color:#aaa;">Survive pressure, hunger, and expectations</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# STATUS PANEL
# =========================================================
st.markdown(f"<div class='game-container'>", unsafe_allow_html=True)

st.markdown(f"### 📍 {zones.get((st.session_state.x,st.session_state.y),'🟫 Street')}")
st.write(st.session_state.message)

# =========================================================
# PRESSURE STATUS
# =========================================================
if st.session_state.pressure_active:
    st.markdown(
        f"""
        <div class="status danger">
            ⚠️ {st.session_state.pressure_type}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="status safe">
            🙂 Normal Life
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# HUD (HTML STATS)
# =========================================================
hp_bar = int(st.session_state.hp)
hg_bar = int(st.session_state.hunger)

st.markdown(
f"""
<div class="hud">

<div class="card">
<b>❤️ HP</b>
<div class="bar"><div class="fill-hp" style="width:{hp_bar}%"></div></div>
</div>

<div class="card">
<b>🍗 Hunger</b>
<div class="bar"><div class="fill-hunger" style="width:{hg_bar}%"></div></div>
</div>

<div class="card"><b>😰 Stress</b><br>{int(st.session_state.stress)}</div>
<div class="card"><b>📊 Grade</b><br>{int(st.session_state.grade)}</div>

</div>
""",
unsafe_allow_html=True
)

# =========================================================
# MAP (HTML)
# =========================================================
st.markdown(f"<div class='map'>{draw_map()}</div>", unsafe_allow_html=True)

# =========================================================
# MOVEMENT
# =========================================================
st.markdown("### 🧭 Movement")

c1,c2,c3 = st.columns(3)

with c1:
    if st.button("⬅️"):
        move(-1,0); st.rerun()
    if st.button("⬇️"):
        move(0,1); st.rerun()

with c2:
    if st.button("⬆️"):
        move(0,-1); st.rerun()

with c3:
    if st.button("➡️"):
        move(1,0); st.rerun()

# =========================================================
# ACTIONS
# =========================================================
st.markdown("### 🎮 Actions")

zone = zones.get((st.session_state.x,st.session_state.y),"Street")

if zone == "🏠 Home":
    if st.button("😴 Rest"):
        st.session_state.hp += 10
        st.session_state.hunger -= 2
        st.rerun()

elif zone == "🏙️ City":
    if st.button("💼 Work"):
        st.session_state.money += random.randint(10,50)
        st.session_state.hunger -= 5
        st.rerun()

# =========================================================
# ENDINGS
# =========================================================
st.markdown("---")

if st.session_state.hp <= 0:
    st.error("💀 TOTAL FAILURE ENDING")

elif st.session_state.happiness <= 5:
    st.warning("😐 EMOTIONAL DAMAGE ENDING")

st.markdown("</div>", unsafe_allow_html=True)
