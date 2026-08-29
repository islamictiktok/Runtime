import time
import requests
import threading
import os
from flask import Flask, jsonify

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

def monitor_bot():
    print(f"🚀 بدء المراقبة المستمرة كل 5 ثوانٍ...")
    
    # رأس الطلب (Headers) ليتنكر البوت كمتصفح حقيقي لتخطي حماية InfinityFree
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    while True:
        try:
            # إرسال الطلب
            response = requests.get(URL, headers=headers, timeout=10)
            
            # محاولة قراءة الرسالة من موقعك وطباعتها في شاشة ريندر
            try:
                data = response.json()
                msg = data.get('message', 'بدون رسالة')
                print(f"✅ [200 OK] {msg}")
            except ValueError:
                # إذا ردت الاستضافة بصفحة حماية بدلاً من JSON
                print(f"⚠️ [تحذير] الاستضافة ردت بصفحة غير متوقعة (كود: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ [خطأ اتصال] السيرفر لا يستجيب: {e}")
        
        # الانتظار 5 ثوانٍ
        time.sleep(5)

# تشغيل حلقة المراقبة خارج بلوك __main__ لضمان عملها فور إقلاع سيرفر Render
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
