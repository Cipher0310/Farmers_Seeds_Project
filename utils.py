import base64
import random

# --- FUNCTION TO LOAD IMAGE AS BASE64 STRING ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    except FileNotFoundError:
        return None

# --- SEASONALITY LOGIC ---
def get_seasonality_multiplier(logic, date):
    """
    Returns a multiplier (e.g., 1.5x for high season) based on 'AI Logic'.
    """
    month = date.month
    multiplier = 1.0

    if logic == "constant":
        return random.uniform(0.9, 1.1)
    elif logic == "rain_sensitive":
        if month in [11, 12]: multiplier = 0.4
        elif month in [1, 2]: multiplier = 0.7
        else: multiplier = 1.1
    elif logic == "festive_peak":
        if month in [1, 2, 3, 4]: multiplier = 1.8
        else: multiplier = 0.8
    elif logic == "school_holiday":
        if month in [2, 3, 5, 12]: multiplier = 1.6
        else: multiplier = 0.9
    elif logic == "hot_season":
        if month in [2, 3, 4]: multiplier = 1.7
        elif month in [11, 12]: multiplier = 0.5
    elif logic == "dual_festival_peak":
        if month in [1, 2]: multiplier = 2.5
        elif month == 9: multiplier = 2.2
        else: multiplier = 0.6
    elif logic == "hot_ramadan_peak":
        if month in [2, 3, 4]: multiplier = 1.5
    
    return multiplier