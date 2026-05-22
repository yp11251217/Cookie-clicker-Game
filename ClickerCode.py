import streamlit as st
import random
import time
from PIL import Image
import os

# =========================================================
# SETUP
# =========================================================
st.set_page_config(layout="centered")

WORLD_SIZE = 12
VIEW = 5
ASSET = "assets"

# =========================================================
# LOAD SPRITES
# =========================================================
@st.cache_data
def img(name):
    return Image.open(os.path.join(ASSET, name)).resize((48, 48))

player = img("player.png")
grass = img("grass.png")
home = img("home.png")
school = img("school.png")
park = img("park.png")
city = img("city.png")

npc_student = img("npc_student.png")
npc_teacher = img("npc_teacher.png")

# =========================================================
# INIT
# =========================================================
def init():
    defaults = {
        "x": 6,
        "y": 6,

        "iq": 50,
        "stress": 20,
        "happiness": 50,

        "dialogue": "You wake up in a competitive world...",
        "last_event": time.time(),

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
# WORLD TILES
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

    return (
        max(0, cx - half),
        min(WORLD_SIZE - 1, cx + half),
        max(0, cy - half),
        min(WORLD_SIZE - 1, cy + half),
    )

# =========================================================
# MOVEMENT (RPG STEP FEEL)
# =========================================================
def move(dx, dy):
    st.session_state.x = max(0, min(WORLD_SIZE - 1, st.session_state.x + dx))
    st.session_state.y = max(0, min(WORLD_SIZE - 1, st.session_state.y + dy))

    st.session_state.stress += 1

    st.session_state.dialogue = "You move through the world..."

# =========================================================
# NPC CHECK
# =========================================================
def npc_at(x, y):
    return st.session_state.npc.get((x, y), None)

# =========================================================
# INTERACTION SYSTEM (RPG CORE)
# =========================================================
def interact():
    x, y = st.session_state.x, st.session_state.y
    npc = npc_at(x, y)

    if npc == "student":
        st.session_state.dialogue = "Student: 'I studied 12 hours yesterday...'"
        st.session_state.stress += 2

    elif npc == "teacher":
        st.session_state.dialogue = "Teacher: 'Why is your score not 100?'"
        st.session_state.stress += 5

    elif get_tile(x, y) == school:
        st.session_state.dialogue = "You attend a silent competitive class."
        st.session_state.iq += 2
        st.session_state.stress += 2

    elif get_tile(x, y) == home:
        st.session_state.dialogue = "Home feels quiet... but expectations remain."
        st.session_state.happiness += 1

    else:
        st.session_state.dialogue = "Nothing happens..."

# =========================================================
# RENDER WORLD (RPG CAMERA VIEW)
# =========================================================
def render():
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
st.title("🎮 Asian Life RPG")

st.write("🧭 Explore the world. Interact. Survive expectations.")

draw(render())

# =========================================================
# CONTROLS (RPG STYLE)
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
# ACTIONS (RPG BUTTON)
# =========================================================
st.markdown("### 🎮 Actions")

if st.button("🗣️ Interact"):
    interact()
    st.rerun()

# =========================================================
# RPG DIALOGUE BOX
# =========================================================
st.markdown("---")

st.markdown("### 📜 Story")
st.info(st.session_state.dialogue)

# =========================================================
# STATS (RPG HUD)
# =========================================================
st.markdown("### 📊 Status")

col1, col2, col3 = st.columns(3)

col1.metric("🧠 IQ", st.session_state.iq)
col2.metric("😰 Stress", st.session_state.stress)
col3.metric("😊 Happiness", st.session_state.happiness)
