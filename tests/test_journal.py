import os
import sys

# Add the parent directory to the path so that dream_interpret can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dream_interpret import (
    load_journal,
    save_journal,
    add_dream_to_journal,
    extract_image_prompt,
)


# ---------------------------------------------------------------------------
# Tests : load_journal / save_journal
# ---------------------------------------------------------------------------

def test_load_journal_creates_file():
    """
    Verify that load_journal returns an empty list
    when the journal file does not exist.
    """
    if os.path.exists("dream_journal.json"):
        os.remove("dream_journal.json")
    result = load_journal()
    assert result == []


def test_save_and_load_journal():
    """
    Verify that a journal saved with save_journal
    is correctly retrieved by load_journal.
    """
    save_journal([{"dream": "I was flying"}])
    result = load_journal()
    assert result == [{"dream": "I was flying"}]


# ---------------------------------------------------------------------------
# Tests : add_dream_to_journal
# ---------------------------------------------------------------------------

def test_add_dream_to_journal():
    """
    Verify that add_dream_to_journal correctly appends
    a new entry with the dream text and its interpretation.
    """
    save_journal([])
    add_dream_to_journal("I was flying", "Symbol of freedom")
    journal = load_journal()
    assert journal[-1]["dream"] == "I was flying"
    assert journal[-1]["interpretation"] == "Symbol of freedom"


# ---------------------------------------------------------------------------
# Tests : extract_image_prompt
# ---------------------------------------------------------------------------

def test_extract_image_prompt_found():
    """
    Verify that extract_image_prompt correctly extracts
    the visual scene when the keyword is found in the text.
    """
    text = "blabla\n🎨 Visual Scene : A red sky\nend"
    result = extract_image_prompt(text)
    assert "A red sky" in result


def test_extract_image_prompt_not_found():
    """
    Verify that extract_image_prompt falls back to the first 400 characters
    and appends quality keywords when no visual scene is found.
    """
    result = extract_image_prompt("text without visual scene")
    assert "digital art" in result