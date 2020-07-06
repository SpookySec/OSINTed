import requests
import json
class Ip:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def getInfo(self):
        """
        Send a request to the api and get the info
        """
        request = json.loads(requests.get(f"http://ip-api.com/json/{self.ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,currency,isp,org,mobile,proxy,hosting").text)
        self.status = request["status"]
        self.continent = request["continent"]
        self.continentCode = request["continentCode"]
        self.country = request["country"]
        self.countryCode = request["countryCode"]
        self.region = request["region"]
        self.regionName = request["regionName"]
        self.city = request["city"]
        self.zipCode = str(request["zip"])
        self.lat = str(request["lat"])
        self.lon = str(request["lon"])
        self.timezone = request["timezone"]
        self.currency = request["currency"]
        self.isp = request["isp"]
        self.mobile = str(request["mobile"])
        self.proxy = str(request["proxy"])
        self.hosting = str(request["hosting"])
    def isValid(self):
        """
        Checks if the ip is valid or not
        """
        request = json.loads(requests.get(f"http://ip-api.com/json/{self.ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,currency,isp,org,mobile,proxy,hosting").text)
        self.status = request["status"]
        if self.status != "success":
            self.message = request["message"]
            return False
        else:
            return True 