import streamlit as st
import login_view
import app_supplier
import farmer_view 
import data_gen 
import backend  # <--- IMPORT THE HELPER

# 1. SETUP PAGE CONFIG (The brain handles this for everyone)
st.set_page_config(
    page_title="SeSeed App", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INITIALIZE SESSION STATE (Using your backend.py)
# This replaces the big block of "if 'key' not in session_state" code
backend.initialize_session_state()

# 3. NAVIGATION LOGIC (The Traffic Controller)
def main():
    # A. SUPPLIER FLOW
    if st.session_state['role'] == 'Supplier':
        if st.session_state['logged_in']:
            # Show Supplier Dashboard
            app_supplier.show_dashboard()
        else:
            # Force Supplier Login
            login_view.login_page()

    # B. FARMER FLOW
    elif st.session_state['role'] == 'Farmer':
        if st.session_state['show_login']:
            # Show Farmer Login (Optional)
            login_view.login_page()
        else:
            # Show Farmer Shop (Default)
            products = data_gen.load_products_from_db()
            farmer_view.farmer_dashboard(products)

    # C. NO ROLE SELECTED (Front Page)
    else:
        login_view.role_selection()

if __name__ == "__main__":
    main()