from bottle import route, run, request
import sys
import guimovement as gm
from Crypto.Cipher import AES
from io import BytesIO

hostip = '192.168.2.100'
pwl = []
# legit pws
with open('entryfile', 'r', encoding='utf-8') as file:
    for line in file:
        pwl.append(line)


@route('/hello')
def hello():
    return "Hello World! I am alive."


@route('/mscontrol')
def answer():
    return "Something is missing!"


@route('/test/<name:re:[\w]+>')
def regrouting(name):
    return "Your name is :" + name


# THIS IS NOT SAFE; THIS IS FOR TESTING PURPOSE IN MY LOCAL NETWORK ONLY
@route('/mscontrol/<name:re:[\w]+>/<action:re:[ma]+x[0-9]+y[0-9]+>')
@route('/mscontrol/<name:re:[\w]+>/<action:re:[rlcs]>')
def mousecontrol(name, action):
    if name not in pwl:
        return "Name violation"
    if action != "r" or action != "l" or action != "c" or action != "s":
        command, position = action.split('x')
        width, height = position.split('y')
    print(command, width, height)
    if command == "c":
        sys.exit("Close via Command 'c'")
    elif command == "a":
        gm.moveAbsolute(int(width), int(height))
    elif command == "m":
        gm.moveRelative(int(width), int(height))
    elif command == "r":
        gm.click("right")
    elif command == "l":
        gm.click("left")
    elif command == "s":
        gm.showCursor()
        pass

    return command + " " + width + " " + height


@route('/secure', method="POST")
def secure():
    content = request.POST

    print("content")
    stream = []
    for i, con in enumerate(content):
        print(i, con)
        stream.append(con)
    print("stream:",stream[0])
    nonce, tag, ciphertext = [BytesIO(stream[0].encode()).read(x) for x in (16, 16, -1)]

    # let's assume that the key is somehow available again
    with open("key.bin", "rb") as i:
        key = i.read()
    print("key",str(key))
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    print("data", data)


run(host="192.168.2.100", port=8080, debug=True)
