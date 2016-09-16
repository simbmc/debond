'''
Created on 18.04.2016
@author: Yingxiong
'''
from kivy.garden.graph import Plot
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from math import log10


class FilledRect(Plot):

    '''
    draw a filled rectangular for given color and geometric parameters
    '''
    _image = ObjectProperty()
    xrange = ListProperty([0, 100])
    yrange = ListProperty([0, 100])
    color = ListProperty([255, 255, 255])

    def __init__(self, **kwargs):
        super(FilledRect, self).__init__(**kwargs)
        self.bind(
            color=self.ask_draw, xrange=self.ask_draw, yrange=self.ask_draw)

    def create_drawings(self):
        self._image = Rectangle(size=[0., 0.])
        return [self._image]

    def draw(self, *args):
        super(FilledRect, self).draw(*args)

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

if __name__ == '__main__':
    from kivy.uix.boxlayout import BoxLayout
    from kivy.app import App
    from kivy.garden.graph import Graph
    import random
    from kivy.clock import Clock

    class TestApp(App):

        def build(self):
            b = BoxLayout(orientation='vertical')

            graph2 = Graph(
                xlabel='x',
                ylabel='y',
                x_ticks_major=10,
                y_ticks_major=10,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                xmin=0,
                ymin=0)

            plot = FilledRect(color=[255, 255, 255])
            plot.xrange = [40, 70]
            plot.yrange = [30, 50]
            graph2.add_plot(plot)

            b.add_widget(graph2)
            self.rectangle = plot

            Clock.schedule_interval(self.update_color, 1)
            Clock.schedule_interval(self.update_pos, 1)

            return b

        def update_color(self, *args):
            self.rectangle.color = [random.randint(0, 255) for r in xrange(3)]

        def update_pos(self, *args):
            self.rectangle.xrange = [100. * random.random() for r in xrange(2)]
            self.rectangle.yrange = [100. * random.random() for r in xrange(2)]

    TestApp().run()