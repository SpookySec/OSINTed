#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "[-] Please run as root" 
   exit 1
fi
clear
echo "Installing now..."
sudo apt install whois
sudo apt install exiftool
python3 -m pip install requests
python3 -m pip install mac-vendor-lookup
python3 -m pip install readline
python3 -m pip install phonenumbers
python3 -m pip install whois
python3 -m pip install pyhibp
python3 -m pip install pyexifinfo
python3 -m pip install requests_futures
