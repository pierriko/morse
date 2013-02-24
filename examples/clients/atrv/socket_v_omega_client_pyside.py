#!/usr/bin/env python3

import time
import struct
import threading

try:
    from PySide import QtCore, QtGui
except ImportError:
    print("sudo apt-get install python3-pyside")
    import sys; sys.exit(1)

import pymorse

class CameraDisplay(QtGui.QLabel):
    stream = QtCore.Signal(QtGui.QImage)
    def __init__(self):
        super(CameraDisplay, self).__init__()
        self.stream.connect(self._update)
    @QtCore.Slot(QtGui.QImage)
    def _update(self, image):
        self.setPixmap(QtGui.QPixmap.fromImage(image))

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # image viewer
        self.imageLabel = CameraDisplay()
        self.setCentralWidget(self.imageLabel)
        self.setWindowTitle("morse socket camera")
        self.resize(200, 200)
        self.show()
        #self.videoStream = VideoStream()
        #self.videoStream.onImage = self.updateImage
        #self.videoStream.start()
        # motion publisher thread and key bindings
        self.publisher = VWPublisher()
        self.publisher.onImage = self.updateImage # TMP
        self.bindings()
        self.publisher.start()
    def updateImage(self, width, height, data):
        flatten = []
        for px in data:
            flatten.extend((px['a'], px['r'], px['g'], px['b']))
        # ARGB json str to packed bytes buff (slow) just for demo!
        data32 = struct.pack('%iB'%len(data)*4, *flatten)
        image = QtGui.QImage(data32, width, height, QtGui.QImage.Format_ARGB32)
        self.imageLabel.stream.emit(image)
    def bindings(self):
        self._key_bindings = {}
        self.bind(QtCore.Qt.Key_Escape, self.close)
        self.bind(QtCore.Qt.Key_Up,     self.publisher.move_forward)
        self.bind(QtCore.Qt.Key_Down,   self.publisher.move_backward)
        self.bind(QtCore.Qt.Key_Left,   self.publisher.move_left)
        self.bind(QtCore.Qt.Key_Right,  self.publisher.move_right)
        self.bind(QtCore.Qt.Key_Space,  self.publisher.move_stop)
    def bind(self, key_code, function):
        self._key_bindings.setdefault(key_code, []).append(function)
    def keyReleaseEvent(self, event):
        for function in self._key_bindings.get(event.key(), []):
            function(released=True)
    def keyPressEvent(self, event):
        for function in self._key_bindings.get(event.key(), []):
            function(released=False)
    def close(self, released):
        if released:
            self.publisher.stop()
            QtGui.QMainWindow.close(self)
    def mousePressEvent(self, event):
        print("clickseEvent " + str(event)) # TODO save /image ?


class VWPublisher(threading.Thread):
    """ Velocity (v,w) Publisher """
    def __init__(self):
        threading.Thread.__init__(self)
        self._cmd_linear_released = False
        self._cmd_angular_released = False
        self._cmd = {"v": 0, "w": 0}
        self.alive = True
    def stop(self, timeout=.5):
        # "kill" and wait `timeout` seconds
        self.alive = False
        self.join(timeout)
    def run(self):
        def slowing(vel, coef=0.8, limit=0.01):
            return 0.0 if abs(vel) < limit else vel * coef
        with pymorse.Morse() as sim:
            motion = sim.robot.motion
            camera = sim.robot.camera
            while self.alive:
                motion.publish(self._cmd)
                if self._cmd_linear_released:
                    self._cmd['v'] = slowing(self._cmd['v'])
                if self._cmd_angular_released:
                    self._cmd['w'] = slowing(self._cmd['w'])
                image = camera.last()
                if image and len(image.keys()) > 2:
                    self.onImage(image['width'], image['height'], image['image'])
                else:
                    time.sleep(.1)

    def move_forward(self, released=False):
        self._cmd_linear_released = released
        self._cmd['v'] = 1 # forward
    def move_backward(self, released=False):
        self._cmd_linear_released = released
        self._cmd['v'] = -1 # backward
    def move_left(self, released=False):
        self._cmd_angular_released = released
        self._cmd['w'] = 1 # turn left
    def move_right(self, released=False):
        self._cmd_angular_released = released
        self._cmd['w'] = -1 # turn right
    def move_stop(self, released):
        self._cmd['v'] = 0
        self._cmd['w'] = 0


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())

