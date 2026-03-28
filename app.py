import streamlit as st
import pickle
import numpy as np
import base64
import os
import urllib.parse
import requests
import random
from streamlit_lottie import st_lottie

st.set_page_config(page_title="GenieBook AI", page_icon="📚", layout="wide")

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_book = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_v7igp37u.json")

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_data = get_base64("bg.jpg")
logo_data = get_base64("logo.png")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
* {{ font-family: 'Inter', sans-serif; color: white; }}

/* --- Background Overlay --- */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)), url("data:image/jpg;base64,{bg_data}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}}

/* --- SIDEBAR UPGRADE --- */
[data-testid="stSidebar"] {{
    background-color: rgba(5, 5, 5, 0.8) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 245, 255, 0.2);
}}

/* Sidebar Logo Styling */
.sidebar-logo-container {{
    text-align: center;
    margin-bottom: 10px;
    padding-top: 10px;
}}
.sidebar-logo-img {{
    width: 100px;
    border-radius: 50%;
    border: 2px solid #00f5ff;
    box-shadow: 0 0 15px rgba(0,245,255,0.4);
}}

.sidebar-title {{
    color: #00f5ff;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 20px;
    text-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
}}

/* --- FIXED FLOATING ANIMATION --- */
@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }} /* Restricted movement to stay inside box */
    100% {{ transform: translateY(0px); }}
}}

.book-img-float {{
    width: 90% !important; /* Slightly smaller to prevent cutting edges */
    height: 250px; 
    object-fit: contain; 
    border-radius: 12px; 
    background: #000; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    animation: float 6s ease-in-out infinite;
    transition: all 0.3s ease;
    display: block;
    margin: 0 auto; /* Perfect center alignment */
}}

/* --- Main Cards --- */
.card-container {{ padding: 10px; }}
.card {{
    background: rgba(15, 15, 15, 0.85);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    height: auto; 
    min-height: 610px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.4s ease-in-out;
    overflow: hidden; /* Added to keep animation inside */
}}
.card:hover {{
    transform: translateY(-12px);
    background: rgba(30, 30, 30, 0.98);
    border: 2px solid #FFFFFF;
    box-shadow: 0px 10px 30px rgba(255, 255, 255, 0.2);
}}

/* --- Dual Button Styling --- */
.button-row {{
    display: flex;
    gap: 8px;
    margin-top: 15px;
}}

.link-btn {{
    flex: 1;
    display: block;
    padding: 10px 2px;
    text-decoration: none;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 800;
    transition: 0.3s;
    text-align: center;
}}

.btn-pdf {{
    background: #FFFFFF !important;
    color: #000000 !important;
}}

