#!/usr/bin/env python
"""
Basic Velocity command in WxPython (using keyboard arrows) over socket
http://stackoverflow.com/questions/5829148/message-reassembly-socket-communication
"""
import wx
import sys
import time
import json
import socket
import threading

VELOCITY_PORT=60000

class SocketClient(object):
    buffers = {}
    sockets = {}
    ports = {}
    host = "localhost"

    def __init__(self, **kwargs):
        self.ports.update(kwargs)
        if "host" in self.ports:
            self.host = self.ports.pop("host")
        for name in self.ports:
            self.sockets[name] = self._connect_port(self.ports[name])

    def _connect_port(self, port, retry=5):
        """ Establish the connection with the given MORSE port"""
        local_socket = None

        for res in socket.getaddrinfo(self.host, port,
                                      socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                local_socket = socket.socket(af, socktype, proto)
            except socket.error as msg:
                local_socket = None
                print("error socket port: %i; %s"%(port, msg))
                continue
            try:
                local_socket.connect(sa)
            except socket.error as msg:
                local_socket.close()
                local_socket = None
                print("error connect port: %i; %s"%(port, msg))
                continue

            if not local_socket and retry > 0:
                retry -= 1
                print("Retry (%i left) to connect to port %i"%(retry, port))
                time.sleep(.1)
            else:
                break

        return local_socket

    def read(self, id):
        got_message = False

        # reading loop
        while not got_message:
            data = self.sockets[id].recv(1024)
            if not data:
                break

            # add the current data read by the socket to a temporary buffer
            self.buffers[id] += data.decode('utf-8')

            # search complete messages
            messages = self.buffers[id].split('\n')

            # we need at least 2 messages to continue
            if len(messages) == 1:
                continue

            # seperator found, iterate across complete messages
            for message in messages [:-1]:
                # Prepare to exit the loop
                got_message = True

            # set the buffer with the last cutted message
            self.buffers[id] = messages [-1]

        decoded_message = json.loads(message)
        return (decoded_message)

    def send(self, **kwargs):
        try:
            for name in kwargs:
                data_out = (json.dumps((kwargs[name])) + '\n').encode()
                self.sockets[name].send(data_out)
        except AttributeError as e:
            print("error send: bad name: %s"%name)

class VWPublisher(threading.Thread):
    """ Velocity (v,w) Publisher """
    def __init__(self, port=None):
        threading.Thread.__init__(self)
        self.port = port if port else VELOCITY_PORT
        self._cmd_linear_released = False
        self._cmd_angular_released = False
        self._cmd = {"v": 0, "w": 0}
        self.cont = True
    def run(self):
        self.sc = SocketClient(velocity=self.port)
        def slowing(vel, coef=0.8, limit=0.01):
            return 0.0 if abs(vel) < limit else vel * coef
        while self.cont:
            self.sc.send(velocity=self._cmd)
            if self._cmd_linear_released:
                self._cmd['v'] = slowing(self._cmd['v'])
            if self._cmd_angular_released:
                self._cmd['w'] = slowing(self._cmd['w'])
            time.sleep(.1)

    def cmd_forward(self, released=False):
        self._cmd_linear_released = released
        self._cmd['v'] = 1 # forward
    def cmd_backward(self, released=False):
        self._cmd_linear_released = released
        self._cmd['v'] = -1 # backward
    def cmd_left(self, released=False):
        self._cmd_angular_released = released
        self._cmd['w'] = 1 # turn left
    def cmd_right(self, released=False):
        self._cmd_angular_released = released
        self._cmd['w'] = -1 # turn right
    def cmd_stop(self, unused=False):
        self._cmd['v'] = 0
        self._cmd['w'] = 0

class KeyEventFrame(wx.Frame):
    def __init__(self, port=None, parent=None, id=-1, title=__file__):
        wx.Frame.__init__(self, parent, id, title)
        self.map_key_function = {}
        self.panel = wx.Panel(self)

        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panel.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.panel.SetFocus()
        self.publisher = VWPublisher(port)
        self.KeyBinding()

        self.Centre()
        self.Show()
        self.publisher.start()

    def BindKey(self, key, function):
        self.map_key_function[key] = function

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode in self.map_key_function:
            self.map_key_function[keycode]()
        event.Skip()

    def OnKeyUp(self, event):
        key_code = event.GetKeyCode()
        if key_code in self.map_key_function:
            self.map_key_function[key_code](True)
        event.Skip()

    def KeyBinding(self):
        """ Bind keys to Twist command
        http://wxpython.org/docs/api/wx.KeyEvent-class.html
        """
        self.BindKey(ord('Z'), self.publisher.cmd_forward)
        self.BindKey(ord('S'), self.publisher.cmd_backward)
        self.BindKey(ord('Q'), self.publisher.cmd_left)
        self.BindKey(ord('D'), self.publisher.cmd_right)
        self.BindKey(wx.WXK_UP,    self.publisher.cmd_forward)
        self.BindKey(wx.WXK_DOWN,  self.publisher.cmd_backward)
        self.BindKey(wx.WXK_LEFT,  self.publisher.cmd_left)
        self.BindKey(wx.WXK_RIGHT, self.publisher.cmd_right)
        self.BindKey(wx.WXK_SPACE, self.publisher.cmd_stop)
        self.BindKey(wx.WXK_ESCAPE,self.quit)

    def quit(self, isKeyUp=False):
        self.publisher.cont = False
        self.Close()

def main(argv):
    port = int(argv[1]) if len(argv) > 1 else None
    app = wx.App()
    KeyEventFrame(port)
    print(__doc__)
    app.MainLoop()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
