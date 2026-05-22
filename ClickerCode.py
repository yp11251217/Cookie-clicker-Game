import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(layout="wide")

# -----------------------------
# P&C QUESTION ENGINE (STREAMLIT SIDE)
# -----------------------------
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

def generate_question():
    n = random.randint(5, 8)
    r = random.randint(2, 4)

    question = f"How many permutations of {n} items taken {r} at a time?"
    answer = factorial(n) // factorial(n - r)

    return question, answer


if "q" not in st.session_state:
    st.session_state.q, st.session_state.a = generate_question()

if "weapon_power" not in st.session_state:
    st.session_state.weapon_power = 0


# -----------------------------
# UI PANEL (STREAMLIT)
# -----------------------------
st.title("🏫 AI Teacher Chase Escape Game")

st.write("Answer correctly to help your character escape the AI teacher!")

st.subheader("🧠 Question")
st.write(st.session_state.q)

user = st.text_input("Your Answer")

if st.button("Submit Answer"):
    if user.isdigit() and int(user) == st.session_state.a:
        st.success("Correct! You got a weapon upgrade 🔫")
        st.session_state.weapon_power += 10
        st.session_state.q, st.session_state.a = generate_question()
    else:
        st.error("Wrong! Teacher gets closer 😈")


# -----------------------------
# HTML + JS GAME ENGINE
# -----------------------------
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin: 0;
    overflow: hidden;
    background: #111;
    font-family: Arial;
}}

#game {{
    position: relative;
    width: 100%;
    height: 500px;
    background: linear-gradient(#222, #000);
    border: 2px solid white;
}}

.player {{
    position: absolute;
    width: 40px;
    height: 40px;
    background: cyan;
    border-radius: 50%;
    top: 250px;
    left: 100px;
}}

.teacher {{
    position: absolute;
    width: 50px;
    height: 50px;
    background: red;
    border-radius: 50%;
    top: 250px;
    left: 10px;
}}

.weapon {{
    position: absolute;
    width: 20px;
    height: 20px;
    background: yellow;
    border-radius: 50%;
    top: 200px;
    left: 400px;
}}

#hud {{
    color: white;
    padding: 10px;
}}
</style>
</head>

<body>

<div id="hud">
    <h3>🏃 AI Teacher Chase</h3>
    <p>Use Arrow Keys → Move | Teacher AI is chasing you</p>
</div>

<div id="game">
    <div class="player" id="player"></div>
    <div class="teacher" id="teacher"></div>
    <div class="weapon" id="weapon"></div>
</div>

<script>
let player = document.getElementById("player");
let teacher = document.getElementById("teacher");
let weapon = document.getElementById("weapon");

let px = 100;
let tx = 10;
let speed = 4;
let teacherSpeed = 2 + {st.session_state.weapon_power/10};

document.addEventListener("keydown", function(e) {{
    if(e.key === "ArrowRight") px += speed;
    if(e.key === "ArrowLeft") px -= speed;
}});

// AI Teacher Chase Logic
function gameLoop() {{
    // teacher follows player
    if(tx < px) {{
        tx += teacherSpeed;
    }} else {{
        tx -= teacherSpeed * 0.5;
    }}

    // update positions
    player.style.left = px + "px";
    teacher.style.left = tx + "px";

    // collision check
    if(Math.abs(px - tx) < 30) {{
        alert("💀 Teacher caught you!");
        px = 100;
        tx = 10;
    }}

    requestAnimationFrame(gameLoop);
}}

gameLoop();
</script>

</body>
</html>
"""

components.html(html_code, height=600)
