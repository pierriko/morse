import base64
from pymorse import Morse

with Morse() as sim:
    data = sim.r.v.get()

width = data['width']
height = data['height']
# data['image'] is RGBA base64 encoded
buff = base64.b64decode( data['image'] )

# Qt, use PyQt4, PySide or PyQt5
from PyQt4.QtGui import *

app = QApplication([])
label = QLabel()

# using PIL/ImageQt since Qt does not support RGBA image
# image = QImage(buff, width, height, QImage.Format_ARGB32)
from PIL import Image, ImageQt
image = Image.frombuffer('RGBA', (width, height), buff, 'raw', 'RGBA', 0, 1)

pixmap = QPixmap.fromImage( ImageQt.ImageQt(image) )
label.setPixmap(pixmap)
label.show()

app.exec_()
