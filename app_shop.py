import streamlit as st
import os
import data_gen
import backend
from login_view import role_selection, login_page, supplier_dashboard
from farmer_view import farmer_dashboard

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Seseed - Smart Farming")

# --- 2. INITIALIZATION ---
# Initialize DB if missing
if not os.path.exists(data_gen.DB_PATH):
    data_gen.generate_data()

# Initialize Session State
backend.initialize_session_state()

# Load Products (Must be done every rerun to get fresh data/state)
products = data_gen.load_products_from_db()

# --- 3. MAIN APPLICATION LOGIC ---
if __name__ == "__main__":
    # Add a warning in the terminal if the DB exists, reminding the user to delete it if they changed images.
    if os.path.exists(data_gen.DB_PATH):
        print("\n[WARNING] 'database.db' exists. The app is loading existing data.")
        print("If you added new local images (like pamelo.png or hoe.png), DELETE 'database.db' and restart the app to regenerate data.\n")

    if st.session_state['show_login']:
        login_page()
    elif st.session_state['role'] is None:
        role_selection()
    else:
        if st.session_state['role'] == 'Farmer':
            # Pass products data to the view
            farmer_dashboard(products)
        elif st.session_state['role'] == 'Supplier':
            if not st.session_state['logged_in']:
                 st.session_state['show_login'] = True
                 st.rerun()
            else:
                supplier_dashboard()