"""
Myszka (Polish for 'mouse') monitors the user's idle time and, if it exceeds a predefined threshold 
(IDLE_THRESHOLD), simulates key presses and mouse movements to prevent inactivity triggers 
(such as screen lock).

Usage:
- The IDLE_THRESHOLD variable defines the idle time threshold in seconds.
- The script runs continuously until manually stopped (using Ctrl+C).

Dependencies:
- Python modules: pyautogui, ctypes, time.
- Works only on Windows (due to the use of the ctypes module).
"""

import pyautogui
import time
import ctypes

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

IDLE_THRESHOLD = 30
KEY_PRESS_INTERVAL = 30
last_key_press_time = 0

try:
    while True:
        idle_time = get_idle_time()

        if idle_time >= IDLE_THRESHOLD:
            current_time = time.time()
            if current_time - last_key_press_time >= KEY_PRESS_INTERVAL:
                pyautogui.keyDown('ctrl')
                pyautogui.keyUp('ctrl')
                last_key_press_time = current_time
            
            pyautogui.moveRel(-100, 0, duration=0.2)
            time.sleep(1)
            pyautogui.moveRel(100, 0, duration=0.2)
            time.sleep(1)
            pyautogui.moveRel(0, -100, duration=0.2)
            time.sleep(1)
            pyautogui.moveRel(0, 100, duration=0.2)
            time.sleep(60)
        else:
            time.sleep(1)
except KeyboardInterrupt:
    pass
