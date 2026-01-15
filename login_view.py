import streamlit as st
import time
import os
import base64

# --- BULLETPROOF IMAGE LOADER ---
def get_base64_of_bin_file(filename):
    """
    Reads a file from the SAME directory as this script and returns base64.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None 

# --- PAGE: ROLE SELECTION ---
def role_selection():
    # 1. LOAD BACKGROUND
    bg_encoded = get_base64_of_bin_file("farm_cover.png")
    
    if bg_encoded:
        bg_style = f"""
            background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url("data:image/png;base64,{bg_encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        """
    else:
        bg_style = "background-color: #555;"

    st.markdown(
        f"""
        <style>
        .stApp {{ {bg_style} }}
        
        /* TITLE STYLING */
        .title-container {{
            text-align: center;
            padding-top: 50px;
            margin-bottom: 30px;
        }}
        .main-title {{
            font-size: 5rem;
            font-weight: 900;
            color: #ffffff;
            text-shadow: 4px 4px 15px rgba(0,0,0,0.8);
            margin: 0;
        }}
        .sub-title {{
            font-size: 2.5rem;
            font-weight: 600;
            color: #f0f0f0;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
            margin-top: -10px;
        }}

        /* --- BUTTON BOX STYLING --- */
        div.stButton > button {{
            width: 100%;
            height: 320px !important;  /* Fixed Square Height */
            background-color: white !important;
            color: black !important;
            border-radius: 25px !important;
            border: 3px solid #e0e0e0 !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}

        /* HOVER EFFECT */
        div.stButton > button:hover {{
            transform: translateY(-8px);
            border-color: #4CAF50 !important;
            color: #4CAF50 !important;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }}
        
        /* --- TEXT & EMOJI SIZING --- */
        
        /* 1. Base Text Settings (For "I am a FARMER") */
        div.stButton > button p {{
            white-space: pre-wrap !important; /* Ensure newlines work */
            font-size: 22px !important;      /* CONSISTENT SMALL SIZE */
            font-weight: 700 !important;
            line-height: 1.5 !important;
            margin: 0px !important;
            padding-top: 20px !important;
        }}

        /* 2. Target ONLY the Emoji (The First Line) */
        div.stButton > button p::first-line {{
            font-size: 90px !important;      /* HUGE EMOJI SIZE */
            line-height: 1.5 !important;
        }}

        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        </style>
        """, unsafe_allow_html=True
    )

    # 2. TITLE SECTION
    st.markdown("""
        <div class="title-container">
            <div class="main-title">🌱 SeSeed</div>
            <div class="sub-title">Select Role</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 3. BUTTONS LAYOUT
    c1, c2, c3, c4, c5 = st.columns([0.5, 2, 0.2, 2, 0.5])
    
    with c2:
        # Putting Emoji on Line 1, Text on Line 2
        if st.button("👨‍🌾\nI am a FARMER", use_container_width=True):
            st.session_state['role'] = 'Farmer'
            st.rerun()
            
    with c4:
        # Putting Emoji on Line 1, Text on Line 2
        if st.button("🏭\nI am a SUPPLIER", use_container_width=True):
            st.session_state['role'] = 'Supplier'
            st.rerun()

# --- PAGE: LOGIN ---
def login_page():
    # 1. LOAD BACKGROUND
    bg_encoded = get_base64_of_bin_file("login_cover.png")
    
    if bg_encoded:
        bg_style = f"""
            background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url("data:image/png;base64,{bg_encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        """
    else:
        bg_style = "background-color: #333;"

    st.markdown(
        f"""
        <style>
        .stApp {{ {bg_style} }}
        
        [data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #d3d3d3;
            padding: 30px; 
            border-radius: 20px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        }}
        
        [data-testid="stForm"] h1, [data-testid="stForm"] p, [data-testid="stForm"] label {{
            color: #000000 !important;
        }}
        
        /* GREEN SIGN IN BUTTON */
        [data-testid="stForm"] button {{
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            padding: 0.5rem 1rem !important;
            border-radius: 8px !important;
        }}
        [data-testid="stForm"] button:hover {{
            background-color: #45a049 !important;
            color: white !important;
        }}
        
        div.stButton > button {{
            width: 100%;
            padding: 10px;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.form("login_form"):
            role_icon = "👨‍🌾" if st.session_state.get('role') == 'Farmer' else "🏭"
            st.title(f"{role_icon} Login")
            
            user = st.text_input("Username", placeholder="Enter username")
            st.caption("Include uppercase and lowercase letter")
            pw = st.text_input("Password", type="password", placeholder="Enter password")
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