#qpy:kivy

import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest
"""
# FIXME this shouldn't be necessary
from kivy.core.window import Window"""
_ip = '192.169.0.3'
pwl = []
with open('entryfile', 'r', encoding='utf-8') as file:
    for line in file:
        pwl.append(line)

_code = pwl[0]
_port = '8080'
class TouchWidget(Widget):

    _start = None
    _end = None

    def command(self, touch, click):
        width, height = touch.pos
        #result should be something like "ax2111y450", a single letter followed by xwidthyheight
        result = click+'x'+str(int(width))+'y'+str(int(height))
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
        url = _ip+':'+_port+'/mscontrol/'+_code+'/'+command
        body = None
        print(url)
        req = UrlRequest(url, req_body=body)

class MouseApp(App):

    def build(self):

        # the root is created in mouse.kv
        root = self.root
        self.title="This is my mouse now ;_;"
        root.add_widget(TouchWidget())

    def on_pause(self):
        return True

if __name__ == '__main__':
    MouseApp().run()

