# PortSwigger Web Security Academy 🚀

This repository contains my personal write-ups, custom Python automation scripts, and methodologies developed while solving labs in the PortSwigger Web Security Academy.

---

## 🔐 Authentication Vulnerabilities

### 📑 1. Vulnerabilities in Password-Based Login (Completed)
This section covers flaws discovered in standard username/password authentication mechanisms, focusing on logic flaws, rate-limiting bypasses, and information disclosure.

* **Lab 1: Username Enumeration via Timing Differences**
    * *Methodology:* [توضیحات یا کدهایی که قبلاً برای این لب نوشتی رو اینجا قرار بده]
* **Lab 2: Flawed Logic in Authentication Protection**
    * *Methodology:* Exploited a rate-limit reset flaw where a successful login cleared the failed attempts counter.
    * *Automation:* Custom Python script alternating between 2 failed attempts and 1 successful login.
* **Lab 3: Username Enumeration via Account Lockout**
    * *Methodology:* Enumerated valid users by triggering a 5-attempt account lockout state, followed by an Intruder Sniper attack using Grep-Extract.

---

### 🔑 2. Vulnerabilities in Multi-Factor Authentication (MFA) - [In Progress]
*(Next topic to be documented...)*
