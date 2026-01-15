import pickle
import pandas as pd
import numpy as np
import os
import warnings

# Suppress the specific sklearn warning about feature names
warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIG (ROBUST PATHS) ---
# Get the folder where this script lives
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Point to the model files in the SAME folder
MODEL_PATH = os.path.join(CURRENT_DIR, "seed_predictor_model.pkl")
ENCODER_PATH = os.path.join(CURRENT_DIR, "label_encoder.pkl")

class SeedAI:
    def __init__(self):
        # Load Model & Encoder
        try:
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            with open(ENCODER_PATH, 'rb') as f:
                self.le = pickle.load(f)
        except FileNotFoundError:
            print(f"ERROR: Model files not found at {MODEL_PATH}")
            print("Please run 'train_ai.py' first.")
            exit()

    def get_context_flags(self, month):
        """
        Hardcoded knowledge base of Malaysian seasons.
        Matches data_gen.py logic exactly.
        """
        return {
            "is_monsoon": 1 if month in [11, 12] else 0,
            "is_hot": 1 if month in [3, 4, 5] else 0,
            "is_holiday": 1 if month in [2, 12] else 0,
            "is_cny": 1 if month in [1, 2] else 0,
            "is_ramadan": 1 if month == 3 else 0,
            "is_deepavali": 1 if month == 10 else 0
        }

    def predict_with_reasoning(self, product_name, month):
        # 1. Prepare Input
        try:
            # Try to convert name to ID
            prod_id = self.le.transform([product_name])[0]
            
            # --- NORMAL PREDICTION PATH (Known Product) ---
            flags = self.get_context_flags(month)
            
            features = [
                prod_id, month, 
                flags['is_monsoon'], flags['is_hot'], flags['is_holiday'], 
                flags['is_cny'], flags['is_ramadan'], flags['is_deepavali']
            ]
            
            baseline_pred = int(self.model.predict([features])[0])
            
            # Reasoning Engine
            reasons = []
            check_list = [
                ('is_ramadan', "Ramadan Spike"),
                ('is_deepavali', "Deepavali Spike"),
                ('is_cny', "CNY Spike"),
                ('is_hot', "Hot Season Demand"),
                ('is_holiday', "School Holiday Surge"),
                ('is_monsoon', "Monsoon Drop")
            ]
            
            idx_map = {
                'is_monsoon': 2, 'is_hot': 3, 'is_holiday': 4, 
                'is_cny': 5, 'is_ramadan': 6, 'is_deepavali': 7
            }
            
            for flag_name, reason_text in check_list:
                if flags[flag_name] == 1:
                    cf_features = features.copy()
                    cf_features[idx_map[flag_name]] = 0
                    cf_pred = int(self.model.predict([cf_features])[0])
                    diff = baseline_pred - cf_pred
                    
                    if diff > 100:
                        reasons.append(reason_text)
                    elif diff < -100:
                        reasons.append(reason_text)

            reason_str = ", ".join(reasons) if reasons else "Standard Seasonal Demand"
            
            return {
                "Product": product_name,
                "Month": month,
                "Predicted_Sales": baseline_pred,
                "Reasoning": reason_str
            }

        except (ValueError, IndexError):
            # --- FALLBACK PATH (Unknown / New Product) ---
            # If the product is new (not in encoder), we return a default "Cold Start" value.
            return {
                "Product": product_name,
                "Month": month,
                "Predicted_Sales": 50,  # Default 'safe' value for new items
                "Reasoning": "🆕 New Product / Insufficient Data"
            }

# --- TEST RUN ---
if __name__ == "__main__":
    ai = SeedAI()
    
    print("--- AI PREDICTION STRESS TEST (UPDATED) ---")
    
    # 1. Hot Season Test (Papaya in May)
    # Expect: "Hot Season Demand"
    print(ai.predict_with_reasoning("Honeydew Seeds (Jade Dew)", 1))

    # 2. Holiday Test (Sweet Corn in December)
    # Expect: "School Holiday Surge" (possibly mixed with Monsoon Drop)
    print(ai.predict_with_reasoning("Sweet Corn Seeds", 12))

    # 3. Ramadan Test (Watermelon in March)
    # Expect: "Ramadan Spike" (and maybe Hot Season Demand too!)
    print(ai.predict_with_reasoning("Watermelon Seeds", 3))