import sqlite3
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

# --- 3. AI ANSWER FUNCTION (UPDATED) ---
def ask_ai(user_question):
    if not model:
        return "I am currently offline (API Key missing)."
    
    # 1. FETCH PRODUCT DATA DYNAMICALLY
    product_context = ""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, category, stock FROM products")
        products = cursor.fetchall()
        conn.close()
        
        # Format the data into a readable string for the AI
        if products:
            product_list = "\n".join([f"- {p[0]}: RM {p[1]:.2f} ({p[2]}) - {p[3]} in stock" for p in products])
            product_context = f"CURRENT INVENTORY & PRICES:\n{product_list}\n"
        else:
            product_context = "Inventory is currently empty."
            
    except Exception as e:
        product_context = "Error retrieving inventory data."

    try:
        # 2. UPDATE PROMPT WITH DATA
        prompt = f"""
        You are Seseedy, a helpful AI assistant for the 'SeSeed' farming website.
        
        {product_context}
        
        Website Rules:
        - We sell vegetable, fruit, and leafy green seeds.
        - We do NOT sell heavy machinery (tractors), only small tools.
        - Users can filter by category or price.
        
        User Question: {user_question}
        
        Instructions:
        - If the user asks for a price, LOOK at the 'CURRENT INVENTORY' list above and answer with the exact price in RM.
        - If the product is not in the list, say we don't carry it.
        - Keep your answer helpful, short, and friendly.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble thinking right now. (Error: {str(e)})"
    
# ==========================================
# --- ADD THESE IMPORTS AT THE TOP ---
# ==========================================
import google.generativeai as genai
import os
# ... existing imports ...
# NEW IMPORTS FOR VOICE:
import speech_recognition as sr
from gtts import gTTS
import io
import tempfile

# ... (Your existing configure_gemini and ask_ai functions remain here) ...


# ==========================================
# --- ADD THESE NEW FUNCTIONS AT THE END ---
# ==========================================

def transcribe_audio(audio_bytes):
    """
    Takes raw audio bytes from the browser recorder, saves them temporarily,
    and uses Google Speech Recognition to transcribe them to text.
    """
    r = sr.Recognizer()
    text = None

    try:
        # 1. Save the raw bytes to a temporary WAV file
        # Browser audio often comes in webm format, but saving as .wav often works 
        # for speech_recognition to read the headers correctly.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
            tmp_audio_file.write(audio_bytes)
            tmp_audio_path = tmp_audio_file.name

        # 2. Read the temporary file into the recognizer
        with sr.AudioFile(tmp_audio_path) as source:
            # Adjust for ambient noise if necessary, though often fine without for quick commands
            # r.adjust_for_ambient_noise(source) 
            audio_data = r.record(source)

        # 3. Perform Google Speech Recognition (requires internet)
        text = r.recognize_google(audio_data)
        print(f"✅ Transcription successful: {text}")

    except sr.UnknownValueError:
        print("Generation Error: Could not understand audio")
    except sr.RequestError as e:
        print(f"Generation Error: Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
    finally:
        # 4. Clean up temp file
        if 'tmp_audio_path' in locals() and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)
            
    return text

def text_to_speech_bytes(text, lang='en'):
    """
    Converts text to speech using gTTS and returns the audio data as bytes
    (in-memory, without saving to disk).
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Create an in-memory byte buffer
        mp3_fp = io.BytesIO()
        # Write the audio data to the buffer
        tts.write_to_fp(mp3_fp)
        # Get the bytes values
        audio_bytes = mp3_fp.getvalue()
        return audio_bytes
    except Exception as e:
        print(f"TTS Error: {e}")
        return None