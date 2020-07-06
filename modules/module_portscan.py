import requests

def PortScan(host):
    req = requests.get(f"https://api.hackertarget.com/nmap/?q={host}")
    return req.text