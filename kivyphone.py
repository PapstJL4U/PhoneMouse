#-*-coding:utf8;-*-
#qpy:2
#qpy:kivy
#Don't autoformat! It puts whitespaces into the above comments, which are used as guidelines for qpython.

import kivy
kivy.require('1.0.6')
from glob import glob
from Crypto.Cipher import AES
from tempfile import TemporaryFile
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest
import urllib

"""
# FIXME this shouldn't be necessary
from kivy.core.window import Window"""
_ip = '192.168.2.100'
_port = '8080'
_key = None
_protocol = "http://"
with open("key.bin", "rb") as i:
    _key = i.read()


class TouchWidget(Widget):
    _start = None
    _end = None

    def encrypt(self, msg):
        cipher = AES.new(_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(msg, 'utf-8'))
        file_out = TemporaryFile(mode='w+b')
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.seek(0)
        return file_out.read()

    def command(self, touch, click):
        width, height = touch.pos
        # result should be something like "ax2111y450", a single letter followed by xwidthyheight
        result = click + 'x' + str(int(width)) + 'y' + str(int(height))
        result = self.encrypt(result)
        return result

    def on_touch_down(self, touch):
        print("td", touch.pos)
        _start = touch.pos
        msg = self.command(touch, "a")
        self.sendMouse(msg)

    def on_touch_move(self, touch):
        print("tm", touch.pos)

    def on_touch_up(self, touch):
        print("tu", touch.pos)
        _end = touch.pos
        msg = self.command(touch, "l")
        self.sendMouse(msg)

    def sendMouse(self, command):
        url = _protocol + _ip + ":" + _port + "/secure"
        print(url)
        header = {'Content-Type': 'application/octet-stream'}
        res = UrlRequest(url=url, req_body={'command',command}, req_headers=header,method="POST")
        print(res)

class MouseApp(App):

    def build(self):
        # the root is created in mouse.kv
        root = self.root
        self.title = "This is my mouse now ;_;"
        root.add_widget(TouchWidget())

    def on_pause(self):
        return True


if __name__ == '__main__':
    MouseApp().run()
