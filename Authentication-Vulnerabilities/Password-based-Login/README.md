# Password-Based Login Vulnerabilities 🔑

This sub-module documents my practical research into logical flaws, defensive implementation bypasses, and state-handling issues found within standard username/password authentication forms.

---

## 📑 Completed Labs Walkthroughs & Methodologies

### 1. Username Enumeration via Timing Differences
* **Core Flaw:** The application exhibited a subtle variation in server response times depending on whether the queried username existed in the database.
* **Exploitation:** Analyzed the `Response Received` timestamp metrics in Burp Suite to differentiate valid accounts from non-existent profiles via measurable crypto/processing delays.

### 2. Flawed Logic in Authentication Protection
* **Core Flaw:** IP-based rate limiting blocked requests after **3** invalid attempts, but a successful authentication sequence completely reset the global failure counter on the server side.
* **Automation Approach:** Developed a Python script (`/scripts/flawed_logic_bypass.py`) that acts as a state-alternator. It automates a brute-force sequence sending **2** invalid credentials to the target, followed by **1** valid login attempt with my own credentials to continuously wipe the IP block counter.

### 3. Username Enumeration via Account Lockout
* **Core Flaw:** The application locked valid accounts after **5** failed login attempts, changing its error message behavior compared to unverified users.
* **Exploitation Workflow:**
  * **Phase 1 (Python Automation):** Wrote `/scripts/account_lockout_enum.py` to target the username list, executing exactly 5 invalid attempts per user until a strict "Account is locked" flag was triggered, successfully isolating the valid victim username.
  * **Phase 2 (Burp Intruder):** Configured a Sniper attack over the isolated user account. Utilized `Grep - Extract` to monitor response changes; when the correct password was targeted, the server omitted the lockout warning, allowing identification of the correct payload.

---

## 📌 Defensive Remediation Summary
* **Generic Error Handling:** Authentication systems should always return a generic error string (e.g., *Invalid username or password*) to prevent user enumeration.
* **Time Response Padding:** Implement artificial delay padding to make response times mathematically uniform, mitigating timing analysis.
* **Robust Counter Scoping:** Rate-limiting counters must be tied strictly to a persistent session or IP infrastructure and shouldn't be flushable via unrelated successful authentication states.
