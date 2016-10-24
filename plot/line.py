'''
Created on 26.04.2016

@author: mkennert
'''
from kivy.graphics import RenderContext
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty
from kivy.garden.graph import Plot, Color, Mesh


class LinePlot(Plot):

    '''
    draw a line by the given color and thickness
    '''
    width = NumericProperty(1.)

    def __init__(self, **kwargs):
        super(LinePlot, self).__init__(**kwargs)
        self.bind(width=self.ask_draw)

    def create_drawings(self):
        self._mesh = Mesh(mode='lines')
        self._grc = RenderContext(
            use_parent_modelview=True,
            use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(points=[], width=self.width)
        return [self._grc]

    def draw(self, *args):
        super(LinePlot, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        with self._grc:
            self._gcolor = Color(*self.color)
        self._gline.points = points

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

            plot = LinePlot(color=[255, 255, 255], width=100.)
            plot.points = [(10, 10), (90, 90)]
            graph2.add_plot(plot)

            b.add_widget(graph2)

            return b

    TestApp().run()
