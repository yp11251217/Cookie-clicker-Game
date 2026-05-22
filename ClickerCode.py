import streamlit as st
import time
import json
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Cookie Clicker",
    page_icon="🍪",
    layout="centered"
)

# -----------------------------
# Save System
# -----------------------------
SAVE_FILE = "cookie_save.json"

def load_game():
    if Path(SAVE_FILE).exists():
        with open(SAVE_FILE, "r") as f:
            return json.load(f)

    return {
        "cookies": 0,
        "cookies_per_click": 1,
        "auto_clickers": 0,
        "farms": 0,
        "last_update": time.time()
    }

def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

game = load_game()

# -----------------------------
# Offline Progress
# -----------------------------
now = time.time()
elapsed = now - game["last_update"]

passive_income = (
    game["auto_clickers"] * 1 +
    game["farms"] * 5
)

offline_cookies = int(elapsed * passive_income)

if offline_cookies > 0:
    game["cookies"] += offline_cookies

game["last_update"] = now

# -----------------------------
# Session State
# -----------------------------
if "cookies" not in st.session_state:
    st.session_state.cookies = game["cookies"]

if "cookies_per_click" not in st.session_state:
    st.session_state.cookies_per_click = game["cookies_per_click"]

if "auto_clickers" not in st.session_state:
    st.session_state.auto_clickers = game["auto_clickers"]

if "farms" not in st.session_state:
    st.session_state.farms = game["farms"]

# -----------------------------
# Auto Income
# -----------------------------
auto_income = (
    st.session_state.auto_clickers * 1 +
    st.session_state.farms * 5
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #f5e6d3;
}

.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: #5b3a29;
}

.cookie-count {
    text-align: center;
    font-size: 40px;
    margin-bottom: 20px;
    color: #3d2a1f;
}

.big-cookie {
    font-size: 120px;
    text-align: center;
    cursor: pointer;
    user-select: none;
    transition: transform 0.1s;
}

.big-cookie:hover {
    transform: scale(1.08);
}

.shop-card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    "<div class='main-title'>🍪 Cookie Clicker</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='cookie-count'>{int(st.session_state.cookies)} Cookies</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Cookie Button
# -----------------------------
cookie_col = st.columns([1,2,1])[1]

with cookie_col:
    if st.button("🍪", use_container_width=True):
        st.session_state.cookies += st.session_state.cookies_per_click

# -----------------------------
# Passive Income
# -----------------------------
st.info(f"""
Cookies Per Click: {st.session_state.cookies_per_click}

Passive Income: {auto_income} cookies/sec
""")

# -----------------------------
# Shop
# -----------------------------
st.subheader("🛒 Shop")

# Auto Clicker
auto_clicker_cost = 50 + (st.session_state.auto_clickers * 20)

st.markdown("<div class='shop-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(f"""
### 🤖 Auto Clicker
Generates 1 cookie/sec

Owned: {st.session_state.auto_clickers}

Cost: {auto_clicker_cost}
""")

with col2:
    if st.button("Buy Auto Clicker"):
        if st.session_state.cookies >= auto_clicker_cost:
            st.session_state.cookies -= auto_clicker_cost
            st.session_state.auto_clickers += 1

st.markdown("</div>", unsafe_allow_html=True)

# Farm
farm_cost = 250 + (st.session_state.farms * 100)

st.markdown("<div class='shop-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(f"""
### 🌾 Cookie Farm
Generates 5 cookies/sec

Owned: {st.session_state.farms}

Cost: {farm_cost}
""")

with col2:
    if st.button("Buy Farm"):
        if st.session_state.cookies >= farm_cost:
            st.session_state.cookies -= farm_cost
            st.session_state.farms += 1

st.markdown("</div>", unsafe_allow_html=True)

# Upgrade Click Power
upgrade_cost = 100 + (st.session_state.cookies_per_click * 50)

st.markdown("<div class='shop-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(f"""
### ⚡ Stronger Clicks
+1 cookie per click

Current Power: {st.session_state.cookies_per_click}

Cost: {upgrade_cost}
""")

with col2:
    if st.button("Upgrade Click"):
        if st.session_state.cookies >= upgrade_cost:
            st.session_state.cookies -= upgrade_cost
            st.session_state.cookies_per_click += 1

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Auto Update Cookies
# -----------------------------
st.session_state.cookies += auto_income * 0.1

# -----------------------------
# Save Game
# -----------------------------
save_data = {
    "cookies": st.session_state.cookies,
    "cookies_per_click": st.session_state.cookies_per_click,
    "auto_clickers": st.session_state.auto_clickers,
    "farms": st.session_state.farms,
    "last_update": time.time()
}

save_game(save_data)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Made with Streamlit 🍪")

# Auto refresh every 100ms
time.sleep(0.1)
st.rerun()
