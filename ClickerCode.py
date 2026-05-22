import streamlit as st
import random

# -----------------------------
# GAME STATE INIT
# -----------------------------
if "distance" not in st.session_state:
    st.session_state.distance = 10  # teacher distance (0 = caught)

if "level" not in st.session_state:
    st.session_state.level = 1

if "weapon" not in st.session_state:
    st.session_state.weapon = None

if "damage" not in st.session_state:
    st.session_state.damage = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "message" not in st.session_state:
    st.session_state.message = ""


# -----------------------------
# QUESTION GENERATOR
# -----------------------------
def generate_question(level):
    if level == 1:
        n = random.randint(5, 8)
        r = random.randint(2, 4)
        q = f"How many permutations of {n} items taken {r} at a time?"
        a = factorial(n) // factorial(n - r)

    elif level == 2:
        n = random.randint(6, 10)
        r = random.randint(2, 5)
        q = f"How many combinations of {n} items taken {r} at a time?"
        a = factorial(n) // (factorial(r) * factorial(n - r))

    else:
        n = random.randint(5, 9)
        r = random.randint(2, 5)
        q = f"In how many ways can you arrange {r} items from {n} distinct items in a circle?"
        a = factorial(r - 1) * combination(n, r)

    return q, a


def factorial(x):
    return 1 if x == 0 else x * factorial(x - 1)


def combination(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))


# -----------------------------
# WEAPON SYSTEM
# -----------------------------
def get_weapon():
    weapons = [
        ("Pencil Sword ✏️", 5),
        ("Notebook Shield 📒", 8),
        ("Protractor Blade 📐", 12),
        ("Calculator Cannon 🔢", 20),
        ("Final Exam Laser 💥", 35),
    ]
    return random.choice(weapons)


# -----------------------------
# GAME LOGIC
# -----------------------------
def next_question():
    q, a = generate_question(st.session_state.level)
    st.session_state.question = q
    st.session_state.answer = a


def check_answer(user_answer):
    try:
        user_answer = int(user_answer)
    except:
        st.session_state.message = "❌ Invalid input!"
        return

    if user_answer == st.session_state.answer:
        st.session_state.message = "✅ Correct! You move forward!"

        st.session_state.distance += 1
        st.session_state.level += 1

        # reward weapon
        weapon, dmg = get_weapon()
        st.session_state.weapon = weapon
        st.session_state.damage = dmg

        st.session_state.message += f" You picked up {weapon} (Damage {dmg})"

    else:
        st.session_state.message = "❌ Wrong! Teacher is getting closer!"
        st.session_state.distance -= 2


# -----------------------------
# UI
# -----------------------------
st.title("🏫 Permutation & Combination Escape Game")
st.write("A teacher is chasing you! Answer correctly to escape and collect weapons.")

st.progress(st.session_state.distance / 20)

st.write(f"👨‍🏫 Teacher Distance: {st.session_state.distance}")
st.write(f"📊 Level: {st.session_state.level}")

if st.session_state.distance <= 0:
    st.error("💀 You got caught by the teacher!")
    st.stop()

if st.session_state.distance >= 20:
    st.success("🎉 You escaped the school!")
    st.stop()

if st.session_state.question is None:
    next_question()

st.subheader("🧠 Question")
st.write(st.session_state.question)

user_answer = st.text_input("Your Answer:")

if st.button("Submit"):
    check_answer(user_answer)
    next_question()

st.write(st.session_state.message)

# -----------------------------
# FINAL ESCAPE MODE
# -----------------------------
if st.session_state.level > 5:
    st.markdown("## 🔥 Final Boss: Teacher Attack Mode")

    st.write("Use your weapon to fight back!")

    if st.button("Attack Teacher"):
        damage = st.session_state.damage
        st.session_state.distance += damage // 5
        st.success(f"You attacked using {st.session_state.weapon} dealing {damage} damage!")
