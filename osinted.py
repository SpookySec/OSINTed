#!/usr/bin/python3
import os
import time
import webbrowser
import requests
import socket
import sys
from mac_vendor_lookup import InvalidMacError
from core.auto_complete import PathComplete, CommandComplete, HistoryClear, commands
from core.color import *
from modules.module_phone import PhoneNumber
from modules.module_whois import Domain
from modules.module_ip import Ip
from modules.module_image import ReverseSearchImage
from modules.module_mac import GetVendor
from modules.module_passbreach import CheckPassword
from modules.module_portscan import PortScan
from modules.module_instagram import Instagram
from modules.module_metadata import ImageJPG, GetType
from urllib.error import HTTPError
from sherlock.site_list import SherlockUpdate
from sherlock.sherlock.sherlock import UserSearch
from core.banner import banner
from core.internet import CheckInternet
from core.update import CheckUpdate, NewStuff, Update
from core.help import HelpMenu

print(info + white + "Checking for internet connection..." + end)
if CheckInternet():
    print(good + green + "You're connected!" + end)
else:
    print(bad + red + "You're not connected!" + end)
    exit()
time.sleep(0.3)
os.system("clear")
print(banner)
while True:
    try:
        CommandComplete()
        cmd = input(yellow + "OSINTed> " + end)
        if cmd != "":

            # META DATA
            if cmd.split()[0] == "metadata":
                argv = cmd.split()
                if len(argv) != 1:
                    print(info + yellow + "Usage: " + green + f"{argv[0]}")
                else:
                    PathComplete()
                    img = input(run + white + f"Path to file (use{green} Tab{white}): " + end)
                    try:
                        fileType = GetType(img)
                        print(run + white + "Analyzing file...")
                        if fileType == "jpg" or fileType == "jpeg":
                            image = ImageJPG(img)
                            print(good + white + "JFIF Version: " + yellow + image.GetJFIFVersion())
                            print(good + white + "MIME Type: " + yellow + image.GetMime())
                            print(good + white + "Image Height: " + yellow + image.GetHeight())
                            print(good + white + "Image Width: " + yellow + image.GetWidth())
                            print(good + white + "Image Size: " + yellow + image.GetImageSize())
                            print(good + white + "X Resolution: " + yellow + image.GetXRes())
                            print(good + white + "Y Resolution: " + yellow + image.GetYRes())
                            print(good + white + "Resolution Unit: " + yellow + image.GetResUnit())
                            print(good + white + "File Size: " + yellow + image.GetFileSize())
                            print(good + white + "File Permissions: " + yellow + image.GetPerms())
                            try:
                                print(good + white + "Exif Byte Order: " + yellow + image.GetByteOrder())
                            except:
                                pass
                            try:
                                print(good + white + "Oreientation: " + yellow + image.GetOrientation())
                            except:
                                pass
                        else:
                            print(bad + red + "Sorry, only supports JPG files currently!")
                            print(bad + red + "Current file type: " + white + GetType(img))            
                    except ValueError:
                        print(bad + red + "File not found!" + end)
                    except Exception as error:
                        print(bad + red + "An unknown error as occurred...")
                        print(bad + red + "Error: " + white + error)
                HistoryClear()
                CommandComplete()

            # INSTAGRAM OSINT
            if cmd.split()[0] == "instainfo":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <instagram username>")
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "instagram")
                else:
                    try:
                        username = Instagram(argv[1])
                        if username.isValid():
                            print(good + white + "User: " + yellow + argv[1] + white + " exists!" + end)
                            print(run + white + "Getting information now..." + end)
                            time.sleep(2)
                            print(good + white + "Username: " + yellow + username.username())
                            print(good + white + "User ID: " + yellow + username.user_id())
                            print(good + white + "FullName: " + yellow + username.fullname())
                            print(good + white + "Followers: " + yellow + username.followers())
                            print(good + white + "Following: " + yellow + username.following())
                            print(good + white + "Posts: " + yellow + username.posts())
                            print(good + white + "Url: " + yellow + username.url())
                            print(good + white + "Is verified: " + yellow + username.verified())
                            print(good + white + "Is private: " + yellow + username.private())
                            print(good + white + "Is a business account: " + yellow + str(username.business()))
                            if username.business():
                                print(good + white + "Business category: " + yellow + username.business_category())
                            print(good + white + "HD Profile picture: \n" + yellow + username.profile_pic())
                            
                            print(good + white + "Biography: \n" + yellow + username.bio())
                        else:
                            print(bad + red + "Username: " + yellow + argv[1] + red + " not found!")
                        
                    except:
                        print(bad + red + "An unknown error has occurred!" + end)
                        
            
            # USER LOOKUP
            if cmd.split()[0] == "sherlock":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <username>")
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "username123")
                else:
                    username = argv[1]
                    UserSearch(username)

            # PORT SCAN
            if cmd.split()[0] == "portscan":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <host>")
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "scanme.nmap.org")
                else:
                    host = argv[1]
                    scan = PortScan(host)
                    if "error" in scan:
                        print(bad + red + "An error has occurred!" + end)
                        print(info + red + "Host format: " + yellow + "scanme.nmap.org" + end)
                    else:
                        print(run + white + "Scanning " + yellow + f"{host}\n" + end)
                        print(scan)

            # PASSWORD BREACH 
            if cmd.split()[0] == "passwordcheck":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <password>")
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "password123")
                else:
                    print(run + white + "Checking for password...")
                    password = CheckPassword(argv[1])
                    time.sleep(1)
                    if password:
                        print(info + white + "Password has been used " + yellow + str(password) + white + " times!" + end)
                    else:
                        print(good + white + "You're good!" + end)
            
            # MAC ADDRESS LOOKUP
            if cmd.split()[0] == "maclookup":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <MAC Address>")
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "11:22:33:44:55:66")
                else:
                    try:
                        vendor = GetVendor(argv[1])
                        print(run + white + "Vendor: " + end + vendor)
                    except KeyError:
                        print(bad + red + "MAC address not found!")
                    except InvalidMacError:
                        print(bad + red + "MAC address doesn't seem legit...")
                    
            # IMAGE REVERSE SEARCH
            if cmd.split()[0] == "imagesearch":
                try:
                    argv = cmd.split()
                    if len(argv) != 1:
                        print(info + yellow + "Usage: " + green + f"{argv[0]}" + end)
                    else:
                        PathComplete()
                        img = input(good + white + f"Enter the path to the picture (use {green}Tab{end}): " + end)
                        ext = img.split(".")[-1]
                        if ext == "jpg" or ext == "png" or ext == "jpeg" or ext == "gif" or ext == "bmp" or ext == "tif" or ext == "webp":
                            try:
                                Url = ReverseSearchImage(img)
                                while True:
                                    ask = input(que + white + "Would you like to open the result in browser [" + green + "Y" + white + "/" + red + "N" + white + "]: " + end)
                                    if ask.upper() == "Y":
                                        webbrowser.open_new(Url)
                                        break
                                    elif ask.upper() == "N":
                                        print(info + white + "Link: " + end + Url)
                                        break
                                    else:
                                        pass
                            except:
                                print(bad + red + "An error has occurred!" + end)
                        else:
                            print(bad + red + "Unsupported format!" + end)
                            print(info + white + "Supported formats: " + yellow + "jpg, png, jpeg, gif, bmp, tif, webp")
                        HistoryClear()
                        CommandComplete()
                except KeyboardInterrupt:
                    pass
            
            # IP INFO
            if cmd.split()[0] == "ipinfo":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <ip address>" + end)
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "8.8.8.8")
                else:
                    ip_address = Ip(argv[1])
                    if not ip_address.isValid():
                        print(bad + red + "IP Doesn't seem to be valid!" + end)
                        print(bad + red + "API message: " + white + ip_address.message + end)
                    else:
                        ip_address.getInfo()
                        print(run + white + "Continent: " + end + ip_address.continent)
                        print(run + white + "ContinentCode: " + end + ip_address.continentCode)
                        print(run + white + "Country: " + end + ip_address.country)
                        print(run + white + "CountryCode: " + end + ip_address.countryCode)
                        print(run + white + "Region Name: " + end + ip_address.regionName)
                        print(run + white + "Region: " + end + ip_address.region)
                        print(run + white + "City: " + end + ip_address.city)
                        print(run + white + "ZipCode: " + end + ip_address.zipCode)
                        print(run + white + "Latitude: " + end + ip_address.lat)
                        print(run + white + "Longitude: " + end + ip_address.lon)
                        print(run + white + "TimeZone: " + end + ip_address.timezone)
                        print(run + white + "Currency: " + end + ip_address.currency)
                        print(run + white + "ISP: " + end + ip_address.isp)
                        print(run + white + "Mobile: " + end + ip_address.mobile)
                        print(run + white + "Proxy: " + end + ip_address.proxy)
                        print(run + white + "Hosting Serivce: " + end + ip_address.hosting)

            # WHO IS
            if cmd.split()[0] == "whois":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <domain>" + end)
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "www.google.com")
                else:
                    try:
                        domain = Domain(argv[1])
                        print(run + white + "Domain Owner: " + end + domain.owner)
                        print(run + white + "Creation Date: " + end + domain.creation)
                        print(run + white + "Expiration Date: " + end + domain.experation)
                        print(run + white + "Last Update: " + end + domain.update)
                        print(run + white + "Name Servers: " + end)
                        for server in domain.name_servers:
                            print(f"\t- {server}\n", end="")
                    except:
                        print(bad + red + "Domain doesn't seem to be valid!" + end)
            
            # NS LOOKUP
            if cmd.split()[0] == "nslookup":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <domain>" + end)
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "www.google.com")
                else:
                    domain = argv[1]

                    ip_list = []
                    ais = socket.getaddrinfo(domain ,0,0,0,0)
                    for result in ais:
                        ip_list.append(result[-1][0])
                    ip_list = list(set(ip_list))
                    for ip in ip_list:
                        print(good + white + "Found: " + yellow + ip + end)


            # PHONE NUMBER
            if cmd.split()[0] == "phoneinfo":
                argv = cmd.split()
                if len(argv) != 2:
                    print(info + yellow + "Usage: " + green + f"{argv[0]} <global format phone number>" + end)
                    print(good + white + "Example: " + green + f"{argv[0]} " + yellow + "+11234567890")
                else:
                    try:
                        number = PhoneNumber(argv[1])
                        if number.carrier == "" and number.country == "":
                            print(bad + red + "Number doesn't seem to be valid!" + end)
                        else:
                            print(good + green + "Getting info..." + end)
                            time.sleep(1)
                            print(run + white + "Carrier: " + end + number.carrier)
                            print(run + white + "Country: " + end + number.country)
                            print(run + white + "Local Format: " + end + number.localNumber)
                            print(run + white + "International Format: " + end + number.internationalNumber)
                    except:
                        print(bad + red + "Number doesn't seem to be valid!" + end)
            

            # WHO AM I
            if cmd.split()[0] == "whoami":
                print(good + white + "Made by " + yellow + "@spooky_sec" + end)

            # BANNER
            if cmd.split()[0] == "banner":
                print(banner)
            
            # CLEAN
            if cmd.split()[0] == "clear":
                os.system("clear")
            
            # HELP
            if cmd.split()[0] == "help":
                print(HelpMenu)
            
            # UPDATE
            if cmd.split()[0] == "update":
                print(run + white + "Checking for updates..." + end)
                if CheckUpdate("https://raw.githubusercontent.com/SpookySec/OSINTed/master/core/updates.py"):
                    print(good + white + "There's an update!" + end)
                    new_stuff = NewStuff("https://raw.githubusercontent.com/SpookySec/OSINTed/master/core/updates.py")
                    print(info + white + "New stuff: " + end)
                    for thing in new_stuff:
                        print(yellow + f"\t- {thing}\n", end="")
                    while True:
                        option = input(que + white + "Would you like to install the update [" + 
                        green + "Y" + white + "/" + red + "N" + white + "]: ")
                        if option.upper() == "Y":
                            print(info + white + "Updating..." + end)
                            time.sleep(2)
                            input(info + white + "Spam Enter to finish: ")
                            Update()
                            print(good + white + "Done!" + end)
                            print(info + white + "Exiting..." + end)
                            sys.exit(0)
                            break
                        elif option.upper() == "N":
                            print(bad + white + "Too bad :(")
                            break
                        else:
                            pass
                else:
                    print(good + white + "You're up to date" + end)

            # SHERLOCK UPDATE
            if cmd.split()[0] == "sherlockupdate":
                print(info + white + "Updating Sherlock..." + end)
                time.sleep(1)
                SherlockUpdate()


            # EXIT
            if cmd.split()[0] == "exit":
                print(good + white + "GoodBye! :)" + end)
                break
            
            # COMMAND NOT FOUND
            if cmd.split()[0] not in commands:
                print(bad + red + "Use \"" + green + "help" + red + "\" to list available commands" + end)
    except KeyboardInterrupt:
        print("\n" + bad + red + "Use \"" + green + "exit" + red + "\" to exit" + end)
        pass