import os
import sys 
import readline
import glob

commands = ["phoneinfo", "sherlockupdate",
"whois", "ipinfo", 
"nslookup", "imagesearch", 
"maclookup", "passwordcheck", 
"portscan", "sherlock",
"metadata", "instainfo", 
"help", "clear", 
"exit", "banner", 
"update", "whoami"]


def completer(text, state):
    """
    complete commands from the list above
    """
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def pathCompleter(text,state):
    """ 
    This is the tab completer for systems paths.
    """
    if '~' in text:
        text = os.path.expanduser('~')
    if os.path.isdir(text):
        text += '/'
    return [x for x in glob.glob(text + '*')][state]

readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")

def PathComplete():
    readline.set_completer(pathCompleter)

def CommandComplete():
    readline.set_completer(completer)

def HistoryClear():
    readline.clear_history()