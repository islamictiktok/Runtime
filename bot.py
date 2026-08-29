import time
import threading
import os
from flask import Flask, jsonify
from curl_cffi import requests

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

def monitor_bot():
    print("🚀 بدء المراقبة باستخدام بصمة كروم المزورة (curl_cffi)...", flush=True)
    
    while True:
        try:
            # خاصية impersonate="chrome110" تجعل الطلب متطابقاً 100% مع متصفح كروم حقيقي
            response = requests.get(URL, impersonate="chrome110", timeout=15)
            
            try:
                data = response.json()
                msg = data.get('message', 'تم الفحص بنجاح')
                print(f"✅ [نجاح] {msg}", flush=True)
            except ValueError:
                # طباعة الرد إذا كان هناك حظر
                snippet = response.text[:60].replace('\n', ' ')
                print(f"⚠️ [رد غير متوقع] {snippet}...", flush=True)
                
        except Exception as e:
            print(f"❌ [خطأ اتصال]: {e}", flush=True)
        
        # الانتظار 30 ثانية لحماية الاستضافة المجانية من الإغلاق
        time.sleep(30)

# تشغيل حلقة المراقبة في الخلفية
threading.Thread(target=monitor_bot, daemon=True).start()

# واجهة الويب التي سيقرأها موقع UptimeRobot
@app.route('/')
def health_check():
    return jsonify({
        "status": "200 OK",
        "message": "SMC Quant Bot is running perfectly with curl_cffi!",
        "service": "Active"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
