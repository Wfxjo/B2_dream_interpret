import base64
from pathlib import Path

import streamlit as st
from dream_interpret import (
    interpret_dream,
    extract_image_prompt,
    generate_image,
    transcribe_audio,
    add_dream_to_journal,
    load_journal,
)

from CSSapp_UI import CUSTOM_CSS, STARS_HTML

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------




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
# UI Components
# ---------------------------------------------------------------------------

def render_header() -> None:
    """
    Render the page header : logo, title and caption.
    """
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


def render_text_input() -> str:
    """
    Render the text input area for dream description.
    Returns the text entered by the user.
    """
    return st.text_area(
        "Describe your dream",
        height=160,
        placeholder="Last night I dreamed of..."
    )


def render_audio_input() -> str:
    """
    Render the audio recording input.
    Handles transcription, session state reset, and the record-again button.
    Returns the transcribed text, or an empty string if nothing is ready.
    """
    if "reset_audio" not in st.session_state:
        st.session_state["reset_audio"] = False
    if "transcribed_text" not in st.session_state:
        st.session_state["transcribed_text"] = ""

    if st.session_state["reset_audio"]:
        st.session_state["reset_audio"] = False
        st.session_state["transcribed_text"] = ""
        st.rerun()

    audio_data = st.audio_input("Record your dream")

    if audio_data:
        with st.spinner("🎙️ Transcribing your voice..."):
            transcribed = transcribe_audio(audio_data)
        if transcribed and not transcribed.startswith("Error"):
            st.session_state["transcribed_text"] = transcribed
            st.success("✦ Transcription done ✦")
            st.write(f"*{transcribed}*")
            if st.button("💫 Record again"):
                st.session_state["reset_audio"] = True
                st.rerun()
        else:
            st.error(transcribed)
            st.session_state["transcribed_text"] = ""

    return st.session_state["transcribed_text"]


def render_dream_input() -> str:
    """
    Render the input mode selector (Write or Record).
    Returns the dream text from whichever input mode is selected.
    """
    input_mode = st.radio(
        "How do you want to describe your dream?",
        ["🪶 Write", "🎙️ Record"],
        horizontal=True,
    )

    if input_mode == "🪶 Write":
        return render_text_input()
    else:
        return render_audio_input()


def render_interpretation(dream_interpretation: str) -> None:
    """
    Render the dream interpretation inside a styled box.
    """
    st.markdown(
        f'<div class="interpretation-box">{dream_interpretation}</div>',
        unsafe_allow_html=True,
    )


def render_image(dream_interpretation: str) -> None:
    """
    Extract the visual prompt, generate and display the dream image.
    Shows a warning if generation fails.
    """
    with st.spinner("🎨 Generating dream vision..."):
        image_prompt = extract_image_prompt(dream_interpretation)
        image_bytes  = generate_image(image_prompt)
    if image_bytes:
        st.image(image_bytes, caption="✦ Your dream vision ✦", use_container_width=True)
    else:
        st.warning("Image could not be generated, please try again.")


def render_journal() -> None:
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


def render_journal_toggle() -> None:
    """
    Render the toggle button to show or hide the dream journal.
    """
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
        render_journal()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Main function that orchestrates the full Streamlit app flow.
    """
    st.set_page_config(page_title="Dream Interpreter", page_icon="🌙", layout="centered")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(STARS_HTML, unsafe_allow_html=True)

    render_header()
    st.divider()

    dream_input = render_dream_input()
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        interpret_button = st.button("🔮 Interpret my dream", type="primary")

    if interpret_button:
        if dream_input.strip():

            # Step 1 : interpret the dream via Groq API
            with st.spinner("✨ Interpreting your dream..."):
                dream_interpretation = interpret_dream(dream_input)

            render_interpretation(dream_interpretation)

            # Step 2 : generate an image from the visual scene description
            render_image(dream_interpretation)

            # Step 3 : save the dream and interpretation to the journal
            add_dream_to_journal(dream_input, dream_interpretation)
            st.success("✦ Dream saved to your journal ✦")

        else:
            st.warning("Please describe your dream first.")

    st.divider()
    render_journal_toggle()


if __name__ == "__main__":
    main()