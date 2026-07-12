# Multi-Factor Authentication (MFA) Vulnerabilities

This repository contains writeups and technical walkthroughs for bypassing Multi-Factor Authentication (MFA) mechanisms based on PortSwigger Web Security Academy labs.

---

## 🛠️ Lab 1: 2FA Bypass via Broken Verification Logic

### 🎯 Objective
Exploit a business logic flaw in the server-side verification process to completely bypass the 2FA requirement.

### 🔍 Walkthrough
1. **Analysis:** Logged in with valid credentials and analyzed the 2FA submission behavior. The application relied on a URL query string (e.g., `?username=my-account`) to determine which user was verifying the code, without strictly validating the session ownership in the background.
2. **Exploitation:** Logged in using the victim's primary credentials. At the 2FA verification step, tampered with the URL parameter by replacing my username with the victim's username. 
3. **Result:** The server forced the login process to complete for the target user without requiring the actual 2FA token. Account successfully compromised.

---

## 🛠️ Lab 2: 2FA Authentication Bypass via Parameter Tampering & Python Automation

### 🎯 Objective
Bypass 2FA by manipulating request headers to target a specific user and automating a 4-digit token brute-force attack due to a total lack of Rate Limiting.

### 🔍 Walkthrough
1. **Initial Access:** Conducted a successful brute-force attack against the victim's primary password to pass the first login phase.
2. **Parameter Tampering:** Analyzed the 2FA verification POST request and identified a custom tracking header (e.g., `verify: wiener`) determining the target session. Modified this header value to the victim's username.
3. **Automation Strategy:** Since a 4-digit code creates $10,000$ possible combinations and Burp Suite Community Edition is throttled, I shifted to a custom Python automation script.
4. **Exploitation:** Verified that the endpoint had **no Rate Limiting or IP blocking** mechanisms. The Python script generated tokens from `0000` to `9999` and concurrently sent high-speed POST requests with the tampered header.
5. **Result:** The correct 2FA token was extracted rapidly, bypassing the multi-factor security layer entirely.

### 🛡️ Remediation & Security Best Practices
* **State Management:** Maintain the MFA state strictly within secure, server-side session variables. Never rely on user-controllable input (such as headers or URL parameters) to identify the session state.
* **Rate Limiting:** Implement aggressive rate limiting, account lockout policies, or CAPTCHA challenges on all authentication and 2FA verification endpoints to block automated brute-force attacks.

