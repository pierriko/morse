import base64
from pymorse import Morse

with Morse() as sim:
    data = sim.r.v.get()

width = data['width']
height = data['height']
# data['image'] is RGBA base64 encoded
buff = base64.b64decode( data['image'] )

buff_rgb = [[r,g,b] for r,g,b in zip(buff[0::4], buff[1::4], buff[2::4])]

def ppm_ascii(image, width, height):
    #assert(len(image) == width * height * 3)
    yield 'P3\n%i %i\n255\n'%(width, height)
    for r,g,b in image:
        yield '%i %i %i'%(r,g,b)

with open('image.ppm', 'w') as f:
    for txt in ppm_ascii(buff_rgb, width, height):
        f.write( txt )
