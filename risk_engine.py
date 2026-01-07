"""from pymongo import MongoClient

# MongoDB Setup
# Apni connection string yahan paste karein
client = MongoClient("mongodb+srv://Pawan_Yadav_084:<db_password>@pawan.wy2hqmv.mongodb.net/?appName=Pawan")
db = client['WealthTech']
collection = db['RiskMetrics']

# ... aapka existing calculate_var function ...

if __name__ == "__main__":
    investment = 100000
    risk_val = calculate_var("BTC-USD", investment)
    
    # Data object jo DB mein jayega
    data_to_save = {
        "asset": "Bitcoin",
        "ticker": "BTC-USD",
        "investment": investment,
        "var_95": round(risk_val, 2),
        "timestamp": "2026-01-07" # Aaj ki date
    }
    
    # Database mein save karo
    collection.insert_one(data_to_save)
    print("✅ Data successfully saved to MongoDB!")














# ...existing code...
import yfinance as yf
import numpy as np
from scipy.stats import norm
# ...existing code...
def calculate_var(ticker, amount_invested, confidence_level=0.95):
    # 1. Market data fetch karo (pichle 1 saal ka)
    data = yf.download(ticker, period="1y")['Close']
    
    # 2. Daily Returns calculate karo
    returns = data.pct_change().dropna()
    
    # 3. Standard Deviation (Volatility) nikaalo
    avg_return = np.mean(returns)
    std_dev = np.std(returns)
    
    # 4. Z-Score (95% confidence ke liye 1.65 hota hai)
    z_score = norm.ppf(confidence_level)
    
    # 5. VaR Formula
    # VaR = Investment * (Avg Return - (Z-score * Std Dev))
    var_value = amount_invested * (avg_return - (z_score * std_dev))
    # Purani line ki jagah ye likhein:
    return float(var_value.iloc[0]) if hasattr(var_value, 'iloc') else float(var_value)
    return abs(var_value)
# ...existing code...

# Function ko call karein aur result ko print karein
if __name__ == "__main__":
    investment = 100000  # ₹1 Lakh
    risk = calculate_var("BTC-USD", investment)
    print("\n" + "="*30)
    print(f"Asset: Bitcoin (BTC-USD)")
    print(f"Investment: ₹{investment}")
    print(f"1-Day Risk (VaR 95%): ₹{round(risk, 2)}")
    print("="*30 + "\n")
"""


  
  
  
  
  
  
  
  
"""    from pymongo import MongoClient

# MongoDB Setup
# Apni connection string yahan paste karein
client = MongoClient("mongodb+srv://Pawan_Yadav_084:<db_password>@pawan.wy2hqmv.mongodb.net/?appName=Pawan")
db = client['WealthTech']
collection = db['RiskMetrics']

# ... aapka existing calculate_var function ...

if __name__ == "__main__":
    investment = 100000
    risk_val = calculate_var("BTC-USD", investment)
    
    # Data object jo DB mein jayega
    data_to_save = {
        "asset": "Bitcoin",
        "ticker": "BTC-USD",
        "investment": investment,
        "var_95": round(risk_val, 2),
        "timestamp": "2026-01-07" # Aaj ki date
    }
    
    # Database mein save karo
    collection.insert_one(data_to_save)
    print("✅ Data successfully saved to MongoDB!")     """










import yfinance as yf
import numpy as np
from scipy.stats import norm
from pymongo import MongoClient
from datetime import datetime

# --- 1. MongoDB Setup ---
# MongoDB Atlas se mili hui connection string yahan paste karein
MONGO_URI = "mongodb+srv://Pawan_Yadav_084:Pawan123@pawan.wy2hqmv.mongodb.net/?appName=Pawan" 

try:
    client = MongoClient(MONGO_URI)
    db = client['WealthTech']
    collection = db['RiskMetrics']
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

# --- 2. Risk Calculation Logic ---
def calculate_var(ticker, amount_invested, confidence_level=0.95):
    # Market data fetch karo
    data = yf.download(ticker, period="1y", progress=False)['Close']
    
    # Daily Returns calculate karo
    returns = data.pct_change().dropna()
    
    # Standard Deviation (Volatility) nikaalo
    avg_return = np.mean(returns)
    std_dev = np.std(returns)
    
    # Z-Score calculate karo
    z_score = norm.ppf(confidence_level)
    
    # VaR Formula
    var_value = amount_invested * (avg_return - (z_score * std_dev))
    
    # Sirf number nikalne ke liye clean-up
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

# --- 3. Execution aur Database Storage ---
if __name__ == "__main__":
    ticker_symbol = "BTC-USD"
    investment_amount = 100000 
    
    print(f"Analyzing {ticker_symbol}...")
    risk_val = calculate_var(ticker_symbol, investment_amount)
    
    # Stress Test calculate karein (25% market crash scenario)
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
