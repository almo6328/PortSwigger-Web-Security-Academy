# IDOR روی فایل‌های استاتیک — نشت لاگ چت

> **Target:** PortSwigger Web Security Academy  
> **Lab:** Insecure direct object references (IDOR)  
> **Difficulty:** Apprentice  
> **Severity:** High  
> **Date:** 17 Tir 1405 (July 8, 2026)  
> **Author:** [Ali (almo6328)](https://github.com/almo6328)

---

## 📋 خلاصه

یک آسیب‌پذیری **IDOR** روی مکانیزم ذخیره فایل‌های استاتیک که به مهاجم اجازه میده با دستکاری نام فایل، لاگ چت کاربران دیگه رو دانلود کنه. نتیجه: دزدی کردنشال و Übernahme کامل اکانت.

---

## 🎯 اندپوینت تحت تاثیر

| فیلد | مقدار |
|-------|-------|
| **Base URL** | `https://0a1900350472af3c80748a930073000b.web-security-academy.net` |
| **مسیر آسیب‌پذیر** | `/static/chat-logs/2.txt` (نمونه) |
| **متد** | `GET` |
| **پارامتر** | نام فایل در مسیر URL (`2.txt`، `1.txt`، ...) |
| **نیاز به احراز** | ❌ خیر — بدون احراز هم قابل دسترسیه |

---

## 🔍 مراحل reproducing

1. **ورود به اپلیکیشن** — آدرس لب رو باز می‌کنیم
2. **تشخیص فایل استاتیک** — می‌بینیم لاگ‌های چت در مسیرهای قابل پیش‌بینی مثل `/static/chat-logs/2.txt` ذخیره شدن
3. **دانلود فایل** — درخواست `GET /static/chat-logs/2.txt` → محتویات لاگ چت برمی‌گردونه
4. **دستکاری نام فایل** — در Burp Repeater، `2.txt` رو به `1.txt` تغییر میدیم
5. **نشست داده** — پاسخ شامل لاگ چت کاربر دیگه با داده‌های حساس (کردنشال، PII)
6. **استخراج کردنشال** — پسورد کاربر `carlos` در فایل `1.txt` پیدا شد
7. **اختصاص اکانت** — با کردنشال استخراج شده به عنوان `carlos` لاگین می‌کنیم → لب حل شد

**درخواست Burp Repeater:**
```http
GET /static/chat-logs/1.txt HTTP/1.1
Host: 0a1900350472af3c80748a930073000b.web-security-academy.net
```

---

## 🧠 ریشه آسیب‌پذیری (Root Cause)

| عامل | توضیح |
|--------|--------|
| **شناسه‌های قابل پیش‌بینی** | فایل‌ها به ترتیب نام‌گذاری شدن (`1.txt`، `2.txt`، `3.txt`...) |
| **عدم کنترل دسترسی** | هیچ چک authorization قبل از سرو فایل استاتیک |
| **بدون احراز هویت** | فایل‌ها بدون هیچ session/token قابل دسترس بودن |
| **داده حساس در فایل استاتیک** | لاگ چت شامل کردنشال در دایرکتوری وب قابل دسترسی |

اپلیکیشن داده‌های حساس کاربران (لاگ چت) رو در یک دایرکتوری استاتیک عمومی با **نام‌های متوالی قابل پیش‌بینی** و **بدون هیچ کنترل دسترسی** ذخیره کرده.

---

## 💥 تاثیر (Impact)

| CIA | تاثیر |
|-----|--------|
| **Confidentiality** | 🔴 **Critical** — افشای کامل مکالمات خصوصی، PII، کردنشال |
| **Integrity** | 🟡 Medium — امکان تزریق محتوای مخرب اگه write access داشته باشه |
| **Availability** | 🟢 Low — DoS مستقیم نه، ولی دزدی کردنشال باعث حملات بعدی میشه |

**تاثیر بزنس:**
- دزدی کردنشال → Übernahme اکانت (Carlos)
- افشای PII → نقض GDPR/حریم خصوصی
- نشت تاریخچه مکالمه → جاسوسی سازمانی، مهندسی اجتماعی
- **CVSS 4.0: 8.7 (High)** — `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N`

---

## 🛡️ رفع آسیب‌پذیری (Remediation)

### اصلاحات فوری

```python
# 1. حذف داده حساس از دایرکتوری‌های استاتیک وب
# لاگ‌های چت رو خارج از webroot یا در دیتابیس با ACL مناسب نگه دار

# 2. استفاده از شناسه‌های غیرقابل پیش‌بینی (UUIDs)
# /static/chat-logs/550e8400-e29b-41d4-a716-446655440000.txt

# 3. پیاده‌سازی میدل‌ور کنترل دسترسی
def serve_chat_log(request, file_id):
    user = get_current_user(request)
    log = get_chat_log(file_id)
    if log.user_id != user.id and not user.is_admin:
        return 403 Forbidden
    return serve_file(log.path)
```

### دفاع در عمق (Defense in Depth)

- ✅ فایل‌های حساس رو خارج از webroot ذخیره کن
- ✅ از UUID / نام‌های تصادفی رمزنگاری شده استفاده کن
- ✅ کنترل Authorization رو روی **هر** دسترسی فایل اعمال کن
- ✅ هدر `X-Content-Type-Options: nosniff` اضافه کن
- ✅ Rate limiting روی اندپوینت‌های فایل استاتیک بذار
- ✅ تمام دایرکتوری‌های استاتیک رو برای داده حساس audit کن

---

## ✅ چک‌لیست کیفیت

| چک | وضعیت |
|------|--------|
| مراحل قابل reproduce توسط غریبه | ✅ |
| اسکرین‌شات/مدراک ضمیمه شده | 📸 *اسکرین‌شات Burp اضافه کن* |
| تاثیر از نظر بزنس مرتبطه | ✅ |
| راهکار رفع قابل اجرا (actionable) | ✅ |
| انتشار در LinkedIn + X + GitHub | ⏳ در انتظار |

---

## 📚 رفرنس‌ها

- **CWE-639:** Authorization Bypass Through User-Controlled Key
- **CWE-200:** Exposure of Sensitive Information to an Unauthorized Actor
- **OWASP A01:2021** — Broken Access Control
- **PortSwigger:** [IDOR Vulnerability](https://portswigger.net/web-security/access-control/idor)

---

## 💡 نکات یادگرفته شده (Lessons Learned)

> **این لب یه الگوهای حیاتی رو یاد میده:** *هرگز فکر نکن "استاتیک" یعنی "امن".* هر فایلی که توسط وب‌سرور سرو میشه — عکس، PDF، لاگ، export — اگه حاوی داده کاربره باید کنترل دسترسی داشته باشه.

**تنوع‌های دنیای واقعی:** در فاکتور PDF (`/invoices/INV-2024-001.pdf`)، export CSV (`/exports/users-123.csv`)، سیستم‌های مدیریت سند، و کش پاسخ API دیده شده.

**نکته اتوماسیون:** یه اسکریپت ساده بنویس که IDهای متوالی روی هر دایرکتوری استاتیکی که در طول recon پیدا می‌کنی enumerate کنه.

---

## 🎯 کاندیدای بعدی برای رایت‌آپ

بعد از این، پیشنهاد می‌کنم:
1. **Referer-based access control** — بایپاس منطق، خیلی رایج در اپ‌های واقعی
2. **Method-based access control bypass** — دستکاری HTTP verb (GET vs POST vs PUT)
3. **User role modification in profile** — ارتقای امتیاز عمودی (Vertical Privilege Escalation)