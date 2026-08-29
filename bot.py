import time
import threading
import os
import json
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

def monitor_bot():
    print("🚀 تجهيز المتصفح الخفي (Headless Browser) لتخطي الحماية...", flush=True)
    
    # تشغيل Playwright
    with sync_playwright() as p:
        # تشغيل متصفح كروميوم حقيقي (مخفي) مع إغلاق وضع الحماية ليعمل على سيرفرات ريندر
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page()
        
        while True:
            try:
                # المتصفح الحقيقي سيزور الرابط ويحل لغز الجافاسكربت تلقائياً
                page.goto(URL, timeout=15000)
                
                # قراءة النص الموجود في الصفحة
                content = page.inner_text("body")
                
                try:
                    # تحويل النص إلى JSON وطباعته
                    data = json.loads(content)
                    msg = data.get('message', 'تم الفحص')
                    print(f"✅ [نجاح] {msg}", flush=True)
                except json.JSONDecodeError:
                    # إذا ظهرت رسالة أخرى، نطبع أول 60 حرف منها
                    print(f"⚠️ [تخطي الحماية] {content[:60]}...", flush=True)
                    
            except Exception as e:
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
        "message": "SMC Quant Bot is running with Headless Browser!",
        "service": "Active"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
