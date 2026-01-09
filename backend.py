import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETUP GEMINI AI ---
def configure_ai():
    try:
        # Try to get key from Streamlit Secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # FIX: "Gemini 3" was too expensive (Quota limit 0). 
        # Switching to "Nano" which is usually the free/fast option in your list.
        return genai.GenerativeModel('gemini-2.5-flash')
        
    except Exception as e:
        st.error(f"⚠️ AI Setup Error: {e}")
        return None

model = configure_ai()

# --- 2. SESSION STATE SETUP ---
def initialize_session_state():
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ""
    if 'cart' not in st.session_state:
        st.session_state['cart'] = []
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False
    if 'show_cart_modal' not in st.session_state:
        st.session_state['show_cart_modal'] = False
    if 'view_category' not in st.session_state:
        st.session_state['view_category'] = 'all'
    if 'search_input' not in st.session_state:
        st.session_state['search_input'] = ""
    if 'price_min' not in st.session_state:
        st.session_state['price_min'] = 0
    if 'price_max' not in st.session_state:
        st.session_state['price_max'] = 100
    if 'selected_product' not in st.session_state:
        st.session_state['selected_product'] = None
        
    # --- NEW: Chat History State ---
    if 'messages' not in st.session_state:
        # Initial greeting
        st.session_state['messages'] = [
            {"role": "assistant", "content": "Hello! I am Seseedy. Ask me about seeds, planting guides, or how to use this website!"}
        ]

# --- 3. AI ANSWER FUNCTION ---
def ask_ai(user_question):
    if not model:
        return "I am currently offline (API Key missing)."
    
    try:
        # Context for the AI so it knows who it is
        prompt = f"""
        You are Seseedy, a helpful AI assistant for the 'SeSeed' farming website.
        
        Website details:
        - We sell vegetable, fruit, and leafy green seeds.
        - We do NOT sell heavy machinery (tractors), only small tools (hoes, sprayers).
        - Users can filter by category or price.
        
        User Question: {user_question}
        
        Keep your answer helpful, short, and friendly.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble thinking right now. (Error: {str(e)})"