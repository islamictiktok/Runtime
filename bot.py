import time
import threading
import os
import cloudscraper
from flask import Flask, jsonify

app = Flask(__name__)

# رابط موقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

def monitor_bot():
    print("🚀 بدء المراقبة المستمرة وتخطي حماية الاستضافة...", flush=True)
    
    # استخدام CloudScraper بدلاً من requests العادية لتخطي الجافاسكربت
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    while True:
        try:
            # إرسال الطلب عبر المتصفح الوهمي
            response = scraper.get(URL, timeout=15)
            
            try:
                # محاولة قراءة استجابة موقعك (JSON)
                data = response.json()
                msg = data.get('message', 'بدون رسالة')
                print(f"✅ [نجاح] {msg}", flush=True)
            except ValueError:
                # إذا اعترضتنا صفحة الحماية مجدداً، سنطبع أول 100 حرف لنعرف ما هي
                snippet = response.text[:100].replace('\n', ' ')
                print(f"⚠️ [رد غير متوقع] {snippet}...", flush=True)
                
        except Exception as e:
            print(f"❌ [خطأ اتصال] {e}", flush=True)
        
        # الانتظار 5 ثوانٍ
        time.sleep(5)

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
