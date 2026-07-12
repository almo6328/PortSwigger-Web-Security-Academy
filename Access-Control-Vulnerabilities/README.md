# Web Security Labs: Access Control & Privilege Escalation

This repository contains my practical solutions, automated tools, and write-ups for exploring **Access Control Vulnerabilities** during my offensive security journey.

## 🎯 Focus Areas
- **Horizontal Privilege Escalation:** Bypassing IDOR and access restrictions to access other users' data.
- **Vertical Privilege Escalation:** Escalating privileges from standard users to administrative roles via parameter tampering and URL manipulation.
- **Context-Dependent Access Control:** Exploiting flaws in business workflows where access state transitions are poorly validated.

## 🛠️ Automation & Tools
In the `/scripts` directory, you'll find a custom Python tool designed to automate parameter fuzzing for multi-layered access control testing, aiming to detect hidden administrative endpoints and parameter leaks.

## 📝 Key Takeaways
- Always enforce access control strictly on the **server-side**.
- Never trust client-controlled parameters (`id`, `role`, `isAdmin`) without proper session verification.
- Implement robust defense-in-depth measures, including structural URL protections and proper reverse proxy header configurations.
