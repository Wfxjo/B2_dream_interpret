import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from groq import Groq
from prompts import SYSTEM_PROMPT


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

API_KEY       = os.getenv("GROQ_API_KEY")
HF_API_KEY    = os.getenv("HUGGINGFACE_API_KEY")

JOURNAL_FILE  = "dream_journal.json"
MODEL         = "llama-3.3-70b-versatile"
WHISPER_MODEL = "whisper-large-v3"
HF_MODEL_URL  = (
    "https://router.huggingface.co/hf-inference/models/"
    "stabilityai/stable-diffusion-xl-base-1.0"
)



client = Groq(api_key=API_KEY)


# ---------------------------------------------------------------------------
# Journal management
# ---------------------------------------------------------------------------

def load_journal() -> list:
    """
    Load the dream journal from the JSON file.
    If the file does not exist, create it with an empty list.
    Returns a list of dream entries.
    """
    if not os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "w", encoding="utf-8") as journal_file:
            json.dump([], journal_file)
    with open(JOURNAL_FILE, "r", encoding="utf-8") as journal_file:
        return json.load(journal_file)


def save_journal(journal: list) -> None:
    """
    Save the full journal list to the JSON file.
    Overwrites the existing file content each time.
    """
    with open(JOURNAL_FILE, "w", encoding="utf-8") as journal_file:
        json.dump(journal, journal_file, indent=2)


def add_dream_to_journal(dream_text: str, interpretation: str) -> None:
    """
    Create a new journal entry with the current date, the dream text,
    and its interpretation, then append it to the journal and save it.
    """
    journal = load_journal()
    journal.append({
        "date":           datetime.now().strftime("%Y-%m-%d %H:%M"),
        "dream":          dream_text,
        "interpretation": interpretation,
    })
    save_journal(journal)


# ---------------------------------------------------------------------------
# Speech to text
# ---------------------------------------------------------------------------

def transcribe_audio(audio_file) -> str:
    """
    Transcribe an audio file to text using Groq's Whisper model.
    Accepts any file-like object (e.g. from st.audio_input or st.file_uploader).
    Returns the transcribed text as a string.
    If transcription fails, returns the error message instead of crashing.
    """
    try:
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", audio_file.read()),
            model=WHISPER_MODEL,
            response_format="text",
        )
        return transcription
    except Exception as error:
        return f"Error during transcription: {error}"


# ---------------------------------------------------------------------------
# Dream interpretation
# ---------------------------------------------------------------------------

def interpret_dream(dream_text: str) -> str:
    """
    Send the dream description to the Groq API (LLaMA model).
    The system prompt defines the AI behavior and output format.
    Returns the interpretation as a string.
    If the API call fails, returns the error message instead of crashing.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": dream_text},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as error:
        return f"Error during interpretation: {error}"


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def extract_image_prompt(interpretation: str) -> str:
    """
    Extract the visual scene description from the full interpretation text.
    Looks for the line containing 'visual scene' and returns the text from that point.
    Appends quality keywords to improve image generation output.
    If no visual scene is found, returns the first 400 characters of the interpretation.
    """
    quality_keywords = (
        ", digital art, highly detailed, intricate details, sharp focus, "
        "cinematic lighting, dramatic atmosphere, vivid colors, "
        "masterpiece, best quality, 8k, artstation, concept art, "
        "trending on artstation, illustration, fantasy art style"
    )
    lines = interpretation.split("\n")
    for i, line in enumerate(lines):
        if "visual scene" in line.lower():
            return " ".join(lines[i:])[:400] + quality_keywords
    return interpretation[:400] + quality_keywords


def generate_image(prompt: str) -> bytes | None:
    """
    Send the image prompt to Hugging Face's Stable Diffusion model.
    Returns the image as raw bytes if successful, None otherwise.
    The image bytes can be passed directly to st.image() in Streamlit.
    """
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as error:
        print(f"Image generation error: {error}")
        return None