import streamlit as st
import time
import os
import sqlite3
from utils import get_base64_of_bin_file
from data_gen import DB_PATH

# --- PAGE: ROLE SELECTION ---
def role_selection():
    # FIXED: Removed .png from the filename
    bg_encoded = get_base64_of_bin_file("farm_cover.png") 
    if bg_encoded:
        bg_style = f'background-image: linear-gradient(rgba(255,255,255,0.2), rgba(255,255,255,0.2)), url("{bg_encoded}");'
    else:
        bg_style = 'background-color: #2E8B57;'

    st.markdown(
        f"""
        <style>
        .stApp {{ {bg_style} background-size: cover; }}
        .title-text {{ text-align: center; color: white; font-size: 5em; font-weight: bold; padding-top: 10vh; text-shadow: 2px 2px 8px #000; }}
        .subtitle-text {{ text-align: center; color: white; font-size: 2em; font-weight: bold; margin-bottom: 30px; text-shadow: 1px 1px 4px #000; }}
        
        div.stButton > button {{
            width: 100%;
            padding: 10px;
            font-weight: bold;
            font-size: 20px;
            color: #333333;
            background-color: white;
            border: 2px solid #4CAF50;
        }}
        div.stButton > button:hover {{
            background-color: #4CAF50 !important;
            color: white !important;
            border-color: #3e8e41 !important;
        }}
        div.stButton > button:hover p {{
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="title-text">🌱 Seseed</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Select Role</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("👨‍🌾 I am a FARMER", use_container_width=True):
            st.session_state['role'] = 'Farmer'
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🏭 I am a SUPPLIER", use_container_width=True):
            st.session_state['role'] = 'Supplier'
            st.rerun()

# --- PAGE: LOGIN ---
def login_page():
    # FIXED: Removed .png from the filename
    bg_encoded = get_base64_of_bin_file("login_cover.png")
    app_bg = f'url("{bg_encoded}")' if bg_encoded else 'none'
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), {app_bg};
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #d3d3d3;
            padding: 20px; 
            border-radius: 20px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        }}
        [data-testid="stForm"] h1, [data-testid="stForm"] label, [data-testid="stForm"] p, [data-testid="stForm"] small {{
            color: #000000 !important;
            text-shadow: none !important;
        }}
        [data-testid="stForm"] div[data-baseweb="input"] {{
            border: 1px solid #000000 !important;
            background-color: #ffffff !important;
            border-radius: 5px !important;
        }}
        div[data-testid="column"]:nth-of-type(2) button {{
            background-color: #f44336 !important;
            color: white !important;
            border: none !important;
            font-weight: bold;
        }}
        div[data-testid="column"]:nth-of-type(2) button:hover {{
            background-color: #d32f2f !important;
            color: white !important;
        }}
        div[data-testid="column"]:nth-of-type(2) button:hover p {{
            color: white !important;
        }}
        [data-testid="stForm"] button {{
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
        }}
        [data-testid="stForm"] button:hover {{
            background-color: #45a049 !important;
            color: white !important;
        }}
        header {{visibility: hidden;}}
        .block-container {{padding-top: 2rem;}}
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            role_icon = "👨‍🌾" if st.session_state.get('role') == 'Farmer' else "🏭"
            st.title(f"{role_icon} Login")
            
            st.markdown("Enter your credentials")
            user = st.text_input("Username")
            st.caption("Include uppercase and lowercase letter")
            pw = st.text_input("Password", type="password")
            st.caption("Minimum 8 characters")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign In", use_container_width=True)

            if submitted:
                has_upper = any(c.isupper() for c in user)
                has_lower = any(c.islower() for c in user)
                if not user or not pw:
                      st.error("Enter any username/password.")
                elif not (has_upper and has_lower):
                    st.error("Username must contain at least one Uppercase and one Lowercase letter.")
                elif len(pw) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    st.success(f"Welcome, {user}!")
                    time.sleep(0.5)
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user
                    st.session_state['show_login'] = False 
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back", use_container_width=True):
            st.session_state['show_login'] = False
            if not st.session_state.get('logged_in'):
                st.session_state['role'] = None
            st.rerun()

def supplier_dashboard():
    pass