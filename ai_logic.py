import joblib
import pandas as pd
import os

# --- CONFIGURATION ---
MODEL_PATH = 'seed_predictor_model.pkl'
ENCODER_PATH = 'label_encoder.pkl'

def load_ai():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        return None, None, "AI models not found. Run train_ai.py first."
    try:
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        return model, encoder, "Success"
    except Exception as e:
        return None, None, str(e)

def get_month_flags(month):
    """
    Determines the cultural/weather flags for a given month.
    Matches logic in data_gen.py
    """
    return {
        'is_monsoon': 1 if month in [11, 12] else 0,
        'is_hot': 1 if month in [3, 4, 5] else 0,
        'is_holiday': 1 if month in [2, 12] else 0,
        'is_cny': 1 if month in [1, 2] else 0,
        'is_ramadan': 1 if month == 3 else 0,
        'is_deepavali': 1 if month == 10 else 0
    }

def get_forecast_reason(month, peak_month, days_to_grow, product_name):
    """
    Returns the 'Why' behind the prediction using Cultural Context.
    """
    flags = get_month_flags(month)
    
    # 1. Cultural Events (High Priority)
    if flags['is_deepavali'] and any(x in product_name for x in ["Okra", "Eggplant", "Bitter Gourd", "Long Bean"]):
        return "🪔 **Deepavali Peak**: High demand for traditional Indian cooking vegetables."
    
    if flags['is_ramadan']:
        if "Watermelon" in product_name: return "🌙 **Ramadan Special**: High demand for fruits during fasting month."
        if "Cucumber" in product_name or "Chilli" in product_name: return "🌙 **Ramadan Cooking**: Increased usage in daily meals."

    if flags['is_cny'] and any(x in product_name for x in ["Leafy", "Fruit", "Pak Choy"]):
        return "🧧 **CNY Season**: High demand for reunion dinner vegetables."

    # 2. Weather
    if flags['is_monsoon']:
        return "🌧️ **Monsoon Season**: Heavy rain reduces planting activity."
    
    # 3. Standard Farming Logic
    if peak_month == 0:
        return "🔄 **Steady Staple**: Consistently consumed year-round."

    if peak_month < month: effective_peak = peak_month + 12
    else: effective_peak = peak_month
        
    months_until_peak = effective_peak - month
    
    if 1 <= months_until_peak <= 3:
        return f"🚀 **Planting Window**: Farmers buying NOW for harvest in {months_until_peak} months."
    elif months_until_peak == 0:
        return "🔻 **Harvest Time**: Farmers are harvesting, not buying seeds."
    else:
        return "📉 **Off-Season**: Low market interest."

def get_yearly_predictions(product_name, days_to_grow, peak_month):
    model, encoder, status = load_ai()
    if not model: return pd.DataFrame()

    try:
        product_encoded = encoder.transform([product_name])[0]
    except ValueError: return pd.DataFrame()

    predictions = []
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for i in range(1, 13):
        flags = get_month_flags(i)
        
        # Prepare input with ALL 8 FEATURES
        input_data = pd.DataFrame({
            'product_encoded': [product_encoded],
            'month': [i],
            'is_monsoon': [flags['is_monsoon']],
            'is_hot': [flags['is_hot']],
            'is_holiday': [flags['is_holiday']],
            'is_cny': [flags['is_cny']],
            'is_ramadan': [flags['is_ramadan']],
            'is_deepavali': [flags['is_deepavali']]
        })
        
        pred_qty = int(model.predict(input_data)[0])
        reason = get_forecast_reason(i, peak_month, days_to_grow, product_name)
        
        predictions.append({
            "MonthID": i,
            "Month": month_names[i-1],
            "Predicted Demand": max(10, pred_qty),
            "AI Reasoning": reason
        })
    
    return pd.DataFrame(predictions)

def predict_simulation(product_name, simulated_month, days_to_grow, peak_month):
    model, encoder, status = load_ai()
    if not model: return 0, "AI Error"

    try:
        product_encoded = encoder.transform([product_name])[0]
    except ValueError: return 0, "Unknown Product"

    flags = get_month_flags(simulated_month)

    input_data = pd.DataFrame({
        'product_encoded': [product_encoded],
        'month': [simulated_month],
        'is_monsoon': [flags['is_monsoon']],
        'is_hot': [flags['is_hot']],
        'is_holiday': [flags['is_holiday']],
        'is_cny': [flags['is_cny']],
        'is_ramadan': [flags['is_ramadan']],
        'is_deepavali': [flags['is_deepavali']]
    })
    
    pred_qty = int(model.predict(input_data)[0])
    reason = get_forecast_reason(simulated_month, peak_month, days_to_grow, product_name)
    
    return max(0, pred_qty), reason