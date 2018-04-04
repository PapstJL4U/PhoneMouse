from bottle import route, run
import sys
import guimovement as gm
hostip='192.168.0.3'
pwl = []
#legit pws
with open('entryfile', 'r', encoding='utf-8') as file:
    for line in file:
        pwl.append(line)

@route('/hello')
def hello():
    return "Hello World! I am alive."

@route('/mscontrol')
def answer():
    return "Something is missing!"

#THIS IS NOT SAFE; THIS IS FOR TESTING PURPOSE IN MY LOCAL NETWORK ONLY
@route('/mscontrol/<name:re:[\w]+>/<action:re:[rlmacs]+x[0-9]+y[0-9]+>')
def mousecontrol(name, action):
    if name not in pwl:
        return
    command, position = action.split('x')
    width, height = position.split('y')
    print(command, width, height)
    if command == "c":
        sys.exit("Close via Command 'c'")
    elif command == "a":
        gm.moveAbsolute(int(width), int(height))
    elif command == "m":
        gm.moveRelative(int((width), int(height)))
    elif command == "r":
        gm.click("right")
    elif command == "l":
        gm.click("left")
    elif command == "s":
        #gm.showCursor()
        pass

run(host='localhost', port=8080, debug=True)
