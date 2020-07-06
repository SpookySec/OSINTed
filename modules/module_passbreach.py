import pyhibp
from pyhibp import pwnedpasswords as pw
pyhibp.set_user_agent(ua="OSINTed/1.0 (OSINT FrameWork @spooky_sec)")

def CheckPassword(password):
    handle = pw.is_password_breached(password=f"{password}")
    return handle