.btn-buy {{
    background: linear-gradient(45deg, #00f5ff, #0072ff) !important;
    color: #FFFFFF !important;
}}

.link-btn:hover {{
    transform: scale(1.05);
    filter: brightness(1.2);
}}

/* --- Input & Buttons --- */
div[data-baseweb="select"] > div {{
    background-color: #000000 !important;
    border-radius: 12px !important;
    border: 2px solid #00f5ff !important;
    height: 55px !important;
}}

/* GENERATE BUTTON GLOW EFFECT & ARROW */
.stButton>button {{
    background: linear-gradient(45deg, #00f5ff, #0072ff) !important;
    color: white !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    height: 55px !important;
    margin-top: 28px !important;
    width: 100% !important;
    position: relative;
    transition: all 0.3s ease;
}}

.stButton>button:hover {{
    box-shadow: 0 0 20px 5px rgba(255, 255, 255, 0.6) !important;
    transform: scale(1.02);
}}

.stButton>button::after {{
    content: ' →';
    font-size: 20px;
    transition: 0.3s;
}}

.main-title {{
    text-align: center;
    font-size: 70px;
    font-weight: 900;
    background: linear-gradient(90deg, #FFFFFF, #00f5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}}

/* RESPONSIVE DESIGN FOR MOBILE/TABLET */
@media (max-width: 768px) {{
    .main-title {{ font-size: 40px; }}
    [data-testid="column"] {{ width: 100% !important; flex: 1 1 100% !important; }}
    .card {{ min-height: auto; margin-bottom: 20px; }}
    .book-img-float {{ height: 200px; }}
}}

/* NO TEXT CUTTING */
.card p {{
    overflow: visible !important;
    height: auto !important;
    display: block !important;
}}

</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    return popular_df, pt, books, similarity_scores

try:
    popular_df, pt, books, similarity_scores = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}. Please check if all .pkl files are uploaded and scikit-learn is in requirements.txt")
    st.stop()

# DYNAMIC DESCRIPTION LOGIC BASED ON VIBE
def get_pro_desc(title, mood):
    vibe_descriptions = {
        "Mysterious": [
            f"Unveil the cryptic shadows hidden within {title}.",
            f"A dark, enigmatic journey awaits in the pages of {title}.",
            f"Decipher the secrets that {title} has kept buried.",
            f"The Oracle whispers: {title} holds keys to the unknown."
        ],
        "Calm": [
            f"Lose yourself in the gentle, serene flow of {title}.",
            f"A peaceful retreat for your mind, found inside {title}.",
            f"Let the tranquil prose of {title} wash over you.",
            f"Find your quiet corner with the soothing narrative of {title}."
        ],
        "Thrilling": [
            f"Brace yourself for the high-octane energy of {title}.",
            f"An adrenaline-fueled ride that begins with {title}.",
            f"Experience the relentless intensity of {title} now.",
            f"A pulse-pounding masterpiece—{title} never slows down."
        ],
        "Intellectual": [
            f"A deep neural resonance with the logic of {title}.",
            f"Expand your cognitive horizons through {title}.",
            f"A complex masterwork of intellect: {title}.",
            f"Curated synaptic intelligence leads you to {title}."
        ]
    }
    
    desc = random.choice(vibe_descriptions.get(mood, vibe_descriptions["Intellectual"]))
    pdf_query = f"{title} book filetype:pdf"
    pdf_url = f"https://www.google.com/search?q={urllib.parse.quote(pdf_query)}&btnI"
    amazon_query = f"{title} book"
    buy_url = f"https://www.amazon.com/s?k={urllib.parse.quote(amazon_query)}"
    
    return desc, pdf_url, buy_url

# Header with Logo in Center
st.markdown('<div class="main-title">GenieBook AI</div>', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<div style="text-align:center; margin-bottom:20px;"><img src="data:image/png;base64,{logo_data}" width="120" style="border-radius:50%; border: 3px solid #00f5ff; box-shadow: 0 0 20px rgba(0,245,255,0.4);"></div>', unsafe_allow_html=True)

# Lottie placement
l_col1, l_col2, l_col3 = st.columns([1, 1, 1])
with l_col2:
    if lottie_book: st_lottie(lottie_book, height=140)

# SIDEBAR CONTENT
with st.sidebar:
    # --- LOGO ADDED AT THE TOP OF SIDEBAR ---
    if logo_data:
        st.markdown(f"""
        <div class="sidebar-logo-container">
            <img src="data:image/png;base64,{logo_data}" class="sidebar-logo-img">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 10px; margin-bottom: 20px;">
        <h2 style="color: #00f5ff; font-weight: 800; text-shadow: 0 0 15px rgba(0,245,255,0.6); margin-bottom: 5px;">GENIE CORE</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #00f5ff, transparent); width: 100%;"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size: 15px; color: #888; font-weight: 600; letter-spacing: 2px; margin-left: 5px;">📚 MENU</p>', unsafe_allow_html=True)
    menu = st.radio("Menu", ["Recommendations", "Popular Books", "About GenieBook AI"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p style="font-size: 12px; color: #888; font-weight: 600; letter-spacing: 2px; margin-left: 5px;">CURRENT VIBE</p>', unsafe_allow_html=True)
    mood = st.select_slider(
        "Select Mood",
        options=["Mysterious", "Calm", "Thrilling", "Intellectual"],
        label_visibility="collapsed")
    
    mood_messages = {
        "Mysterious": "Adjusting neural filters for dark secrets... 🌑",
        "Calm": "Finding peaceful narratives for you... 🌊",
        "Thrilling": "Hyper-driving engine for adrenaline... ⚡",
        "Intellectual": "Scanning deep philosophical databases... 🧠"
    }
    st.caption(mood_messages[mood])
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; margin-top: 40px; border-top: 1px solid rgba(255, 255, 255, 0.05);">
        <p style="font-size: 11px; font-weight: 800; color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0;">Architect</p>
        <p style="font-size: 22px; font-weight: 900; background: linear-gradient(180deg, #fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">VICKY SHARMA</p>
        <div style="display: inline-block; padding: 2px 10px; border-radius: 20px; background: rgba(0,245,255,0.1); border: 1px solid rgba(0,245,255,0.2); margin-top: 10px;">
            <span style="font-size: 10px; color: #00f5ff; font-weight: bold;">NEURAL CORE V2.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# AI RECOMMENDATIONS
if menu == "Recommendations":
    st.markdown("### Discover Your Next Favorite Book")
    c_s, c_b = st.columns([3, 1])
    with c_s:
        user_input = st.selectbox("🔍 SEARCH FOR A BOOK YOU LOVE:", pt.index.values)
    with c_b:
        generate_btn = st.button("GENERATE", use_container_width=True)
    if generate_btn:
        index = list(pt.index).index(user_input)
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        cols = st.columns(5)
        for i, item in enumerate(similar_items):
            temp_df = books[books['Book-Title'] == pt.index[item[0]]].drop_duplicates('Book-Title')
            if not temp_df.empty:
                title = temp_df['Book-Title'].values[0]
                author = temp_df['Book-Author'].values[0]
                img = temp_df['Image-URL-M'].values[0]
                desc, pdf_url, buy_url = get_pro_desc(title, mood)
                with cols[i]:
                    st.markdown(f"""
                    <div class="card-container">
                        <div class="card">
                            <img src="{img}" class="book-img-float">
                            <p style="font-weight:800; font-size:15px; margin-top:12px; line-height:1.2;">{title[:30]}</p>
                            <p style="color:#00f5ff; font-size:12px; font-weight:500;">{author}</p>
                            <p style="color:#bbb; font-size:11px; line-height:1.4; font-style:italic;">"{desc}"</p>
                            <div class="button-row">
                                <a href="{pdf_url}" target="_blank" class="link-btn btn-pdf">READ MORE</a>
                                <a href="{buy_url}" target="_blank" class="link-btn btn-buy">BUY NOW</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# POPULAR BOOKS
elif menu == "Popular Books":
    st.markdown(f"### Popular Books - Current Vibe: {mood}")
    cols = st.columns(5)
    for i in range(min(10, len(popular_df))):
        title = popular_df['Book-Title'].iloc[i]
        author = popular_df['Book-Author'].iloc[i]
        img = popular_df['Image-URL-M'].iloc[i]
        rating = round(popular_df['avg_rating'].iloc[i], 2)
        desc, pdf_url, buy_url = get_pro_desc(title, mood)
        with cols[i % 5]:
            st.markdown(f"""
            <div class="card-container">
                <div class="card">
                    <img src="{img}" class="book-img-float">
                    <div>
                        <p style="font-weight:800; font-size:15px; margin-top:12px; color:#fff; line-height:1.2;">{title[:30]}</p>
                        <p style="color:#00f5ff; font-size:12px; font-weight:500;">{author}</p>
                        <p style="color:#FFD700; font-size:13px; font-weight:bold;">★ {rating}</p>
                    </div>
                    <p style="color:#bbb; font-size:11px; line-height:1.4; font-style:italic;">"{desc}"</p>
                    <div class="button-row">
                        <a href="{pdf_url}" target="_blank" class="link-btn btn-pdf">READ MORE</a>
                        <a href="{buy_url}" target="_blank" class="link-btn btn-buy">BUY NOW</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ABOUT SECTION
elif menu == "About GenieBook AI":
    st.markdown("""
    <div class="about-box" style="background: rgba(0,0,0,0.8); padding: 40px; border-radius: 30px; border: 1px solid #00f5ff;">
        <h1 style='color:#00f5ff; text-align:center; font-size:45px; font-weight:800;'>THE FUTURE OF DISCOVERY</h1>
        <p style='text-align:center; color:#ccc; font-size:18px;'>BookGenie AI isn't just a search tool—it's a neural bridge to your next favorite story.</p>
        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:25px; margin-top:40px;'>
            <div style='background:rgba(255,255,255,0.03); padding:25px; border-radius:20px; border-left: 5px solid #00f5ff;'>
                <h3 style='margin:0; color:#fff;'>🚀 Neural Discovery</h3>
                <p style='color:#ccc; font-size:14px; margin-top:10px;'>Advanced Vector Similarity maps your unique taste.</p>
            </div>
            <div style='background:rgba(255,255,255,0.03); padding:25px; border-radius:20px; border-left: 5px solid #00f5ff;'>
                <h3 style='margin:0; color:#fff;'>📊 Massive Intelligence</h3>
                <p style='color:#ccc; font-size:14px; margin-top:10px;'>Millions of data points distilled into clean recommendations.</p>
            </div>
        </div>
        <div style="text-align:center; margin-top:50px;">
             <p style="color:#00f5ff; font-weight:800; font-size:24px;">Vicky Sharma</p>
             <p style="color:#888;">Lead Architect & Visionary</p>
        </div>
    </div>
    """, unsafe_allow_html=True)