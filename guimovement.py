import pyautogui

pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True
_width, _height = pyautogui.size()

#moves the mouse to an absoloute position
def moveAbsolute(x,y):
    posX = min(x, _width)
    posY = min(y, _height)
    pyautogui.moveTo(posX, posY, duration=0.5)

def moveRelative(x, y):
    posX = min(x, _width)
    posY = min(y, _height)
    pyautogui.moveRel(posX, posY, duration=0.5)

def showCursor():
    x, y = pyautogui.position()
    pyautogui.alert(text='The Cursor is here: {},{}'.format(x,y), title='Position!', button='OK' )

def click(button='left'):
    if button == 'left':
        pyautogui.click()
    elif button == 'right':
        pyautogui.rightclick()