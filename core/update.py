import os
import re
import sys
from requests import get    
from core.updates import updates


def CheckUpdate(source):
    latestCommit = get(source).text
    if updates not in latestCommit:
        return True
    else:
        return False

def NewStuff(source):
    latestCommit = get(source).text
    changelog = re.search(r"updates = \"(.*?)\"", latestCommit)
    changelog = changelog.group(1).split(":")
    return changelog

def Update():
    currentPath = os.getcwd().split("/")
    folder = currentPath[-1]
    path = "/".join(currentPath)
    os.system(f"git clone --quiet https://github.com/SpookySec/OSINTed {folder}")
    os.system(f"cp -r {path}/{folder}/* {path} && rm -r {path}/{folder}/ 2>/dev/null")