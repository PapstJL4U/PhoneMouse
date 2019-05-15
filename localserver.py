from bottle import route, run, request, FormsDict
import sys
import guimovement as gm
from Crypto.Cipher import AES
from io import BytesIO

hostip = '192.168.2.100'

@route('/hello')
def hello():
    return "Hello World! I am alive."


@route('/test/<name:re:[\w]+>')
def regrouting(name):
    return "Your name is :" + name


# THIS IS NOT SAFE; THIS IS FOR TESTING PURPOSE IN MY LOCAL NETWORK ONLY
@route('/mscontrol/<name:re:[\w]+>/<action:re:[ma]+x[0-9]+y[0-9]+>')
@route('/mscontrol/<name:re:[\w]+>/<action:re:[rlcs]>')
def mousecontrol(name, action):
    return "Old method - no use"

def parsecommands(action):

    if action.startswith("m") or action.startswith("a"):
        command, position = action.split('x')
        width, height = position.split('y')
    else:
        command = action

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



@route('/secure', method="POST")
def secure():
    content = request.POST
    stream = []
    for i, con in enumerate(content):
        stream.append(con)
        # print(i, i+1, stream[0].encode(encoding="latin1"))

    incoming = BytesIO(bytearray(stream[0], encoding="latin1"))
    nonce, tag, ciphertext = [incoming.read(x) for x in (16, 16, -1)]

    # let's assume that the key is somehow available again
    with open("key.bin", "rb") as i:
        key = i.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    #data = cipher.decrypt_and_verify(ciphertext, tag)
    print("data", data.decode(encoding="utf-8"))
    parsecommands(data.decode(encoding="utf-8"))

@route('/unsecure', method="POST")
def unsecure():
    content = request.POST
    stream = []
    for i, con in enumerate(content):
        stream.append(con)

    parsecommands(stream[0])

run(host="192.168.2.100", port=8080, debug=True)
