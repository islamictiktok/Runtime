import time
import requests
import threading
import os
import re
from flask import Flask, jsonify
from Crypto.Cipher import AES

app = Flask(__name__)

# تم تعديل الرابط ليعمل على http بدلاً من https
URL = "http://btccryptoscan.42web.io/api.php?action=scan"

def solve_infinityfree_challenge(html):
    """
    دالة الهندسة العكسية:
    تقرأ اللغز الرياضي من صفحة الحماية وتفُك التشفير لتوليد رخصة مرور (Cookie)
    """
    try:
        # استخراج المتغيرات الثلاثة من كود الجافاسكربت (المفتاح، متجه التهيئة، النص المشفر)
        matches = re.findall(r'toNumbers\("([a-f0-9]+)"\)', html)
        if len(matches) >= 3:
            key = bytes.fromhex(matches[0])
            iv = bytes.fromhex(matches[1])
            ciphertext = bytes.fromhex(matches[2])
            
            # فك تشفير AES-CBC رياضياً (كما يفعل المتصفح تماماً)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext)
            
            # تحويل النتيجة لـ Hex لتصبح كوكيز صالح للاستخدام
            return plaintext.hex()
    except Exception as e:
        print(f"❌ خطأ أثناء فك التشفير: {e}")
    return None

def monitor_bot():
    print("🚀 بدء المراقبة مع محرك الهندسة العكسية لفك تشفير InfinityFree...", flush=True)
    
    # استخدام Session للحفاظ على الكوكيز بين الطلبات
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    })
    
    while True:
        try:
            # 1. إرسال الطلب للاستضافة
            response = session.get(URL, timeout=15)
            
            # 2. إذا واجهنا جدار الحماية (aes.js)
            if "aes.js" in response.text and "toNumbers" in response.text:
                print("⚠️ [جدار الحماية] تم اكتشاف قفل InfinityFree، جاري الاختراق الرياضي...", flush=True)
                test_cookie = solve_infinityfree_challenge(response.text)
                
                if test_cookie:
                    print(f"🔓 [اختراق ناجح] تم توليد رخصة مرور شرعية: {test_cookie[:12]}...", flush=True)
                    # تركيب الكوكيز الجديد للـ Domain الخاص بك
                    session.cookies.set('__test', test_cookie, domain='btccryptoscan.42web.io', path='/')
                    
                    # إعادة إرسال الطلب بعد تخطي الحماية
                    response = session.get(URL, timeout=15)
                else:
                    print("❌ [فشل] لم أتمكن من استخراج معادلة التشفير.", flush=True)
            
            # 3. قراءة النتيجة
            try:
                data = response.json()
                msg = data.get('message', 'تم الفحص بنجاح')
                print(f"✅ [نجاح] {msg}", flush=True)
            except ValueError:
                # طباعة الرد إذا استمر الحظر أو ظهر خطأ جديد
                snippet = response.text[:60].replace('\n', ' ')
                print(f"⚠️ [رد غير متوقع] {snippet}...", flush=True)
                
        except Exception as e:
            print(f"❌ [خطأ اتصال]: {e}", flush=True)
        
        # الانتظار 15 ثانية لتحديث البيانات دون التسبب في حظر موقعك
        time.sleep(15)

threading.Thread(target=monitor_bot, daemon=True).start()

@app.route('/')
def health_check():
    return jsonify({
        "status": "200 OK",
        "message": "SMC Quant Bot bypassed InfinityFree with Reverse Engineering!",
        "service": "Active"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
