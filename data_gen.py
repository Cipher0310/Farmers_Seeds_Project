import sqlite3
import random
import os
import base64
from datetime import datetime, timedelta

# --- CONFIGURATION ---
DB_PATH = "database.db"
START_DATE = datetime(2023, 1, 1) # 3 Years of Data
DAYS_TO_GENERATE = 365 * 3

# Fallback image (Online URL to prevent crashes if local files missing)
seed_packet_image_url = "https://images.unsplash.com/photo-1523301343968-6a6ebf63c672?w=400"

# --- 1. IMAGE HELPER FUNCTIONS ---
def get_base64_of_bin_file(filename):
    """
    Reads a local image file from the 'images' folder and converts it to base64.
    """
    # FIX: Look inside the 'images' folder
    bin_file = os.path.join("images", filename)
    
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def get_img(local_data, fallback_url):
    """
    Returns the base64 string if available, otherwise the fallback URL.
    """
    if local_data:
        return f"data:image/png;base64,{local_data}"
    return fallback_url

# --- 2. LOAD LOCAL IMAGES ---
print("Loading local images from 'images/' folder...")

# Make sure your filenames in the 'images' folder match these exactly!
local_kangkung_img = get_base64_of_bin_file("kangkung.png")
local_ks_img = get_base64_of_bin_file("ks.png") 
local_kt_img = get_base64_of_bin_file("kt.png") 

local_sawi_img = get_base64_of_bin_file("sawihijau.png") 
local_shs_img = get_base64_of_bin_file("shs.png") 
local_sht_img = get_base64_of_bin_file("sht.png") 

local_cili_img = get_base64_of_bin_file("cilikulai.png")
local_cks_img = get_base64_of_bin_file("cks.png") 
local_ckt_img = get_base64_of_bin_file("ckt.png") 

local_cucumber_img = get_base64_of_bin_file("cucumber.png")
local_cs_img = get_base64_of_bin_file("cs.png") 
local_ct_img = get_base64_of_bin_file("ct.png") 

local_sweetcorn_img = get_base64_of_bin_file("sweetcorn.png")
local_scs_img = get_base64_of_bin_file("scs.png") 
local_sct_img = get_base64_of_bin_file("sct.png") 

local_orka_img = get_base64_of_bin_file("orka.png")
local_os_img = get_base64_of_bin_file("os.png") 
local_ot_img = get_base64_of_bin_file("ot.png") 

local_bittergourd_img = get_base64_of_bin_file("bittergourd.png")
local_bgs_img = get_base64_of_bin_file("bgs.png") 
local_bgt_img = get_base64_of_bin_file("bgt.png") 

local_longbean_img = get_base64_of_bin_file("longbean.png")
local_lbs_img = get_base64_of_bin_file("lbs.png")
local_lbt_img = get_base64_of_bin_file("lbt.png")

local_eggplant_img = get_base64_of_bin_file("eggplant.png")
local_es_img = get_base64_of_bin_file("es.png")
local_et_img = get_base64_of_bin_file("et.png")

local_watermelon_img = get_base64_of_bin_file("watermelon.png")
local_ws_img = get_base64_of_bin_file("ws.png") 
local_wt_img = get_base64_of_bin_file("wt.png") 

local_papaya_img = get_base64_of_bin_file("papaya.png")
local_ps_img = get_base64_of_bin_file("ps.png") 
local_pt_img = get_base64_of_bin_file("pt.png") 

local_honeydew_img = get_base64_of_bin_file("honeydew.png")
local_hds_img = get_base64_of_bin_file("hds.png") 
local_hdt_img = get_base64_of_bin_file("hdt.png") 


