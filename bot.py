import time
import requests
from datetime import datetime

# الرابط الخاص بموقعك
URL = "https://btccryptoscan.42web.io/api.php?action=scan"

print("🚀 بدء تشغيل البوت... سيتم فحص الرابط كل 10 ثوانٍ.")
print(f"🔗 الرابط المستهدف: {URL}")
print("-" * 50)

while True:
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # إرسال الطلب مع مهلة 15 ثانية لتجنب تعليق السكربت
        response = requests.get(URL, timeout=15)
        
        # محاولة قراءة الرسالة القادمة من موقعك
        try:
            data = response.json()
            message = data.get('message', 'تم التنفيذ بنجاح')
            print(f"[{current_time}] ✅ {message}")
        except ValueError:
            # في حال كان الرد ليس JSON (مثلاً خطأ من الاستضافة)
            print(f"[{current_time}] ⚡ تم الوصول للرابط (Status: {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        # التقاط أي خطأ في الاتصال (انقطاع إنترنت، سيرفر واقع) لكي لا يتوقف البوت
        print(f"[{current_time}] ❌ خطأ في الاتصال: {e}")
    
    # الانتظار 10 ثوانٍ قبل المحاولة التالية
    time.sleep(10)
