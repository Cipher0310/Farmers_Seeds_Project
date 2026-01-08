import streamlit as st

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
    # New state for Navigation Tabs (defaults to 'all')
    if 'view_category' not in st.session_state:
        st.session_state['view_category'] = 'all'
    # Initialize search input state if not present
    if 'search_input' not in st.session_state:
        st.session_state['search_input'] = ""
    # Initialize Price States for Syncing
    if 'price_min' not in st.session_state:
        st.session_state['price_min'] = 0
    if 'price_max' not in st.session_state:
        st.session_state['price_max'] = 100
    # State to track selected product for Detail View
    if 'selected_product' not in st.session_state:
        st.session_state['selected_product'] = None