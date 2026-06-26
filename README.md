# PortSwigger Web Security Academy - Labs & Automation 🚀

Welcome to my security research repository. This project serves as a structured archive of my methodologies, labs walkthroughs, and custom Python automation scripts developed while solving challenges in the PortSwigger Web Security Academy.

Rather than relying purely on default automated tools (like Burp Intruder), my primary focus is understanding core application logic and building programmatic exploits.

---

## 📂 Repository Structure & Modules

Every core security module contains its own dedicated directory, isolation of custom scripts, and a localized detailed write-up.

### 🔐 1. [Authentication Vulnerabilities](./Authentication-Vulnerabilities/)
Flaws and logical errors within authentication schemes, session management, and multi-factor mechanisms.
* **Sub-Module:** [Password-Based Login Vulnerabilities](./Authentication-Vulnerabilities/Password-Based-Login/) `[Completed]` - Information disclosure via timing, flawed business logic bypasses, and account lockout enumeration.
* **Sub-Module:** [Multi-Factor Authentication (MFA) Vulnerabilities]
* **Lab 1:** 2FA Bypass via Broken Verification Logic | (./Authentication -vulnerabilities/Multi-factor-Authentication/readme.md)
* **Lab 2:** 2FA Bypass via Parameter Tampering & Python Automation (No Rate Limiting) | [View Writeup](./Authentication -vulnerabilities/Multi-factor-Authentication/readme.md)



---

## 🛠️ Tech Stack & Tooling
* **Languages:** Python 3.x (Bespoke exploit automation)
* **Tools:** Burp Suite Professional (Intruder, Repeater, Grep-Extract, Logger)
* **Environment:** Linux / Advanced VPS Environments
