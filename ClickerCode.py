import streamlit as st
import time
import json
from pathlib import Path

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="Cookie Clicker",
    page_icon="🍪",
    layout="centered"
)

SAVE_FILE = "cookie_save.json"

# ==========================================
# LOAD GAME
# ==========================================
def load_game():

    default_data = {
        "cookies": 0,
        "cookies_per_click": 1,
        "auto_clickers": 0,
        "farms": 0,
        "last_tick": time.time()
    }

    try:
        if Path(SAVE_FILE).exists():

            with open(SAVE_FILE, "r") as f:

                content = f.read().strip()

                # Prevent empty file crash
                if not content:
                    return default_data

                return json.loads(content)

    except json.JSONDecodeError:
        # Corrupted save file
        return default_data

    except Exception as e:
        st.error(f"Save file error: {e}")
        return default_data

    return default_data

# ==========================================
# SAVE GAME
# ==========================================
def save_game():

    data = {
        "cookies": st.session_state.cookies,
        "cookies_per_click": st.session_state.cookies_per_click,
        "auto_clickers": st.session_state.auto_clickers,
        "farms": st.session_state.farms,
        "last_tick": time.time()
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
if "initialized" not in st.session_state:

    game = load_game()

    st.session_state.cookies = game["cookies"]
    st.session_state.cookies_per_click = game["cookies_per_click"]
    st.session_state.auto_clickers = game["auto_clickers"]
    st.session_state.farms = game["farms"]
    st.session_state.last_tick = game["last_tick"]

    st.session_state.initialized = True

# ==========================================
# PASSIVE INCOME
# ==========================================
now = time.time()

elapsed = now - st.session_state.last_tick

income_per_second = (
    st.session_state.auto_clickers * 1 +
    st.session_state.farms * 5
)

# Add passive cookies
st.session_state.cookies += income_per_second * elapsed

# Update timer
st.session_state.last_tick = now

# ==========================================
# CSS STYLING
# ==========================================
st.markdown("""
<style>

body {
    background-color: #f7e7ce;
}

.main-title {
    text-align: center;
    font-size: 65px;
    font-weight: bold;
    color: #5c3b1e;
    margin-bottom: 10px;
}

.cookie-counter {
    text-align: center;
    font-size: 42px;
    color: #3d2514;
    margin-bottom: 25px;
}

.shop-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

div.stButton > button:first-child {
    font-size: 90px;
    height: 200px;
    width: 200px;
    border-radius: 50%;
    border: none;
    background-color: #c97a3d;
    transition: 0.1s ease-in-out;
}

div.stButton > button:first-child:hover {
    transform: scale(1.05);
}

div.stButton > button:first-child:active {
    transform: scale(0.95);
}

.small-text {
    text-align: center;
    color: gray;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown(
    "<div class='main-title'>🍪 Cookie Clicker</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='cookie-counter'>{int(st.session_state.cookies)} Cookies</div>",
    unsafe_allow_html=True
)

# ==========================================
# COOKIE BUTTON
# ==========================================
left, center, right = st.columns([1,2,1])

with center:

    if st.button("🍪"):
        st.session_state.cookies += st.session_state.cookies_per_click
        save_game()
        st.rerun()

# ==========================================
# STATS
# ==========================================
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric("Cookies Per Click", st.session_state.cookies_per_click)

with col2:
    st.metric("Passive Income", f"{income_per_second}/sec")

# ==========================================
# SHOP
# ==========================================
st.markdown("---")
st.subheader("🛒 Shop")

# ==========================================
# AUTO CLICKER
# ==========================================
auto_clicker_cost = 50 + (st.session_state.auto_clickers * 20)

st.markdown("<div class='shop-box'>", unsafe_allow_html=True)

st.markdown(f"""
### 🤖 Auto Clicker

Generates **1 cookie/sec**

Owned: **{st.session_state.auto_clickers}**

Cost: **{auto_clicker_cost}**
""")

if st.button("Buy Auto Clicker"):

    if st.session_state.cookies >= auto_clicker_cost:

        st.session_state.cookies -= auto_clicker_cost
        st.session_state.auto_clickers += 1

        save_game()
        st.rerun()

    else:
        st.warning("Not enough cookies!")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FARM
# ==========================================
farm_cost = 250 + (st.session_state.farms * 100)

st.markdown("<div class='shop-box'>", unsafe_allow_html=True)

st.markdown(f"""
### 🌾 Cookie Farm

Generates **5 cookies/sec**

Owned: **{st.session_state.farms}**

Cost: **{farm_cost}**
""")

if st.button("Buy Farm"):

    if st.session_state.cookies >= farm_cost:

        st.session_state.cookies -= farm_cost
        st.session_state.farms += 1

        save_game()
        st.rerun()

    else:
        st.warning("Not enough cookies!")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CLICK UPGRADE
# ==========================================
upgrade_cost = 100 + (st.session_state.cookies_per_click * 50)

st.markdown("<div class='shop-box'>", unsafe_allow_html=True)

st.markdown(f"""
### ⚡ Stronger Clicks

+1 cookie per click

Current Power: **{st.session_state.cookies_per_click}**

Cost: **{upgrade_cost}**
""")

if st.button("Upgrade Click Power"):

    if st.session_state.cookies >= upgrade_cost:

        st.session_state.cookies -= upgrade_cost
        st.session_state.cookies_per_click += 1

        save_game()
        st.rerun()

    else:
        st.warning("Not enough cookies!")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# SAVE GAME
# ==========================================
save_game()

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")

st.markdown(
    "<div class='small-text'>Made with Streamlit 🍪</div>",
    unsafe_allow_html=True
)
