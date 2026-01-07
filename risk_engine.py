import yfinance as yf
import numpy as np
from scipy.stats import norm
from pymongo import MongoClient
from datetime import datetime

# --- 1. MongoDB Setup ---

MONGO_URI = "mongodb+srv://Pawan_Yadav_084:Pawan123@pawan.wy2hqmv.mongodb.net/?appName=Pawan" 

try:
    client = MongoClient(MONGO_URI)
    db = client['WealthTech']
    collection = db['RiskMetrics']
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f" MongoDB Connection Error: {e}")

# --- 2. Risk Calculation Logic ---

def calculate_var(ticker, amount_invested, confidence_level=0.95):
   
    data = yf.download(ticker, period="1y", progress=False)['Close']   
    
    returns = data.pct_change().dropna()
     
    avg_return = np.mean(returns)
    std_dev = np.std(returns)
      
    z_score = norm.ppf(confidence_level)
    
    var_value = amount_invested * (avg_return - (z_score * std_dev))
    
    final_risk = abs(float(var_value.iloc[0]) if hasattr(var_value, 'iloc') else float(var_value))
    return final_risk

def run_stress_test(investment, crash_percent=0.25):
    """
    Check karta hai ki agar market X% gir jaye toh kitna loss hoga.
    Default crash hum 25% (Market Crash) maan kar chal rahe hain.
    """
    potential_loss = investment * crash_percent
    remaining_value = investment - potential_loss
    return potential_loss, remaining_value

# --- 3. Execution Database Storage ---
if __name__ == "__main__":
    ticker_symbol = "BTC-USD"
    investment_amount = 100000 
    
    print(f"Analyzing {ticker_symbol}...")
    risk_val = calculate_var(ticker_symbol, investment_amount)
   
    crash_loss, final_val = run_stress_test(investment_amount, 0.25)
    
    data_to_save = {
        "asset": "Bitcoin",
        "ticker": ticker_symbol,
        "investment": investment_amount,
        "var_95": round(risk_val, 2),
        "stress_test_loss": round(crash_loss, 2),
        "stress_test_remaining": round(final_val, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
collection.insert_one(data_to_save)
print(f"Risk: ₹{round(risk_val, 2)} | Stress Loss: ₹{round(crash_loss, 2)}")
print("✅ Full Report saved to MongoDB!")
