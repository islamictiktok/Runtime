import time
import requests
import threading
import os
from flask import Flask, jsonify

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

# قيمة الكوكيز التي تم استخراجها من متصفحك (لتخطي الحماية)
TEST_COOKIE_VALUE = "77d33aa5d6eabcab5b54cac26dd8519e"

def monitor_bot():
    print("🚀 بدء المراقبة باستخدام تصريح الدخول (Cookie) السري...", flush=True)
    
    # تنكر كمتصفح حقيقي
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    # تمرير رخصة المرور للاستضافة لكي تتخطى صفحة الحماية
    cookies = {
        '__test': TEST_COOKIE_VALUE
    }
    
    while True:
        try:
            response = requests.get(URL, headers=headers, cookies=cookies, timeout=10)
            
            try:
                data = response.json()
                msg = data.get('message', 'بدون رسالة')
                print(f"✅ [نجاح] {msg}", flush=True)
            except ValueError:
                print(f"⚠️ [رد غير متوقع] تم حظر الطلب أو الرد ليس JSON. كود الرد: {response.status_code}", flush=True)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ [خطأ اتصال] السيرفر لا يستجيب: {e}", flush=True)
        
        # الانتظار 5 ثوانٍ
        time.sleep(5)

# تشغيل حلقة المراقبة في الخلفية
threading.Thread(target=monitor_bot, daemon=True).start()

# واجهة الويب التي سيقرأها موقع UptimeRobot
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
