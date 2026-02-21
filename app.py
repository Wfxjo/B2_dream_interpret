import base64
from pathlib import Path

import streamlit as st
from dream_interpret import (
    interpret_dream,
    extract_image_prompt,
    generate_image,
    add_dream_to_journal,
    load_journal,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a0a1a 100%);
        color: #e0d7f5;
    }
    h1 {
        text-align: center;
        font-size: 3rem !important;
        background: linear-gradient(90deg, #a855f7, #ec4899, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        padding: 1rem 0;
    }
    div[data-testid="stCaptionContainer"] {
        text-align: center;
        color: #9d7fd4;
        font-style: italic;
    }
    textarea {
        background-color: #1a1a2e !important;
        color: #e0d7f5 !important;
        border: 1px solid #6d28d9 !important;
        border-radius: 12px !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #7c3aed, #9d174d);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 1px;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.85;
    }
    .stButton > button[kind="secondary"] {
        background: transparent;
        color: #c084fc;
        border: 1px solid #6d28d9;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #1a1a2e;
        border-color: #a855f7;
        color: #a855f7;
    }
    .interpretation-box {
        background: linear-gradient(135deg, #1a1a2e, #2d1b4e);
        border: 1px solid #6d28d9;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        color: #e0d7f5;
        line-height: 1.8;
    }
    .stExpander {
        background-color: #1a1a2e !important;
        border: 1px solid #4c1d95 !important;
        border-radius: 12px !important;
        margin-bottom: 8px;
    }
    hr {
        border-color: #4c1d95 !important;
        margin: 2rem 0 !important;
    }
    h2, h3 {
        color: #c084fc !important;
        letter-spacing: 2px;
    }
    img {
        border-radius: 16px;
        border: 2px solid #6d28d9;
        margin-top: 12px;
    }
    .little-dreamy-girl-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 8px auto;
    }
    .little-dreamy-girl-container img {
        border: none !important;
        border-radius: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        width: 120px;
        margin: 0;
    }
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .star {
        position: absolute;
        width: 2px;
        height: 2px;
        background: white;
        border-radius: 50%;
        animation: twinkle 3s infinite alternate;
    }
    @keyframes twinkle {
        0%   { opacity: 0; transform: scale(1); }
        100% { opacity: 1; transform: scale(1.5); }
    }
</style>
"""

STARS_HTML = """
<div class="stars">
    <div class="star" style="top:5%;left:10%;animation-delay:0s;"></div>
    <div class="star" style="top:10%;left:20%;animation-delay:0.3s;"></div>
    <div class="star" style="top:15%;left:35%;animation-delay:0.6s;"></div>
    <div class="star" style="top:8%;left:50%;animation-delay:0.9s;"></div>
    <div class="star" style="top:20%;left:65%;animation-delay:1.2s;"></div>
    <div class="star" style="top:5%;left:75%;animation-delay:1.5s;"></div>
    <div class="star" style="top:12%;left:90%;animation-delay:1.8s;"></div>
    <div class="star" style="top:30%;left:5%;animation-delay:0.4s;"></div>
    <div class="star" style="top:40%;left:25%;animation-delay:0.7s;"></div>
    <div class="star" style="top:35%;left:45%;animation-delay:1.0s;"></div>
    <div class="star" style="top:45%;left:60%;animation-delay:1.3s;"></div>
    <div class="star" style="top:38%;left:80%;animation-delay:1.6s;"></div>
    <div class="star" style="top:55%;left:15%;animation-delay:0.2s;"></div>
    <div class="star" style="top:60%;left:30%;animation-delay:0.5s;"></div>
    <div class="star" style="top:50%;left:55%;animation-delay:0.8s;"></div>
    <div class="star" style="top:65%;left:70%;animation-delay:1.1s;"></div>
    <div class="star" style="top:58%;left:88%;animation-delay:1.4s;"></div>
    <div class="star" style="top:75%;left:8%;animation-delay:1.7s;"></div>
    <div class="star" style="top:80%;left:40%;animation-delay:2.0s;"></div>
    <div class="star" style="top:70%;left:95%;animation-delay:2.3s;"></div>
</div>
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_image_as_base64(image_path: str) -> str:
    """
    Load a local image file and convert it to a base64 string.
    Used to embed images directly in HTML without a server path.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# ---------------------------------------------------------------------------
# Journal display
# ---------------------------------------------------------------------------

def display_journal() -> None:
    """
    Load and display all journal entries in reverse chronological order.
    Each entry is shown as a collapsible expander with the date as title,
    revealing the dream text and its interpretation when clicked.
    """
    journal = load_journal()
    if not journal:
        st.info("Your dream journal is empty.")
        return
    st.caption(f"✦ {len(journal)} dream(s) recorded ✦")
    for entry in reversed(journal):
        with st.expander(f"🌙 {entry['date']}"):
            st.markdown("**✨ Dream**")
            st.write(entry["dream"])
            st.markdown("**🔮 Interpretation**")
            st.write(entry["interpretation"])


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Dream Interpreter", page_icon="🌙", layout="centered")

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown(STARS_HTML, unsafe_allow_html=True)

# Display Little Dreamy Girl near the title
little_dreamy_girl_path = Path("littledreamy_girl.png")
if little_dreamy_girl_path.exists():
    little_dreamy_girl_base64 = load_image_as_base64(str(little_dreamy_girl_path))
    st.markdown(
        f'<div class="little-dreamy-girl-container">'
        f'<img src="data:image/png;base64,{little_dreamy_girl_base64}" alt="Little Dreamy Girl"/>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.title("🌙 Dream Interpreter")
st.caption("✦ Learn how to see. Realize that everything connects to everything else ✦")
st.caption("Leonardo Da Vinci")

st.divider()

dream_input = st.text_area(
    "Describe your dream",
    height=160,
    placeholder="Last night I dreamed of..."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    interpret_button = st.button("🔮 Interpret my dream", type="primary")

if interpret_button:
    if dream_input.strip():

        # Step 1 : interpret the dream via Groq API
        with st.spinner("✨ Interpreting your dream..."):
            dream_interpretation = interpret_dream(dream_input)

        st.markdown(
            f'<div class="interpretation-box">{dream_interpretation}</div>',
            unsafe_allow_html=True,
        )

        # Step 2 : generate an image from the visual scene description
        with st.spinner("🎨 Generating dream vision..."):
            image_prompt = extract_image_prompt(dream_interpretation)
            image_bytes  = generate_image(image_prompt)
            if image_bytes:
                st.image(image_bytes, caption="✦ Your dream vision ✦", use_container_width=True)
            else:
                st.warning("Image could not be generated, please try again.")

        # Step 3 : save the dream and interpretation to the journal
        add_dream_to_journal(dream_input, dream_interpretation)
        st.success("✦ Dream saved to your journal ✦")

    else:
        st.warning("Please describe your dream first.")

st.divider()

# ---------------------------------------------------------------------------
# Journal toggle
# ---------------------------------------------------------------------------

if "show_journal" not in st.session_state:
    st.session_state["show_journal"] = False

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    journal_label = "📖 Hide Dream Journal" if st.session_state["show_journal"] else "📖 Show Dream Journal"
    if st.button(journal_label, type="secondary"):
        st.session_state["show_journal"] = not st.session_state["show_journal"]
        st.rerun()

if st.session_state["show_journal"]:
    st.subheader("📖 Dream Journal")
    display_journal()