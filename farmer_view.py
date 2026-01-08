import streamlit as st
import time
import os
import streamlit.components.v1 as components 
from utils import get_base64_of_bin_file

# --- CONFIRMATION DIALOG FUNCTION ---
if hasattr(st, 'dialog'):
    decorator = st.dialog
else:
    # Fallback for slightly older Streamlit versions
    decorator = st.experimental_dialog

@decorator("⚠️ Are You Sure Delete All?")
def confirm_delete_dialog():
    st.write("This will remove all items from your cart. This action cannot be undone.")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Yes, Delete", use_container_width=True, key="confirm_delete_btn"):
            st.session_state['cart'] = []
            st.rerun()
            
    with col2:
        if st.button("No, Cancel", use_container_width=True, key="cancel_delete_btn"):
            st.rerun()

# --- FARMER DASHBOARD ---
def farmer_dashboard(products):
    
    # =========================================================
    # 1. FLOATING CUSTOMER SERVICE BUTTON
    # =========================================================
    
    if "chat_trigger" in st.query_params:
        st.session_state['show_chatbot'] = True
        st.query_params.clear() 
        st.rerun()

    chat_icon_b64 = get_base64_of_bin_file("Screenshot 2025-12-28 232049.png")
    
    if chat_icon_b64:
        st.markdown(f"""
            <style>
            .floating-chat-container {{
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 999999;
                transition: transform 0.3s ease;
            }}
            .floating-chat-container:hover {{
                transform: scale(1.1);
            }}
            .floating-chat-container img {{
                width: 70px;
                height: auto;
                cursor: pointer;
                filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
            }}
            </style>
            
            <a href="?chat_trigger=true" target="_self" class="floating-chat-container">
                <img src="{chat_icon_b64}" alt="Customer Service">
            </a>
        """, unsafe_allow_html=True)

    # =========================================================
    # 2. STYLING & BACKGROUND
    # =========================================================

    bg_encoded = get_base64_of_bin_file("background.png")
    if bg_encoded:
        bg_style = f'background-image: url("{bg_encoded}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;'
    else:
        bg_style = "background-image: none;"

    st.markdown(f"""
        <style>
        .stApp {{ {bg_style} }}
        
        /* General Button Style */
        div[data-testid="stVerticalBlock"] div.stButton > button {{
            background-color: #3e5c43 !important;
            color: white !important;
            border-radius: 5px;
            border: none;
            width: 100%;
        }}
        div[data-testid="stVerticalBlock"] div.stButton > button:hover {{
            background-color: #2e4632 !important;
            color: white !important;
        }}

        /* Customer Service/Chat button (Black) */
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlock"] > div.stButton:last-of-type > button {{
            background-color: #000000 !important;
            border-color: #000000 !important;
            color: #ffffff !important;
        }}
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlock"] > div.stButton:last-of-type > button:hover {{
            background-color: #333333 !important;
            color: white !important;
        }}
        
        /* SEARCH BUTTON STYLING */
        div[data-testid="column"]:nth-of-type(3) div[data-testid="stVerticalBlock"] button {{
            background-color: white !important;
            border: 1px solid #cccccc !important;
            color: inherit !important;
        }}
        div[data-testid="column"]:nth-of-type(3) div[data-testid="stVerticalBlock"] button:hover {{
            background-color: #f0f0f0 !important;
        }}
        
        /* Cart Page Styles */
        .cart-total {{
            font-size: 1.5em;
            font-weight: bold;
            text-align: right;
            margin-top: 20px;
            border-top: 2px solid #333;
            padding-top: 10px;
        }}
        
        /* CENTER TOAST NOTIFICATION */
        div[data-testid="stToast"] {{
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: auto !important;
            min-width: 300px;
            z-index: 999999 !important;
            text-align: center;
            background-color: white; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # 3. CHATBOT VIEW SWITCH
    # =========================================================
    
    if 'show_chatbot' not in st.session_state:
        st.session_state['show_chatbot'] = False

    if st.session_state['show_chatbot']:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("← Back to Dashboard"):
            st.session_state['show_chatbot'] = False
            st.rerun()

        chatbot_file_path = "chatbot.html"
        if os.path.exists(chatbot_file_path):
            try:
                with open(chatbot_file_path, "r", encoding="utf-8") as f:
                    chatbot_code = f.read()
                components.html(chatbot_code, height=700, scrolling=True)
            except Exception as e:
                st.error(f"Error loading chatbot: {e}")
        else:
            st.warning("⚠️ 'chatbot.html' file not found.")
            
        return 

    # =========================================================
    # 4. DASHBOARD LOGIC
    # =========================================================

    # --- CALLBACKS ---
    def update_view(category):
        st.session_state['view_category'] = category
        st.session_state['search_input'] = ""
        st.session_state['selected_product'] = None 
        st.session_state['show_cart_modal'] = False 

    def update_price_from_text():
        try:
            p_max_input = float(st.session_state['max_text']) if st.session_state['max_text'] else 100.0
            if p_max_input < 0:
                st.toast("⛔ Warning: Price cannot be negative!")
                st.session_state['max_text'] = str(int(st.session_state['price_max']))
                return
            if p_max_input > 100: 
                p_max_input = 100.0
            st.session_state['price_max'] = p_max_input
            if st.session_state['price_min'] > st.session_state['price_max']:
                st.session_state['price_max'] = st.session_state['price_min']
        except ValueError:
            st.toast("⛔ Please enter a valid number.")
            st.session_state['max_text'] = str(int(st.session_state['price_max']))

    # --- HEADER ---
    back_col, head1, head2, head3 = st.columns([0.5, 2.2, 3, 2], gap="small")
    
    with back_col:
        if st.button("🏠", key="back_home_role", help="Return to Role Selection"):
            st.session_state['role'] = None
            st.session_state['logged_in'] = False
            st.rerun()

    with head1:
        st.markdown("### <div style='white-space: nowrap;'>🌱 *SeSeed* &nbsp; <span style='color:#3e5c43; font-size:1.2rem'>Farmer's Seeds</span></div>", unsafe_allow_html=True)
    
    with head2:
        search_col1, search_col2 = st.columns([5, 1])
        with search_col1:
            search_query = st.text_input("Search", placeholder="Search for seeds...", label_visibility="collapsed", key="search_input")
        with search_col2:
            st.button("🔍", help="Search")
            
    with head3:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            if st.session_state['logged_in']:
                st.write(f"👤 *{st.session_state['username']}*")
                if st.button("Logout", key="logout_btn"):
                    st.session_state['logged_in'] = False
                    st.session_state['username'] = ""
                    st.rerun()
            else:
                if st.button("Register / Login", key="login_btn"):
                    st.session_state['show_login'] = True
                    st.rerun()
        with c2:
            if st.button(f"🛒 Cart ({len(st.session_state['cart'])})", key="top_cart"):
                st.session_state['show_cart_modal'] = not st.session_state['show_cart_modal']
                st.session_state['selected_product'] = None
                st.rerun()

    # --- MAIN CONTENT SWITCH ---
    
    # A. VIEW: CART PAGE
    if st.session_state.get('show_cart_modal'):
        st.markdown("<br>", unsafe_allow_html=True)
        
        c_back, c_title = st.columns([1, 5])
        with c_back:
            if st.button("← Back", key="back_from_cart"):
                st.session_state['show_cart_modal'] = False
                st.rerun()
        with c_title:
            st.markdown("## 🛒 My Cart")

        st.markdown("---")

        if not st.session_state['cart']:
            st.info("Your cart is currently empty. Go add some seeds!")
        else:
            cart_items = {}
            for item in st.session_state['cart']:
                key = item['id']
                if key in cart_items:
                    cart_items[key]['quantity'] += item.get('quantity_ordered', 1)
                    cart_items[key]['total_price'] += item.get('price_ordered', item['price'])
                else:
                    cart_items[key] = {
                        **item, 
                        'quantity': item.get('quantity_ordered', 1),
                        'total_price': item.get('price_ordered', item['price'])
                    }
            
            total_cart_price = 0
            for item_id, item in cart_items.items():
                with st.container():
                    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
                    with c1:
                        st.image(item['image'], width=80)
                    with c2:
                        st.subheader(item['name'])
                        st.write(f"Price: RM {item['price']:.2f} / unit")
                    with c3:
                        st.write(f"*Qty: {item['quantity']}*")
                        st.write(f"*RM {item['total_price']:.2f}*")
                    with c4:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("🗑️ Remove", key=f"remove_{item_id}"):
                            st.session_state['cart'] = [x for x in st.session_state['cart'] if x['id'] != item_id]
                            st.rerun()
                    st.markdown("---")
                total_cart_price += item['total_price']
            
            st.markdown(f"<div class='cart-total'>Total Amount: RM {total_cart_price:.2f}</div>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            b_space, b1, b_gap, b2, b_space2 = st.columns([1, 2, 0.6, 2, 1])
            with b1:
                if st.button("Delete All Items", use_container_width=True):
                    confirm_delete_dialog()
            with b2:
                if st.button("Proceed to Checkout", use_container_width=True):
                    st.session_state['page'] = 'checkout'
                    st.session_state['show_cart_modal'] = False
                    st.rerun()

    # B. VIEW: PRODUCT DETAILS (NO REVIEWS, NO EQUIPMENT)
    elif st.session_state['selected_product']:
        prod = st.session_state['selected_product']
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("X Close", key="close_details_btn"):
            st.session_state['selected_product'] = None
            st.rerun()
            
        st.markdown(f"## {prod['name']}")
        
        # Single column layout for clarity since reviews are gone
        # Using a container to center visually
        with st.container():
            img_packet = prod.get('image', '')
            img_seed = prod.get('image_seed', img_packet)
            img_tree = prod.get('image_tree', img_packet) 
            
            img_c1, img_c2, img_c3 = st.columns(3)
            
            def render_detail_image(label, img_src):
                st.caption(label)
                st.markdown(f"""
                    <div style="height: 250px; display: flex; justify-content: center; align-items: center; background-color: #f8f9fa; border-radius: 8px; margin-bottom: 10px;">
                        <img src="{img_src}" style="max-height: 100%; max-width: 100%; object-fit: contain;">
                    </div>
                """, unsafe_allow_html=True)

            with img_c1:
                render_detail_image("Packet", img_packet)
            with img_c2:
                render_detail_image("Seed", img_seed)
            with img_c3:
                render_detail_image("Mature Tree", img_tree)
        
        st.markdown("---")
        st.caption("Description")
        st.write(prod.get('description', "High quality seeds sourced directly from organic farms. High germination rate and suitable for local climate."))
        st.markdown("---")
        
        st.subheader("Order Quantity")
        box_qty = 0
        
        # Standard Seed Ordering Logic
        q_c1, q_c2 = st.columns([2, 1])
        with q_c1:
            st.write(f"*Packet* (RM {prod['price']:.2f})")
        with q_c2:
            packet_qty = st.number_input(f"Packet Qty", min_value=0, value=0, step=1, label_visibility="collapsed", key="pkt_qty")
        
        q_c3, q_c4 = st.columns([2, 1])
        with q_c3:
            box_price = prod['price'] * 30
            st.write(f"*Box (30 packets)* (RM {box_price:.2f})")
        with q_c4:
            box_qty = st.number_input("Box Qty", min_value=0, value=0, step=1, label_visibility="collapsed", key="box_qty")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- MODIFIED: CENTER AND RESIZE BUTTON ---
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1]) # [1,2,1] Creates a centered button with 50% width
        with b_col2:
            if st.button("Add to Cart", use_container_width=True, key="place_order_final"):
                if packet_qty == 0 and box_qty == 0:
                    st.error("Please select at least 1 unit.")
                else:
                    total_units = packet_qty + (box_qty * 30)
                    total_cost = (packet_qty * prod['price']) + (box_qty * (prod['price'] * 30))
                    
                    order_item = {
                        **prod,
                        "quantity_ordered": total_units,
                        "price_ordered": total_cost,
                        "name": f"{prod['name']} (x{total_units})"
                    }
                    
                    st.session_state['cart'].append(order_item)
                    st.toast(f"Added {total_units} units of {prod['name']} to cart!")
                    st.session_state['selected_product'] = None
                    time.sleep(1)
                    st.rerun()

    # C. VIEW: NORMAL GRID VIEW (NO EQUIPMENT)
    else:
        st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
        
        # Simplified Navigation (Removed Equipment)
        nav_col1, nav_col2, nav_spacer = st.columns([1, 1.2, 4])
        
        with nav_col1:
            st.button("Home", use_container_width=True, on_click=update_view, args=('all',))
        with nav_col2:
            st.button("Browse Seeds", use_container_width=True, on_click=update_view, args=('seeds',))
                
        st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

        c_filt, c_prod = st.columns([1, 4], gap="large")

        with c_filt:
            st.markdown("##### Categories")
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.button("🍆 Fruiting Veg", use_container_width=True, on_click=update_view, args=('Fruiting Veg',))
            st.button("🍉 Fruit", use_container_width=True, on_click=update_view, args=('Fruit',))
            st.button("🥬 Leafy Greens", use_container_width=True, on_click=update_view, args=('Leafy Greens',))
            st.button("🥕 Vegetable", use_container_width=True, on_click=update_view, args=('Vegetable',))
            # REMOVED: Farming Equipment button

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("##### Price")
            
            p1, p2 = st.columns(2)
            with p1: 
                st.text_input("Min", value="0", key='min_text', disabled=True)
            with p2: 
                if 'max_text' not in st.session_state:
                    st.session_state['max_text'] = str(int(st.session_state['price_max']))
                
                st.text_input(
                    "Max", 
                    key='max_text', 
                    on_change=update_price_from_text,
                    help="Must be greater than 0"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🎧 Customer Service", use_container_width=True):
                st.session_state['show_chatbot'] = True
                st.rerun()

        with c_prod:
            title_map = {
                'all': "All Products", 
                'seeds': "Browse Seeds", 
                'Leafy Greens': "Leafy Greens",
                'Fruiting Veg': "Fruiting Vegetables",
                'Fruit': "Fruits",
                'Vegetable': "Vegetables"
            }
            # Fallback for category names that might not exactly match key
            page_title = title_map.get(st.session_state['view_category'], st.session_state['view_category'])
            st.markdown(f"##### {page_title}")

            filtered_products = products
            
            # Filtering Logic
            if search_query:
                filtered_products = [
                    p for p in products 
                    if search_query.lower() in p['name'].lower() 
                    or search_query.lower() in p['category'].lower()
                ]
                filtered_products = [
                    p for p in filtered_products 
                    if st.session_state['price_min'] <= p['price'] <= st.session_state['price_max']
                ]
            else:
                current_view = st.session_state['view_category']
                
                if current_view == 'seeds':
                    # Just show everything since equipment is gone
                    pass 
                elif current_view != 'all':
                    filtered_products = [p for p in filtered_products if p['category'] == current_view]
                    
                filtered_products = [
                    p for p in filtered_products 
                    if st.session_state['price_min'] <= p['price'] <= st.session_state['price_max']
                ]
            
            if not filtered_products:
                st.warning("No products found matching your criteria.")

            # Grid Layout
            rows = [filtered_products[i:i + 3] for i in range(0, len(filtered_products), 3)]
            for row in rows:
                cols = st.columns(3, gap="medium")
                for i, p in enumerate(row):
                    with cols[i]:
                        with st.container(border=True):
                            st.markdown(f"""
                                <div style="height: 200px; overflow: hidden; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: center; align-items: center; background-color: #f8f9fa;">
                                    <img src="{p['image']}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown(f"*{p['name']}*")
                            # REMOVED: Rating display
                            st.markdown(f"*RM {p['price']:.2f}*")
                            
                            if st.button("ORDER", key=f"select_{p['id']}", use_container_width=True):
                                st.session_state['selected_product'] = p
                                st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)