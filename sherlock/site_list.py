"""Sherlock: Supported Site Listing
This module generates the listing of supported sites.
"""
import json
import sys
import requests
white = '\033[97m'
green = '\033[92m'
red = '\033[91m'
yellow = '\033[93m'
end = '\033[0m'
info = '\033[93m[!] \033[0m'
que = '\033[94m[?] \033[0m'
bad = '\033[91m[-] \033[0m'
good = '\033[32m[+] \033[0m'
run = '\033[97m[~] \033[0m'

def SherlockUpdate():
    pool = list()

    with open("sherlock/sherlock/resources/data.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)


    with open("sites.md", "w") as site_file:
        data_length = len(data)
        site_file.write(f'## List Of Supported Sites ({data_length} Sites In Total!)\n')

        for social_network in data:
            url_main = data.get(social_network).get("urlMain")
            data.get(social_network)["rank"] = 0
            th = None
            pool.append((social_network, url_main, th))

        index = 1
        for social_network, url_main, th in pool:
            site_file.write(f'{index}. [{social_network}]({url_main})\n')
            sys.stdout.write("\r{0}".format(good + white + "Updated " + yellow + f"{index} " + white + "out of " + yellow + f"{data_length} " + white + "entries" + end))
            sys.stdout.flush()
            index = index + 1
    print()
    sorted_json_data = json.dumps(data, indent=2, sort_keys=True)

    with open("sherlock/sherlock/resources/data.json", "w") as data_file:
        data_file.write(sorted_json_data)

    print(good + white + "Finished updating supported site listing!")