# --- 3. THE MERGED PRODUCT LIST (12 ITEMS) ---
products_list = [
    # --- LEAFY GREENS ---
    {
        "name": "Kangkung Seeds", 
        "cat": "Leafy Greens", 
        "price": 2.00, 
        "stock": 1000,
        "days_to_grow": 25, 
        "peak_harvest_month": 0, 
        "image": get_img(local_kangkung_img, seed_packet_image_url),
        "image_seed": get_img(local_ks_img, seed_packet_image_url),
        "image_tree": get_img(local_kt_img, seed_packet_image_url),
        "desc": "High-yield water spinach. Harvest as early as 21 days."
    },
    {
        "name": "Choy Sum Seeds", 
        "cat": "Leafy Greens", 
        "price": 2.50, 
        "stock": 1000,
        "days_to_grow": 30, 
        "peak_harvest_month": 0, 
        "image": get_img(local_sawi_img, seed_packet_image_url),
        "image_seed": get_img(local_shs_img, seed_packet_image_url),
        "image_tree": get_img(local_sht_img, seed_packet_image_url),
        "desc": "Flowering White Cabbage. Rich in vitamins."
    },

    # --- FRUITING VEGETABLES ---
    {
        "name": "Chilli Kulai Seeds", 
        "cat": "Fruiting Veg", 
        "price": 12.50, 
        "stock": 1000,
        "days_to_grow": 90, 
        "peak_harvest_month": 4, 
        "image": get_img(local_cili_img, seed_packet_image_url),
        "image_seed": get_img(local_cks_img, seed_packet_image_url),
        "image_tree": get_img(local_ckt_img, seed_packet_image_url),
        "desc": "Premium Cili Kulai grade. Glossy red skin."
    },

    # --- VEGETABLES ---
    {
        "name": "Cucumber Seeds", 
        "cat": "Vegetable", 
        "price": 3.50, 
        "stock": 1000,
        "days_to_grow": 45, 
        "peak_harvest_month": 11, 
        "image": get_img(local_cucumber_img, seed_packet_image_url),
        "image_seed": get_img(local_cs_img, seed_packet_image_url),
        "image_tree": get_img(local_ct_img, seed_packet_image_url),
        "desc": "Crisp, juicy local cucumber."
    },
    {
        "name": "Sweet Corn Seeds", 
        "cat": "Vegetable", 
        "price": 9.00, 
        "stock": 1000,
        "days_to_grow": 70, 
        "peak_harvest_month": 12, 
        "image": get_img(local_sweetcorn_img, seed_packet_image_url),
        "image_seed": get_img(local_scs_img, seed_packet_image_url),
        "image_tree": get_img(local_sct_img, seed_packet_image_url),
        "desc": "Honey Gold Sweet Corn. High sugar content."
    },
    {
        "name": "Okra Seeds", 
        "cat": "Vegetable", 
        "price": 4.00, 
        "stock": 1000,
        "days_to_grow": 60, 
        "peak_harvest_month": 0, 
        "image": get_img(local_orka_img, seed_packet_image_url),
        "image_seed": get_img(local_os_img, seed_packet_image_url),
        "image_tree": get_img(local_ot_img, seed_packet_image_url),
        "desc": "Lady's Finger (Bendi). Heat tolerant."
    },
    {
        "name": "Bitter Gourd Seeds", 
        "cat": "Vegetable", 
        "price": 5.00, 
        "stock": 1000,
        "days_to_grow": 65, 
        "peak_harvest_month": 0, 
        "image": get_img(local_bittergourd_img, seed_packet_image_url),
        "image_seed": get_img(local_bgs_img, seed_packet_image_url),
        "image_tree": get_img(local_bgt_img, seed_packet_image_url),
        "desc": "Peria Katak. Medicinal properties."
    },
    {
        "name": "Long Bean Seeds", 
        "cat": "Vegetable", 
        "price": 4.50, 
        "stock": 1000,
        "days_to_grow": 55, 
        "peak_harvest_month": 0, 
        "image": get_img(local_longbean_img, seed_packet_image_url),
        "image_seed": get_img(local_lbs_img, seed_packet_image_url),
        "image_tree": get_img(local_lbt_img, seed_packet_image_url),
        "desc": "Yardlong Bean. Produces pods up to 70cm."
    },
    {
        "name": "Eggplant Seeds", 
        "cat": "Vegetable", 
        "price": 4.20, 
        "stock": 1000,
        "days_to_grow": 70, 
        "peak_harvest_month": 8, 
        "image": get_img(local_eggplant_img, seed_packet_image_url),
        "image_seed": get_img(local_es_img, seed_packet_image_url),
        "image_tree": get_img(local_et_img, seed_packet_image_url),
        "desc": "Long Brinjal. Soft creamy flesh."
    },

    # --- FRUITS ---
    {
        "name": "Watermelon Seeds", 
        "cat": "Fruit", 
        "price": 6.50, 
        "stock": 1000,
        "days_to_grow": 80, 
        "peak_harvest_month": 6, 
        "image": get_img(local_watermelon_img, seed_packet_image_url),
        "image_seed": get_img(local_ws_img, seed_packet_image_url),
        "image_tree": get_img(local_wt_img, seed_packet_image_url),
        "desc": "Red Sweet Dragon. High sweetness."
    },
    {
        "name": "Papaya Seeds", 
        "cat": "Fruit", 
        "price": 8.00, 
        "stock": 1000,
        "days_to_grow": 240, 
        "peak_harvest_month": 0, 
        "image": get_img(local_papaya_img, seed_packet_image_url),
        "image_seed": get_img(local_ps_img, seed_packet_image_url),
        "image_tree": get_img(local_pt_img, seed_packet_image_url),
        "desc": "Exotica Papaya. Sweet orange-red flesh."
    },
    {
        "name": "Honeydew Seeds (Jade Dew)", 
        "cat": "Fruit", 
        "price": 15.00, 
        "stock": 1000,
        "days_to_grow": 85, 
        "peak_harvest_month": 3, 
        "image": get_img(local_honeydew_img, seed_packet_image_url),
        "image_seed": get_img(local_hds_img, seed_packet_image_url),
        "image_tree": get_img(local_hdt_img, seed_packet_image_url),
        "desc": "Premium Jade Dew. Emerald green flesh."
    }
]

