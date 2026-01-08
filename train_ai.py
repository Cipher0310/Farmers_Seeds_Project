import sqlite3
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# 1. SETUP PATHS
# We look for database.db in the same folder as this script
db_path = "database.db"

print(f"Connecting to database at: {db_path}")
conn = sqlite3.connect(db_path)

# 2. LOAD DATA (Including all 6 Context Flags)
query = """
SELECT sh.date_sold, p.name, sh.quantity, 
       sh.is_monsoon, sh.is_hot, sh.is_holiday, sh.is_cny, sh.is_ramadan, sh.is_deepavali
FROM sales_history sh
JOIN products p ON sh.product_id = p.id
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 3. PREPARE DATE FEATURES
df['date_sold'] = pd.to_datetime(df['date_sold'])
df['month'] = df['date_sold'].dt.month
df['year'] = df['date_sold'].dt.year

# 4. AGGREGATE DATA
# We sum up the sales by Month + All Flags
monthly_df = df.groupby([
    'name', 'year', 'month', 
    'is_monsoon', 'is_hot', 'is_holiday', 'is_cny', 'is_ramadan', 'is_deepavali'
])['quantity'].sum().reset_index()

# 5. ENCODE PRODUCT NAMES
le = LabelEncoder()
monthly_df['product_encoded'] = le.fit_transform(monthly_df['name'])

# 6. DEFINE INPUTS (X) AND TARGET (y)
X = monthly_df[[
    'product_encoded', 'month', 
    'is_monsoon', 'is_hot', 'is_holiday', 'is_cny', 'is_ramadan', 'is_deepavali'
]]
y = monthly_df['quantity']

# 7. SPLIT & TRAIN
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Cultural-Aware AI Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. SAVE THE BRAIN
joblib.dump(model, 'seed_predictor_model.pkl')
joblib.dump(le, 'label_encoder.pkl')

print("SUCCESS: AI trained with Cultural Awareness!")