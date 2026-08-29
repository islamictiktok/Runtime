import time
import requests
import threading
import os
from flask import Flask, jsonify

app = Flask(__name__)

# رابط موقعك الذي سيتم فحصه
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

# 1. دالة المراقبة التي ستعمل في الخلفية
def monitor_bot():
    print(f"🚀 بدء المراقبة المستمرة كل 5 ثوانٍ للرابط: {URL}")
    while True:
        try:
            # مهلة 4 ثواني حتى لا يتراكم الطلب
            response = requests.get(URL, timeout=4)
            print(f"[Ping] Status: {response.status_code}")
        except Exception as e:
            print(f"[Ping Error] {e}")
        
        # الانتظار 5 ثوانٍ بين كل فحص
        time.sleep(5)

# 2. واجهة الويب التي سيقرأها موقع UptimeRobot
@app.route('/')
def health_check():
    # إرجاع استجابة 200 OK مع رسالة تأكيد
    return jsonify({
        "status": "200 OK",
        "message": "SMC Quant Bot is running perfectly!",
        "service": "Active"
    }), 200

if __name__ == '__main__':
    # تشغيل حلقة المراقبة في مسار خلفي (Daemon Thread)
    threading.Thread(target=monitor_bot, daemon=True).start()
    
    # تشغيل سيرفر الويب على المنفذ الذي تحدده Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
