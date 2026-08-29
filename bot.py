import time
import requests
import threading
import os
from flask import Flask, jsonify

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

def monitor_bot():
    # لاحظ إضافة flush=True هنا وفي الأسفل لإجبار السيرفر على عرض النص فوراً
    print("🚀 بدء المراقبة المستمرة كل 5 ثوانٍ...", flush=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    while True:
        try:
            response = requests.get(URL, headers=headers, timeout=10)
            
            try:
                data = response.json()
                msg = data.get('message', 'بدون رسالة')
                print(f"✅ [200 OK] {msg}", flush=True)
            except ValueError:
                print(f"⚠️ [تحذير] الاستضافة ردت بصفحة غير متوقعة (كود: {response.status_code})", flush=True)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ [خطأ اتصال] السيرفر لا يستجيب: {e}", flush=True)
        
        time.sleep(5)

# تشغيل المراقبة
threading.Thread(target=monitor_bot, daemon=True).start()

@app.route('/')
def health_check():
    return jsonify({
        "status": "200 OK",
        "message": "SMC Quant Bot is running perfectly!",
        "service": "Active"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
