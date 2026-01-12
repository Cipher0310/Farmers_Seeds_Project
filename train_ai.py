import sqlite3
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# --- CONFIG ---
DB_PATH = "database.db"
MODEL_PATH = "seed_predictor_model.pkl"
ENCODER_PATH = "label_encoder.pkl"

def train_model():
    # 1. Load Data
    conn = sqlite3.connect(DB_PATH)
    
    # We join products to get the name (for encoding)
    query = """
        SELECT 
            p.name as product_name,
            s.date_sold,
            s.quantity,
            s.is_monsoon, s.is_hot, s.is_holiday, 
            s.is_cny, s.is_ramadan, s.is_deepavali
        FROM sales_history s
        JOIN products p ON s.product_id = p.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 2. Preprocessing & Aggregation (Daily -> Monthly)
    # Convert date to datetime
    df['date_sold'] = pd.to_datetime(df['date_sold'])
    df['month'] = df['date_sold'].dt.month
    df['year'] = df['date_sold'].dt.year

    # Aggregate by Month + Product
    # Logic: Sum quantity, but take the MAX of flags (if it happened that month, the flag is True)
    monthly_df = df.groupby(['product_name', 'year', 'month']).agg({
        'quantity': 'sum',
        'is_monsoon': 'max',
        'is_hot': 'max',
        'is_holiday': 'max',
        'is_cny': 'max',
        'is_ramadan': 'max',
        'is_deepavali': 'max'
    }).reset_index()

    print(f"Training on {len(monthly_df)} monthly aggregated records...")

    # 3. Encode Product Names
    le = LabelEncoder()
    monthly_df['product_encoded'] = le.fit_transform(monthly_df['product_name'])

    # 4. Define Features & Target
    # Input: Product ID, Month, and the 6 Context Flags
    X = monthly_df[[
        'product_encoded', 'month', 
        'is_monsoon', 'is_hot', 'is_holiday', 
        'is_cny', 'is_ramadan', 'is_deepavali'
    ]]
    y = monthly_df['quantity']

    # 5. Train Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # 6. Save Artifacts
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(rf, f)
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(le, f)

    print("--- SUCCESS: AI Model Trained & Saved ---")

if __name__ == "__main__":
    train_model()