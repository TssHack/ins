from instagrapi import Client
import requests
import time

USERNAME = "gpt4_ehsan"
PASSWORD = "ehsan13841386"
API_URL = "https://gpt4-ehsan.liara.run/ehsan/g"
API_LICENSE = "g9s7B3lPZVXN3k2hD2fWgRzOq67d2XKZbgcnqVQ4Ksgg"

# اتصال به اینستاگرام
cl = Client()
cl.login(USERNAME, PASSWORD)

# ذخیره آخرین پیام پاسخ داده‌شده برای جلوگیری از پاسخ تکراری
last_checked = {}

def get_ai_response(message, user_id):
    try:
        response = requests.get(API_URL, params={
            "q": message,
            "userId": user_id,
            "license": API_LICENSE
        })
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "پاسخی دریافت نشد.")
        else:
            return "خطا در دریافت پاسخ از هوش مصنوعی."
    except Exception as e:
        return f"خطای اتصال: {e}"

while True:
    try:
        threads = cl.direct_threads(amount=10)
        for thread in threads:
            if not thread.messages:
                continue

            last_message = thread.messages[0]
            thread_id = thread.id
            user = thread.users[0]
            user_id = str(user.pk)
            message_text = last_message.text

            if thread_id not in last_checked or last_checked[thread_id] != last_message.id:
                print(f"New message from @{user.username}: {message_text}")

                # گرفتن پاسخ از هوش مصنوعی
                ai_reply = get_ai_response(message_text, user_id)

                # ارسال پاسخ به دایرکت
                cl.direct_send(ai_reply, [user.pk])

                # ذخیره آی‌دی آخرین پیام
                last_checked[thread_id] = last_message.id

        time.sleep(5)
    
    except Exception as e:
        print(f"خطای کلی: {e}")
        time.sleep(10)
