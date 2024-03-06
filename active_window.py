import psutil;
import ctypes;
from ctypes import wintypes;
import time, datetime, os;

from discordrp import Presence;

#get client_id here https://discord.com/developers/applications
client_id = '000000000000000000' # replace this with client_id from top url

with Presence(client_id) as presence:
    _presence = { # https://discord.com/developers/applications/client_id/rich-presence/assets
        "state": 'BIG TEXT',
        "details": 'SMALL TEXT',
        "assets": {
            "large_image": "ACTIVITY_IMAGE",
            "large_text": "ACTIVITY_TEXT",
        }    
    }
    presence.set(_presence)

    while True:

        pid = wintypes.DWORD()
        active = ctypes.windll.user32.GetForegroundWindow()
        active_window = ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
        length = ctypes.windll.user32.GetWindowTextLengthW(active);
        buf = ctypes.create_unicode_buffer(length + 1);
        ctypes.windll.user32.GetWindowTextW(active, buf, length + 1)

        pid = pid.value

        for item in psutil.process_iter():
            if pid == item.pid:
                name_aw = item.name()
                proc_title = buf.value;

                # if name_aw == "#proccess.exe"
                #     _presence["details"] = 'blah blah blah'
                #     _presence["state"] = proc_title

                if name_aw == "Telegram.exe":
                    _presence["details"] = 'typing to my mommy uwu'
                    _presence["state"] = proc_title
                else:
                    _presence["details"] = 'i love mommy'
                    _presence["state"] = 'mommy is god oWo'

                presence.set(_presence)
        time.sleep(5)