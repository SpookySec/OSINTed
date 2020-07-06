#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "[-] Please run as root" 
   exit 1
fi
clear
echo "Installing now..."
sudo apt install whois
sudo apt install exiftool
pip3 install requests
pip3 install mac-vendor-lookup
pip3 install readline
pip3 install phonenumbers
pip3 install whois
pip3 install pyhibp
