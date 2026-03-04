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
        width: 400px;
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