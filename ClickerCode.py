import streamlit as st
import os
import time
import random
from PIL import Image

# =========================================================
# SETUP
# =========================================================
st.set_page_config(page_title="Asian Life RPG", layout="centered")

WORLD_SIZE = 12
VIEW = 5
ASSET = "assets"

# =========================================================
# SAFE IMAGE LOADER (NO CRASH VERSION)
# =========================================================
@st.cache_data
def img(name):
    path = os.path.join(ASSET, name)

    if not os.path.exists(path):
        # fallback placeholder tile (prevents crash)
        return Image.new("RGB", (48, 48), (200, 50, 50))

    return Image.open(path).resize((48, 48))

# =========================================================
# SPRITES
# =========================================================
player = img("player.png")
grass = img("grass.png")
home = img("home.png")
school = img("school.png")
park = img("park.png")
city = img("city.png")

npc_student = img("npc_student.png")
npc_teacher = img("npc_teacher.png")

# =========================================================
# INIT STATE
# =========================================================
def init():
    defaults = {
        "x": 6,
        "y": 6,

        "iq": 50,
        "stress": 20,
        "happiness": 50,

        "dialogue": "You enter a competitive life world...",

        "npc": {
            (3, 3): "student",
            (8, 8): "teacher",
        }
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# ZONES (MAP TILES)
# =========================================================
zones = {
    (2, 2): school,
    (6, 6): home,
    (9, 2): school,
    (2, 9): park,
    (9, 9): city,
}

def get_tile(x, y):
    return zones.get((x, y), grass)

# =========================================================
# CAMERA SYSTEM (RPG FEEL)
# =========================================================
def camera():
    half = VIEW // 2
    cx, cy = st.session_state.x, st.session_state.y

    minx = max(0, cx - half)
    maxx = min(WORLD_SIZE - 1, cx + half)
    miny = max(0, cy - half)
    maxy = min(WORLD_SIZE - 1, cy + half)

    return minx, maxx, miny, maxy

# =========================================================
# MOVE SYSTEM
# =========================================================
def move(dx, dy):
    st.session_state.x = max(0, min(WORLD_SIZE - 1, st.session_state.x + dx))
    st.session_state.y = max(0, min(WORLD_SIZE - 1, st.session_state.y + dy))

    st.session_state.stress += 1
    st.session_state.dialogue = "You move through life..."

# =========================================================
# NPC SYSTEM
# =========================================================
def npc_at(x, y):
    return st.session_state.npc.get((x, y), None)

# =========================================================
# INTERACTION SYSTEM
# =========================================================
def interact():
    x, y = st.session_state.x, st.session_state.y
    npc = npc_at(x, y)
    tile = get_tile(x, y)

    if npc == "student":
        st.session_state.dialogue = "Student: 'I studied 10 hours yesterday...'"
        st.session_state.stress += 2

    elif npc == "teacher":
        st.session_state.dialogue = "Teacher: 'Why not 100 marks?'"
        st.session_state.stress += 5

    elif tile == school:
        st.session_state.dialogue = "You attend class. Pressure builds."
        st.session_state.iq += 2
        st.session_state.stress += 2

    elif tile == home:
        st.session_state.dialogue = "Home feels quiet but expectations remain."
        st.session_state.happiness += 1

    elif tile == park:
        st.session_state.dialogue = "You feel slightly relieved."
        st.session_state.happiness += 3
        st.session_state.stress -= 2

    else:
        st.session_state.dialogue = "Nothing important happens."

# =========================================================
# RENDER WORLD (CAMERA VIEW)
# =========================================================
def render_world():
    minx, maxx, miny, maxy = camera()

    grid = []

    for y in range(miny, maxy + 1):
        row = []

        for x in range(minx, maxx + 1):

            if x == st.session_state.x and y == st.session_state.y:
                row.append(player)

            elif (x, y) in st.session_state.npc:
                if st.session_state.npc[(x, y)] == "student":
                    row.append(npc_student)
                else:
                    row.append(npc_teacher)

            else:
                row.append(get_tile(x, y))

        grid.append(row)

    return grid

def draw(grid):
    for row in grid:
        st.image(row)

# =========================================================
# UI
# =========================================================
st.title("🎮 Asian Life RPG (Final Version)")

st.write("🧭 Move, interact, and survive expectations.")

draw(render_world())

# =========================================================
# CONTROLS
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⬅️"):
        move(-1, 0)
        st.rerun()

    if st.button("⬇️"):
        move(0, 1)
        st.rerun()

with c2:
    if st.button("⬆️"):
        move(0, -1)
        st.rerun()

with c3:
    if st.button("➡️"):
        move(1, 0)
        st.rerun()

# =========================================================
# ACTIONS
# =========================================================
st.markdown("### 🎮 Actions")

if st.button("🗣️ Interact"):
    interact()
    st.rerun()

# =========================================================
# DIALOGUE BOX
# =========================================================
st.markdown("---")
st.markdown("### 📜 Story")
st.info(st.session_state.dialogue)

# =========================================================
# STATS HUD
# =========================================================
st.markdown("### 📊 Status")

c1, c2, c3 = st.columns(3)
c1.metric("🧠 IQ", st.session_state.iq)
c2.metric("😰 Stress", st.session_state.stress)
c3.metric("😊 Happiness", st.session_state.happiness)
