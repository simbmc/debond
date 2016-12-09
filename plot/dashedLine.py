'''
Created on 27.06.2016

@author: mkennert
'''
from kivy.graphics import Line, RenderContext
from kivy.metrics import dp

from kivy.garden.graph import Plot, Color, Mesh


class DashedLine(Plot):
    
    '''
    draw a dashed-line by the given color
    '''
    
    def __init__(self, **kwargs):
        super(DashedLine, self).__init__(**kwargs)
    
    def create_drawings(self):
        self._mesh = Mesh(mode='lines')
        self._grc = RenderContext(
                use_parent_modelview=True,
                use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(points=[], width=1, dash_offset=dp(15), dash_length=dp(15))
        return [self._grc]
    
    def draw(self, *args):
        super(DashedLine, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        with self._grc:
            self._gcolor = Color(*self.color)
        self._gline.points = points
