import time
import datetime
import pytz
import subprocess

IST = pytz.timezone("Asia/Kolkata")

def market_is_open():
    now = datetime.datetime.now(IST)
    
    # Monday=0, Sunday=6
    if now.weekday() >= 5:
        return False
    
    market_open = now.replace(hour=9, minute=0, second=0)
    market_close = now.replace(hour=23, minute=30, second=0)
    
    return market_open <= now <= market_close

while True:
    if market_is_open():
        print("Execution Time:", datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"))
        print("🚀 Running Streco main.py")
        subprocess.run(["python", "main.py"])
    else:
        print("Market closed... sleeping")

    # Sleep 30 minutes
    time.sleep(60)
