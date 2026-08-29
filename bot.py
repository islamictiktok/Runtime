import time
import requests
import threading
import os
from flask import Flask, jsonify

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

# الكوكيز الخاص بك
TEST_COOKIE_VALUE = "77d33aa5d6eabcab5b54cac26dd8519e"

def monitor_bot():
    print("🚀 بدء تشغيل محرك المراقبة مع تخطي جدار الحماية المتقدم...", flush=True)
    
    # بصمة متصفح أندرويد (نفس بيئة هاتفك) + ترويسة AJAX السحرية
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'  # هذه الترويسة تتخطى حماية InfinityFree
    }
    
    cookies = {
        '__test': TEST_COOKIE_VALUE
    }
    
    while True:
        try:
            # استخدام POST بدلاً من GET هي ثغرة معروفة لتخطي حماية الاستضافات المجانية
            response = requests.post(URL, headers=headers, cookies=cookies, timeout=10)
            
            try:
                data = response.json()
                msg = data.get('message', 'بدون رسالة')
                print(f"✅ [نجاح] {msg}", flush=True)
            except ValueError:
                # إذا تم الحظر، سنطبع أول 50 حرف لنرى ماذا ترد الاستضافة
                text_snippet = response.text[:50].replace('\n', ' ')
                print(f"⚠️ [تم الحظر] كود: {response.status_code} | الرد: {text_snippet}...", flush=True)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ [خطأ اتصال]: {e}", flush=True)
        
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
