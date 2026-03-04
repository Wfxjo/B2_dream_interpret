# 🌙 Dream Interpreter

> *"Learn how to see. Realize that everything connects to everything else."* — Leonardo Da Vinci

An AI-powered application that interprets your dreams, generates a visual illustration, and stores everything in a personal dream journal.

---

## ✨ Features

- **🪶 Text input** — describe your dream by typing
- **🎙️ Voice input** — record your dream and get it transcribed automatically
- **🔮 AI interpretation** — symbolic and poetic analysis powered by LLaMA via Groq
- **🎨 Image generation** — a unique visual illustration generated from your dream
- **📖 Dream journal** — all your dreams are saved with their interpretation and image

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| [Streamlit](https://streamlit.io) | Web interface |
| [Groq](https://groq.com) + LLaMA 3.3 70B | Dream interpretation |
| [Groq](https://groq.com) + Whisper Large v3 | Speech-to-text transcription |
| [Hugging Face](https://huggingface.co) + Stable Diffusion XL | Image generation |
| Python | Core language |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Wfxjo/B2_dream_interpret.git
cd B2_dream_interpret
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

Create a `.env` file at the root of the project:

```
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🗂️ Project Structure

```
B2_dream_interpret/
├── app.py               # Streamlit UI — all render functions
├── dream_interpret.py   # Business logic — API calls, journal management
├── prompts.py           # LLM system prompt
├── CSSapp_UI.py         # CSS styles and HTML stars animation
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed)
├── dream_journal.json   # Dream journal (not committed)
└── tests/
    ├── test_journal.py  # Unit tests
    └── rapport_tests.html  # Test report
```

---

## 🧪 Running Tests

```bash
pytest tests/test_journal.py -v
```

Generate an HTML report :

```bash
pytest tests/test_journal.py -v --html=tests/rapport_tests.html
```

---

## 🔑 API Keys

| API | Where to get it | Free tier |
|-----|----------------|-----------|
| Groq | [console.groq.com](https://console.groq.com) | ✅ Yes |
| Hugging Face | [huggingface.co](https://huggingface.co) → Settings → Access Tokens | ✅ Yes |
