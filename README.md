# PortSwigger Web Security Academy - Authentication Flaws

This repository contains my write-ups and technical notes as I progress through the PortSwigger Web Security Academy. 

## Lab: Username Enumeration via Timing Differences & IP Rate Limiting Bypass

### 📝 Vulnerability Description
The application's authentication mechanism is vulnerable to a **Timing Attack**. While checking credentials, the server takes longer to respond when a valid username is provided because it executes heavy cryptographic hashing functions (e.g., bcrypt) on the password. If the username is invalid, it rejects the request instantly. This minor difference in response times allows attackers to enumerate valid usernames. 

Additionally, the server implements IP-based rate limiting to prevent brute-force attacks, but it insecurely relies on HTTP headers to identify the client's IP address.

---

### 🛡️ Exploit Methodology

#### Step 1: Bypassing the WAF / Rate Limiter
Since the application blocks the IP after a few failed attempts, we can spoof our identity by injecting the `X-Forwarded-For` header into the HTTP request. 

#### Step 2: Pitchfork Attack vs Cluster Bomb
To effectively enumerate the usernames without getting blocked, a **Pitchfork Attack** in Burp Suite Intruder is used:
* **Payload 1:** A list of potential usernames.
* **Payload 2:** A list of unique IP addresses.

*Why not Cluster Bomb?* 
Using a `Cluster Bomb` attack would pair every single username with every single IP address, generating `(Usernames × IPs)` requests. This is highly inefficient for timing analysis and wastes massive network traffic since we only need to test each username once with a fresh IP. `Pitchfork` ensures a 1:1 mapping (User 1 with IP 1, User 2 with IP 2), preserving our IP pool and keeping the timing data clean.

#### Step 3: Analyzing Response Times
1. Fire the Pitchfork attack.
2. Sort the results by the **Response Received Time** column in Burp Suite.
3. The valid username will stand out significantly with a higher delay (e.g., several hundred milliseconds more than invalid ones).

#### Step 4: Brute-forcing the Password
Once the valid username is identified:
1. Set the username as static.
2. Use the **Pitchfork Attack** again to cycle through the password list while simultaneously rotating the `X-Forwarded-For` IPs to prevent lockdown.
3. A successful login will return a `302 Redirect` or a different response length.

---
*Disclaimer: This write-up is for educational and ethical hacking purposes only.*
