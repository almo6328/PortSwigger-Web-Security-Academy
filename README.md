# PortSwigger Web Security Academy - Authentication Vulnerabilities

This section documents my technical methodologies, custom Python automation scripts, and strategic approaches focused on exploiting and analyzing Authentication mechanisms. 

---

## 🔐 ۱. Vulnerabilities in Password-Based Login (Completed)

This module explores fundamental and logical flaws within standard username/password authentication implementations, with a strong focus on bypassing rate limits, abusing application logic, and data exfiltration.

### 📊 Lab Metrics & Methodology Summary

| Lab Name | Core Vulnerability | Exploitation Strategy & Automation |
| :--- | :--- | :--- |
| **Username Enumeration via Timing Differences** | Information Disclosure / Timing Attack | Analyzed subtle delays in server response times to identify valid usernames versus non-existent accounts. |
| **Flawed Logic in Authentication Protection** | IP-Based Rate Limiting Bypass via State Reset | Engineered a custom Python script that automated a brute-force attack by alternating states: attempting ۲ invalid credentials followed by ۱ valid login to programmatically reset the server-side failure counter. |
| **Username Enumeration via Account Lockout** | Information Disclosure via Defensive State Triggering | **Phase ۱:** Developed a Python script to iterate through usernames, testing a password ۵ times per user to detect the distinct account lockout error. <br>**Phase ۲:** Leveraged Burp Suite Intruder (Sniper) equipped with `Grep - Extract` to capture the correct password without triggering further lockout blocks. |

---

## 🔑 ۲. Vulnerabilities in Multi-Factor Authentication (MFA) - [In Progress]

*Currently researching and developing exploit vectors for MFA bypasses, session fixation, and flaws in two-factor administrative logic.*
