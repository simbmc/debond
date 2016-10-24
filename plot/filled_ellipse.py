'''
Created on 18.04.2016

@author: Yingxiong
'''
from kivy.garden.graph import Plot
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Ellipse
from kivy.graphics.texture import Texture
from math import log10


class FilledEllipse(Plot):

    '''
    draw a filled ellipse for given color and geometric parameters
    '''
    
    _image = ObjectProperty()
    xrange = ListProperty([0, 100])
    yrange = ListProperty([0, 100])
    color = ListProperty([255, 255, 255])

    def __init__(self, **kwargs):
        super(FilledEllipse, self).__init__(**kwargs)
        self.bind(
            color=self.ask_draw, xrange=self.ask_draw, yrange=self.ask_draw)
        
    def create_drawings(self):
        self._image = Ellipse(size=[0., 0.])
        return [self._image]

    def draw(self, *args):
        super(FilledEllipse, self).draw(*args)

        self._texture = Texture.create(size=(1, 1), colorfmt='rgb')
        self._texture.blit_buffer(
            b''.join(map(chr, self.color)), colorfmt='rgb', bufferfmt='ubyte')
        image = self._image
        image.texture = self._texture

        params = self._params
        funcx = log10 if params['xlog'] else lambda x: x
        funcy = log10 if params['ylog'] else lambda x: x
        xmin = funcx(params['xmin'])
        ymin = funcy(params['ymin'])
        size = params['size']
        ratiox = (size[2] - size[0]) / float(funcx(params['xmax']) - xmin)
        ratioy = (size[3] - size[1]) / float(funcy(params['ymax']) - ymin)
        bl = (funcx(self.xrange[0]) - xmin) * ratiox + \
            size[0], (funcy(self.yrange[0]) - ymin) * ratioy + size[1]
        tr = (funcx(self.xrange[1]) - xmin) * ratiox + \
            size[0], (funcy(self.yrange[1]) - ymin) * ratioy + size[1]
        image.pos = bl
        w = tr[0] - bl[0]
        h = tr[1] - bl[1]
        image.size = (w, h)
