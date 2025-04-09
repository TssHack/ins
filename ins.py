from instagrapi import Client
import requests
import time
import os
import traceback

# اطلاعات ورود به حساب اینستاگرام
USERNAME = "gpt4_ehsan"
PASSWORD = "ehsan13841386"

# اطلاعات API هوش مصنوعی
API_URL = "https://gpt4-ehsan.liara.run/ehsan/g"
API_LICENSE = "g9s7B3lPZVXN3k2hD2fWgRzOq67d2XKZbgcnqVQ4Ksgg"

# ایجاد یک نمونه از کلاینت اینستاگرام
cl = Client()

# تنظیمات دستگاه شبیه‌سازی شده
cl.device_settings = {
    "app_version": "239.0.0.12.119",
    "android_version": 25,
    "android_release": "7.1.2",
    "dpi": "420dpi",
    "resolution": "1080x1920",
    "manufacturer": "Samsung",
    "model": "Galaxy S9",
    "device": "starlte",
}

# تابع ورود به حساب و ذخیره سشن
def login():
    try:
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings("session.json")
        print("وارد حساب شدی و سشن ذخیره شد.")
    except Exception as e:
        print(f"خطا در ورود: {e}")
        traceback.print_exc()

# تابع دریافت پاسخ از هوش مصنوعی
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
        return f"خطای اتصال به API: {e}"

# ورود به حساب
login()

# دیکشنری برای نگهداری آخرین پیام‌های بررسی‌شده
last_checked = {}

# حلقه اصلی برای بررسی پیام‌ها و پاسخ‌دهی
while True:
    try:
        threads = cl.direct_threads(amount=10)
        for thread in threads:
            messages = sorted(thread.messages, key=lambda m: m.timestamp, reverse=True)
            if not messages:
                continue

            last_message = messages[0]

            # بررسی اینکه پیام از طرف خود ربات نباشد
            if last_message.user_id == cl.user_id:
                continue

            thread_id = thread.id
            message_text = last_message.text
            user_id = str(last_message.user_id)

            if thread_id not in last_checked or last_checked[thread_id] != last_message.id:
                user = cl.user_info(last_message.user_id)
                print(f"پیام جدید از @{user.username}: {message_text}")

                # دریافت پاسخ از هوش مصنوعی
                ai_reply = get_ai_response(message_text, user_id)

                # ارسال پاسخ به دایرکت
                cl.direct_send(ai_reply, [last_message.user_id])

                # ذخیره آی‌دی آخرین پیام بررسی‌شده
                last_checked[thread_id] = last_message.id

        time.sleep(5)

    except Exception as e:
        print(f"خطای کلی: {e}")
        traceback.print_exc()
        time.sleep(10)
