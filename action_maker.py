import pyautogui as pgi
import time
def stop_play():
    pgi.press('space')
def seek_fwd():
    pgi.hotkey('ctrl','right') #pgi.press('right') for windows vlc media player
def seek_bkwd():
    pgi.hotkey('ctrl','left') #pgi.press('left') for windows vlc media player
def vol_up():
    pgi.hotkey('ctrl','up') #pgi.press('up') for linux vlc media player
def vol_down():
    pgi.hotkey('ctrl','down') #pgi.press('down') for linux vlc media player
def exit():
    pgi.hotkey('ctrl','q')

def initAction(cnt):
    if cnt==1:
        stop_play()
    elif cnt==20:
        vol_down()
    elif cnt==30:
        vol_up()
    elif cnt == 40:
        seek_fwd()
    elif cnt == 50:
        seek_bkwd()
    elif cnt==4:
        pass
