import pyautogui as pgi
import time
def stop_play():
    pgi.press('space')
def seek_fwd():
    pgi.press('right')
def seek_bkwd():
    pgi.press('left')
def vol_up():
    pgi.press('up')
def vol_down():
    pgi.press('down')
def exit():
    pgi.hotkey('ctrl','q')

def initAction(cnt):
    if cnt==1:
        stop_play()
    elif cnt==2:
        vol_down()
    elif cnt==3:
        vol_up()
    elif cnt==4:
        pass
