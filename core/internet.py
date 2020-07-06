import requests
def CheckInternet():
    try:
        requests.get("https://google.com")
        return True
    except:
        return False