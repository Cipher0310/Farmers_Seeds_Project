import streamlit as st
import sqlite3
import pandas as pd
import altair as alt 
from ai_engine import SeedAI  # <--- UPDATED IMPORT
import time
import calendar # <--- ADDED for month names

# --- CUSTOM CSS ---
def load_css():
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] > div:first-child button { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        div[data-testid="stDecoration"] { display: none !important; }

        .stApp {
            background-image: linear-gradient(rgba(250, 249, 246, 0.96), rgba(250, 249, 246, 0.96)), 
            url('https://images.unsplash.com/photo-1610348725531-843dff563e2c?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }

        section[data-testid="stSidebar"] {
            background-color: #3A5A40;
            border-right: 2px solid #243828;
        }
        section[data-testid="stSidebar"] * {
            color: #FAF9F6 !important; 
        }

        .stSelectbox label p, .stSlider label p, .stNumberInput label p, .stTextInput label p {
            color: #000000 !important; font-weight: 800 !important; font-size: 1.1rem !important;
        }
        [data-testid="stMetricLabel"] div {
            color: #000000 !important; font-weight: 800 !important;
        }
        [data-testid="stMetricValue"] div {
            color: #3A5A40 !important;
        }
        div[data-testid="stCaptionContainer"] p {
            color: #000000 !important; font-weight: 700 !important; opacity: 1 !important;
        }
        
        div[data-baseweb="tab-list"] button {
            color: #1a291d !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
        }
        div[data-baseweb="tab-list"] button:focus {
            background-color: rgba(58, 90, 64, 0.1) !important;
        }

        .ai-container {
            background-color: #F1F8E9; border: 2px solid #3A5A40; border-radius: 15px; padding: 25px; margin-top: 20px; margin-bottom: 30px;
        }
        .ai-title { color: #3A5A40; font-weight: 900; font-size: 1.5rem; margin-bottom: 10px; }
        .ai-desc { color: #333333; font-weight: 600; margin-bottom: 20px; }

        .summary-container { display: flex; gap: 20px; margin-bottom: 30px; }
        .summary-card {
            background-color: white; padding: 25px; border-radius: 12px;
            border: 1px solid #d4d1c9; flex: 1; text-align: center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }
        .summary-value { color: #3A5A40; font-size: 2.2rem; font-weight: 800; }
        .summary-label { color: #666; font-weight: bold; }
        
        div.stButton > button { background-color: #D62828; color: white; border: none; font-weight: bold; }
        div.stButton > button:hover { background-color: #a81c1c; color: white; }
        
        h1, h2, h3 { color: #3A5A40 !important; font-weight: 800; }

        .custom-info {
            background-color: #E3F2FD;
            color: #000000 !important;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #2196F3;
            font-weight: 700 !important;
            margin-bottom: 15px;
            font-size: 1rem;
        }
        .danger-info {
            background-color: #FFEBEE;
            color: #B71C1C !important;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #D32F2F;
            font-weight: 700 !important;
            margin-bottom: 15px;
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- DATABASE FUNCTIONS ---
def get_data():
    conn = sqlite3.connect('database.db')
    df_products = pd.read_sql_query("SELECT * FROM products", conn)
    df_sales = pd.read_sql_query("""
        SELECT strftime('%Y-%m', date_sold) as month, SUM(quantity) as total_qty
        FROM sales_history GROUP BY month ORDER BY month
    """, conn)
    conn.close()
    
    # FETCH USERNAME FROM SESSION
    username = st.session_state.get('username', 'Supplier')
    farm_name = "Green Valley Farms"
    
    return farm_name, username, df_products, df_sales

def update_stock_in_db(product_name, new_stock):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock = ? WHERE name = ?", (new_stock, product_name))
    conn.commit()
    conn.close()

def add_product_to_db(name, category, price, stock, grow_days, peak_month):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, category, price, stock, days_to_grow, peak_month) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, price, stock, grow_days, peak_month))
    conn.commit()
    conn.close()

def delete_product_from_db(product_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
    result = cursor.fetchone()
    if result:
        p_id = result[0]
        cursor.execute("DELETE FROM sales_history WHERE product_id = ?", (p_id,))
        cursor.execute("DELETE FROM products WHERE id = ?", (p_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

# --- MAIN DASHBOARD FUNCTION ---
def show_dashboard():
    load_css()
    
    # --- INITIALIZE NEW AI ENGINE ---
    try:
        ai = SeedAI()
    except Exception as e:
        st.error(f"⚠️ AI Engine Error: {e}. Ensure 'train_ai.py' has been run.")
        st.stop()

    try:
        farm_name, username, df_products, df_sales = get_data()
    except Exception as e:
        st.error(f"Database Error: {e}")
        st.stop()

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/497/497348.png", width=100) 
        st.title("SeSeed")
        st.markdown("**MANAGER PORTAL**")
        st.markdown("---")
        st.write(f"User: **{username}**")
        st.write(f"Farm: **{farm_name}**")
        st.markdown("<br><br>", unsafe_allow_html=True)

    # --- HEADER ---
    c1, c2 = st.columns([8,1])
    c1.title(f"{farm_name} Dashboard")
    
    if c2.button("🚪 Log Out"):
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['show_login'] = False
        st.rerun()
        
    st.markdown("---")

    # 1. METRICS
    total_stock = df_products['stock'].sum() if not df_products.empty else 0
    est_value = (df_products['price'] * df_products['stock']).sum() if not df_products.empty else 0
    low_stock_count = len(df_products[df_products['stock'] < 30]) if not df_products.empty else 0
    
    alert_border = '#D62828' if low_stock_count > 0 else '#3A5A40'
    alert_class = 'alert-text' if low_stock_count > 0 else ''

    st.markdown(f"""
    <div class="summary-container">
        <div class="summary-card">
            <span class="summary-icon">📦</span>
            <div class="summary-label">Total Stock</div>
            <div class="summary-value">{total_stock}</div>
        </div>
        <div class="summary-card">
            <span class="summary-icon">💰</span>
            <div class="summary-label">Inventory Value</div>
            <div class="summary-value">RM {est_value:,.2f}</div>
        </div>
        <div class="summary-card" style="border-bottom: 5px solid {alert_border};">
            <span class="summary-icon">⚠️</span>
            <div class="summary-label">Alerts</div>
            <div class="summary-value {alert_class}">{low_stock_count}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. AI FORECAST GRAPH (UPDATED TO CONNECT TO AI_ENGINE.PY)
    st.markdown('<div class="ai-container">', unsafe_allow_html=True)
    st.markdown('<div class="ai-title">🧠 AI Demand Forecast (Next 12 Months)</div>', unsafe_allow_html=True)
    st.markdown('<div class="ai-desc">Visualizing future demand trends. Hover over the dots to see AI Reasoning.</div>', unsafe_allow_html=True)

    if not df_products.empty:
        product_names = df_products['name'].tolist()
        selected_name = st.selectbox("Select Product to Forecast:", product_names)

        product_row = df_products[df_products['name'] == selected_name].iloc[0]
        current_stock = product_row['stock']
        
        # --- NEW FORECAST LOGIC ---
        forecast_data = []
        for m in range(1, 13):
            # Calls your new reasoning engine
            prediction = ai.predict_with_reasoning(selected_name, m)
            
            # Map Month Number (1) -> Name (Jan)
            month_name = calendar.month_abbr[m]
            
            forecast_data.append({
                "Month": month_name,
                "Predicted Demand": prediction['Predicted_Sales'],
                "AI Reasoning": prediction['Reasoning']
            })

        forecast_df = pd.DataFrame(forecast_data)

        if not forecast_df.empty:
            # Sort order for the chart (Jan -> Dec)
            month_order = list(calendar.month_abbr[1:])
            
            base = alt.Chart(forecast_df).encode(
                x=alt.X('Month', sort=month_order, title="Month"),
                y=alt.Y('Predicted Demand', title="Predicted Units Sold")
            )
            line = base.mark_line(color='#3A5A40', strokeWidth=4)
            points = base.mark_circle(size=120, color='#3A5A40').encode(
                tooltip=['Month', 'Predicted Demand', 'AI Reasoning']
            )
            
            # Stock Line
            stock_line = alt.Chart(pd.DataFrame({'y': [current_stock]})).mark_rule(color='#D62828', strokeDash=[5,5]).encode(y='y')
            
            final_chart = (line + points + stock_line).properties(height=400).interactive()
            st.altair_chart(final_chart, use_container_width=True)
            
            col_stat1, col_stat2 = st.columns(2)
            col_stat1.caption(f"🔴 Red Dashed Line = Current Stock ({current_stock} units)")
            col_stat2.caption("🟢 Green Line = Predicted Demand")
        else:
            st.warning("Not enough data to generate forecast.")
    else:
        st.warning("No products in database.")

    st.markdown('</div>', unsafe_allow_html=True)

    # 3. INVENTORY MANAGEMENT
    st.subheader("🛠️ Inventory Management")

    tab1, tab2, tab3 = st.tabs(["📝 Update Stock", "➕ Add New Seed", "🗑️ Delete Seed"])

    with tab1:
        st.markdown('<div class="custom-info">ℹ️ Select a product below to update its stock level immediately.</div>', unsafe_allow_html=True)
        if not df_products.empty:
            c_up1, c_up2, c_up3 = st.columns([2, 1, 1])
            with c_up1:
                prod_to_update = st.selectbox("Product:", product_names, key="stock_select")
                curr_val = int(df_products[df_products['name'] == prod_to_update]['stock'].values[0])
            with c_up2:
                new_stock_val = st.number_input("New Stock Level:", min_value=0, max_value=10000, value=curr_val)
            with c_up3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Update Stock"):
                    update_stock_in_db(prod_to_update, new_stock_val)
                    st.success(f"Updated {prod_to_update} to {new_stock_val}!")
                    time.sleep(1) 
                    st.rerun() 

    with tab2:
        st.markdown('<div class="custom-info">➕ Add a new seed variety to the database. The AI will immediately begin analyzing it.</div>', unsafe_allow_html=True)
        with st.form("add_product_form"):
            c_add1, c_add2 = st.columns(2)
            with c_add1:
                new_name = st.text_input("Seed Name (e.g., 'Golden Pumpkin Seeds')")
                new_cat = st.selectbox("Category", ["Vegetable", "Fruit", "Fruiting Veg", "Leafy Green", "Herb"])
                new_price = st.number_input("Price (RM)", min_value=0.5, value=5.0)
            with c_add2:
                new_stock = st.number_input("Initial Stock", min_value=0, value=100)
                new_grow = st.number_input("Days to Grow", min_value=20, value=60)
                new_peak = st.selectbox("Peak Harvest Month (0 = Year Round)", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            submitted = st.form_submit_button("🌱 Add Product")
            if submitted:
                if new_name:
                    add_product_to_db(new_name, new_cat, new_price, new_stock, new_grow, new_peak)
                    st.toast(f"Success! {new_name} added to inventory.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter a product name.")

    with tab3:
        st.markdown('<div class="danger-info">⚠️ <b>WARNING:</b> Deleting a product will also permanently wipe its sales history and AI learning data. This cannot be undone.</div>', unsafe_allow_html=True)
        if not df_products.empty:
            c_del1, c_del2 = st.columns([2, 1])
            with c_del1:
                prod_to_delete = st.selectbox("Select Product to Permanently Delete:", product_names, key="delete_select")
            with c_del2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Delete Product"):
                    success = delete_product_from_db(prod_to_delete)
                    if success:
                        st.error(f"Deleted {prod_to_delete} from database.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Could not find product.")

    st.markdown("---")

    # 4. LIVE INVENTORY TABLE
    st.subheader("📦 Live Inventory")
    if not df_products.empty:
        max_stock_val = int(df_products['stock'].max())
        
        # COPY Dataframe so we don't mess up the original data
        df_display = df_products.copy()
        df_display['stock'] = df_display['stock'].astype(int)

        # FILTER COLUMNS: Show only relevant columns (Hide images/desc)
        cols_to_keep = ["name", "category", "price", "stock", "days_to_grow", "peak_month"]
        df_display = df_display[cols_to_keep]

        st.dataframe(
            df_display,
            use_container_width=True,
            height=300,
            column_config={
                "name": "Product",
                "category": "Type",
                "stock": st.column_config.ProgressColumn(
                    "Stock", 
                    format="%d", 
                    min_value=0, 
                    max_value=max(200, max_stock_val)
                ),
                "days_to_grow": "Growth Days",
                "peak_month": "Peak Month (0=All)",
                # UPDATED: Price column simplified
                "price": st.column_config.NumberColumn("Price (RM)", format="%.2f") 
            },
            hide_index=True
        )
    else:
        st.info("Inventory is empty. Add a product above.")

    st.subheader("📈 Overall Sales History")
    if not df_sales.empty:
        st.bar_chart(df_sales.set_index('month'), color='#3A5A40')