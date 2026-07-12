# Vulnerabilities in Other Authentication Mechanisms - PortSwigger Labs Walkthrough

## Overview
In this write-up, I break down the core logic behind bypassing flawed authentication mechanisms, focusing on tracking flaws in password reset tokens, vulnerable password change functionalities, and insecure "Remember Me" cookie implementations based on 5 challenges from PortSwigger Web Security Academy.

## Key Flaws Analyzed

### 1. Insecure Password Reset Logic
* **The Vulnerability:** Applications often generate predictable reset tokens or fail to properly bind the token to the specific user requesting the change. Another high-risk vector is Host Header Injection, where a manipulated `Host` or `X-Forwarded-Host` header forces the server to send the reset link to an attacker-controlled domain.
* **Exploitation Strategy:** Analyze token entropy (uniqueness), test for predictability, and verify if a token generated for User A can be reused to reset User B's password.

### 2. Authentication Bypass in Password Changing
* **The Vulnerability:** Broken Access Control (IDOR) disguised as a password change form. When the backend relies on user-supplied parameters (like `username=victim` or `user_id=102`) inside the POST request body rather than identifying the user via their active session cookie.
* **Exploitation Strategy:** Intercept the `POST` request, modify the target username/ID, and attempt to strip the `current_password` parameter to see if the server bypasses current password validation.

### 3. Exploiting Broken "Remember Me" Cookies
* **The Vulnerability:** Relying on weak cryptography or simple encodings (like Base64) to handle persistent login states. Often, these cookies expose a structure like `username:hash`.
* **Exploitation Strategy:** Decode the cookie, identify the hash type (e.g., MD5/SHA-1), crack it using tools like `Hashcat` or custom Python automation, and craft a forged cookie for administrative users.
