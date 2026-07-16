#py -m streamlit run app.py


import streamlit as st
from rewriter import (
    rewrite_text,
    back_translate,
    verify_meaning
)

st.set_page_config(
    page_title="ToneShift",
    page_icon="📝",
    layout="wide"
)

st.title("📝 ToneShift")
st.caption("Rewrite text while preserving its original meaning.")
st.divider()

# -----------------------------
# Session State
# -----------------------------

if "rewritten_text" not in st.session_state:
    st.session_state["rewritten_text"] = ""

if "back_translation" not in st.session_state:
    st.session_state["back_translation"] = ""

if "similarity" not in st.session_state:
    st.session_state["similarity"] = None

if "status" not in st.session_state:
    st.session_state["status"] = ""

if "drift" not in st.session_state:
    st.session_state["drift"] = ""

if "reason" not in st.session_state:
    st.session_state["reason"] = ""

# -----------------------------
# Labels
# -----------------------------

length_labels = {
    1: "⚡ Extremely Concise",
    2: "✂️ Short",
    3: "📄 Similar to Original",
    4: "📖 Longer",
    5: "📝 Even More???"
}

tone_labels = {
    1: "🧒 Child-Friendly",
    2: "🎓 College Student",
    3: "😊 Casual",
    4: "💼 Professional",
    5: "🏛️ Executive"
}

fun_mode_labels = {
    0: "Off",
    1: "🤓 Nerd Mode",
    2: "🪶 Shakespearean"
}

left, right = st.columns(2, gap="large")

# -----------------------------
# Left Panel
# -----------------------------

with left:

    st.subheader("📝 Original Text")

    user_text = st.text_area(
        "",
        height=320,
        placeholder="Paste or type your text here...",
        label_visibility="collapsed",
        key="input_text"
    )

    st.subheader("Length")

    if st.session_state.get("fun_mode", 0) == 0:

        length = st.select_slider(
            "",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.get("length_slider", 3),
            format_func=lambda x: length_labels[x],
            label_visibility="collapsed",
            key="length_slider"
        )

    else:

        length = 3

        st.info(
            "🔒 **Length is locked to 'Similar to Original' while a Fun Mode is active.**"
        )

    st.subheader("Tone")

    if st.session_state.get("fun_mode", 0) == 0:

        tone = st.select_slider(
            "",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.get("tone_slider", 3),
            format_func=lambda x: tone_labels[x],
            label_visibility="collapsed",
            key="tone_slider"
        )

    else:

        tone = st.session_state.get("tone_slider", 3)

        st.info(
            "🔒 **Tone selection is hidden while you are having fun.**"
        )

    st.subheader("🦝 Questionable Modes")

    fun_mode = st.radio(
        "",
        options=[0, 1, 2],
        index=st.session_state.get("fun_mode", 0),
        horizontal=True,
        format_func=lambda x: fun_mode_labels[x],
        label_visibility="collapsed",
        key="fun_mode"
    )

    st.caption(
        "⚠ **Fun Modes override Tone and lock Length to 'Similar to Original'.**"
    )

    if fun_mode != 0:
        tone = 5 + fun_mode
        length = 3

    rewrite = st.button(
        "✨ Rewrite",
        use_container_width=True,
        key="rewrite_button"
    )

# -----------------------------
# Rewrite Pipeline
# -----------------------------

if rewrite:

    if user_text.strip():

        with st.spinner("Rewriting text..."):

            rewritten = rewrite_text(
                text=user_text,
                length=length,
                tone=tone
            )

            st.session_state["rewritten_text"] = rewritten

        with st.spinner("Generating back translation..."):

            back_text = back_translate(
                rewritten
            )

            st.session_state["back_translation"] = back_text

        with st.spinner("Analyzing meaning..."):

            result = verify_meaning(
                original=user_text,
                rewritten=back_text
            )

            st.session_state["similarity"] = result.get(
                "similarity",
                0
            )

            st.session_state["status"] = result.get(
                "status",
                "Unknown"
            )

            st.session_state["drift"] = result.get(
                "drift",
                "Unknown"
            )

            st.session_state["reason"] = result.get(
                "reason",
                ""
            )

    else:

        st.warning("Please enter some text before rewriting.")


# -----------------------------
# Right Panel
# -----------------------------

with right:

    st.subheader("✨ Rewritten Text")

    rewritten_container = st.container(border=True)

    with rewritten_container:

        if st.session_state["rewritten_text"]:

            st.markdown(st.session_state["rewritten_text"])

        else:

            st.caption("Your rewritten text will appear here.")

    st.subheader("🔄 Back Translation")

    back_container = st.container(border=True)

    with back_container:

        if st.session_state["back_translation"]:

            st.markdown(st.session_state["back_translation"])

        else:

            st.caption("The back-translated text will appear here.")

# -----------------------------
# Meaning Analysis
# -----------------------------

st.divider()

st.subheader("🔍 Meaning Analysis")

if st.session_state["similarity"] is not None:

    # Similarity Score
    st.metric(
        label="Semantic Similarity",
        value=f"{st.session_state['similarity']}%"
    )

    st.markdown("---")

    # Status
    status = st.session_state["status"]

    if status == "Meaning Preserved":
        st.success(f"✅ **Status:** {status}")

    elif status == "Minor Changes":
        st.warning(f"⚠️ **Status:** {status}")

    else:
        st.error(f"❌ **Status:** {status}")

    # Drift
    drift = st.session_state["drift"]

    if drift == "Low Drift":
        st.success(f"🟢 **Meaning Drift:** {drift}")

    elif drift == "Moderate Drift":
        st.warning(f"🟡 **Meaning Drift:** {drift}")

    else:
        st.error(f"🔴 **Meaning Drift:** {drift}")

    # Reason
    if st.session_state["reason"]:

        st.info(
            f"**Reason:**\n\n{st.session_state['reason']}"
        )

else:

    st.info(
        "Rewrite some text to analyze semantic similarity and meaning preservation."
    )