# --- 4. CULTURAL LOGIC ---
def get_context_multiplier(prod, current_date, flags):
    """
    Calculates sales multiplier based on cultural and weather flags.
    """
    m = 1.0
    (monsoon, hot, holiday, cny, ramadan, deepavali) = flags
    
    # 1. WEATHER IMPACTS
    if monsoon: 
        m *= random.uniform(0.4, 0.6) 
        if "Kangkung" in prod["name"]: m *= 0.8 
    if hot and prod["cat"] == "Fruit": m *= random.uniform(1.5, 2.0)

    # 2. CULTURAL IMPACTS
    if cny and prod["cat"] in ["Leafy Greens", "Fruit"]: 
        m *= random.uniform(1.8, 2.4)
    
    if ramadan:
        if "Watermelon" in prod["name"]: m *= random.uniform(2.2, 3.2)
        if "Cucumber" in prod["name"] or "Chilli" in prod["name"]: m *= random.uniform(1.5, 2.0)

    if deepavali:
        if any(x in prod["name"] for x in ["Okra", "Eggplant", "Bitter Gourd", "Long Bean"]): 
            m *= random.uniform(2.2, 3.0)
        elif "Chilli" in prod["name"]: 
            m *= random.uniform(1.8, 2.5)

    # 3. HOLIDAY & GROWTH
    if holiday and ("Corn" in prod["name"] or "Melon" in prod["name"]): 
        m *= random.uniform(1.3, 1.6)

    # Smart Seasonality (Growth Cycle)
    if prod["peak_harvest_month"] != 0:
        target_harvest = datetime(current_date.year, prod["peak_harvest_month"], 15)
        if current_date.month > prod["peak_harvest_month"]:
            target_harvest = target_harvest.replace(year=current_date.year + 1)
        ideal_planting = target_harvest - timedelta(days=prod["days_to_grow"])
        delta = abs((current_date - ideal_planting).days)
        if delta > 182: delta = 365 - delta
        if delta < 30: m *= 2.5 
        
    return m

def generate_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # --- 5. CLEAN SCHEMA (NO REVIEWS/RATINGS) ---
    cursor.execute("DROP TABLE IF EXISTS sales_history")
    cursor.execute("DROP TABLE IF EXISTS products")
    
    # PRODUCTS: Added 3 image columns
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER,
            days_to_grow INTEGER, 
            peak_month INTEGER,
            image TEXT,
            image_seed TEXT,
            image_tree TEXT,
            description TEXT
        )
    ''')

    # SALES HISTORY: Keeps AI Flags
    cursor.execute('''
        CREATE TABLE sales_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            date_sold DATE,
            quantity INTEGER,
            is_monsoon INTEGER,
            is_hot INTEGER,
            is_holiday INTEGER,
            is_cny INTEGER,
            is_ramadan INTEGER,
            is_deepavali INTEGER,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    print(f"Generating Database for {len(products_list)} Products (With 3 Image Columns)...")

    for prod in products_list:
        # Insert Product (No Ratings/Reviews)
        cursor.execute("""
            INSERT INTO products (
                name, category, price, stock, days_to_grow, peak_month,
                image, image_seed, image_tree, description
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prod["name"], prod["cat"], prod["price"], prod["stock"], prod["days_to_grow"], prod["peak_harvest_month"],
            prod["image"], prod["image_seed"], prod["image_tree"], prod["desc"]
        ))
        
        product_id = cursor.lastrowid
        curr = START_DATE
        
        # Generate History
        for _ in range(DAYS_TO_GENERATE):
            # Calculate Flags
            monsoon = 1 if curr.month in [11, 12] else 0
            hot = 1 if curr.month in [3, 4, 5] else 0
            holiday = 1 if curr.month in [2, 12] else 0
            cny = 1 if curr.month in [1, 2] else 0
            ramadan = 1 if curr.month == 3 else 0
            deepavali = 1 if curr.month == 10 else 0
            
            flags = (monsoon, hot, holiday, cny, ramadan, deepavali)
            
            m = get_context_multiplier(prod, curr, flags)
            
            qty = int(random.randint(20, 40) * m)
            
            if qty > 0:
                cursor.execute("""
                    INSERT INTO sales_history (
                        product_id, date_sold, quantity, 
                        is_monsoon, is_hot, is_holiday, is_cny, is_ramadan, is_deepavali
                    ) VALUES (?,?,?,?,?,?,?,?,?)
                """, (product_id, curr.strftime("%Y-%m-%d"), qty, monsoon, hot, holiday, cny, ramadan, deepavali))
            
            curr += timedelta(days=1)
            
    conn.commit()
    conn.close()
    print("--- SUCCESS: Database Created with Images (Packet, Seed, Tree) ---")

# --- 6. FUNCTION TO READ DATA ---
def load_products_from_db():
    """
    Reads all products from the database and returns them as a list of dictionaries.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    products = []
    for row in rows:
        products.append(dict(row))
        
    conn.close()
    return products

if __name__ == "__main__":
    generate_data()