import streamlit as st
# =====================================
if st.button("😴 Sleep"):

    st.session_state.energy += 30
    st.session_state.happiness += 5

    if st.session_state.energy > 100:
        st.session_state.energy = 100

    st.session_state.message = (
        "You slept peacefully... until parents wake you up for more studying."
    )

    check_status()
    st.rerun()

# =====================================
# AGE UP
# =====================================
st.markdown("---")

if st.button("🎂 Next Year"):

    st.session_state.age += 1
    st.session_state.grade += 1

    st.session_state.energy -= 10

    event = random.choice([
        "You got compared to cousin again.",
        "Parents ask why you not doctor yet.",
        "You got 99%. Parents ask where 1% went.",
        "You attend another tutoring center.",
        "Grandma says you too skinny.",
        "Parents say failure is not option.",
        "You won math competition.",
        "You got another homework packet.",
    ])

    st.session_state.message = event

    # Random stat changes
    st.session_state.intelligence += random.randint(1, 8)
    st.session_state.happiness -= random.randint(1, 5)

    # Clamp stats
    st.session_state.happiness = max(0, st.session_state.happiness)
    st.session_state.energy = max(0, st.session_state.energy)

    check_status()

    st.rerun()

# =====================================
# GAME OVER
# =====================================
if st.session_state.age >= 30:

    st.markdown("---")
    st.subheader("🏆 Final Result")

    if st.session_state.intelligence >= 200:
        st.success("You became a legendary doctor. Parents finally proud.")

    elif st.session_state.intelligence >= 170:
        st.success("You became an engineer. Parents accept you.")

    elif st.session_state.intelligence >= 140:
        st.warning("You became accountant. Acceptable.")

    else:
        st.error("EMOTIONAL DAMAGE! You became disappointment.")

    st.stop()

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.caption("Inspired by Steven He comedy videos")
