'''
Created on 06.10.2016

@author: Yingxiong
'''
from kivy.garden.graph import Graph
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from numpad import Numpad
from kivy.uix.label import Label
from kivy.uix.button import Button
import numpy as np


class ResizeGraph(Graph):

    def __init__(self, **kwargs):
        super(ResizeGraph, self).__init__(**kwargs)
        self.numpad = Numpad()
        self.numpad.p = self
        self.editNumpad = Popup(content=self.numpad)
        self.create_buttons()
        self.create_panel()
        self.x_min = self.xmin
        self.x_max = self.xmax
        self.y_min = self.ymin
        self.y_max = self.ymax

    n_x_ticks = NumericProperty(5.)
    n_y_ticks = NumericProperty(5.)

    x_min = NumericProperty(0.)
    x_max = NumericProperty(100.)
    y_min = NumericProperty(0.)
    y_max = NumericProperty(100.)

    def on_x_min(self, instance, value):
        self.xmin = self.x_min
        a = (self.x_max - self.x_min) / self.n_x_ticks
        self.x_ticks_major = round(a, -int(np.log10(a)) + 1)
        self.x_l.text = str(self.x_min)

    def on_x_max(self, instance, value):
        self.xmax = self.x_max
        a = (self.x_max - self.x_min) / self.n_x_ticks
        self.x_ticks_major = round(a, -int(np.log10(a)) + 1)
        self.x_u.text = str(self.x_max)

    def on_y_min(self, instance, value):
        self.ymin = self.y_min
        a = (self.y_max - self.y_min) / self.n_y_ticks
        self.y_ticks_major = round(a, -int(np.log10(a)) + 1)
        self.y_l.text = str(self.y_min)

    def on_y_max(self, instance, value):
        self.ymax = self.y_max
        a = (self.y_max - self.y_min) / self.n_y_ticks
        self.y_ticks_major = round(a, -int(np.log10(a)) + 1)
        self.y_u.text = str(self.y_max)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if touch.is_double_tap:
                self.limit_pop.open()

    def create_buttons(self):
        # x lower limit
        self.x_l = Button()
        self.x_l.btn_name = 'x lower limit'
        self.x_l.bind(on_press=self.show_numpad)

        # x upper limit
        self.x_u = Button()
        self.x_u.btn_name = 'x upper limit'
        self.x_u.bind(on_press=self.show_numpad)

        # y lower limit
        self.y_l = Button()
        self.y_l.btn_name = 'y lower limit'
        self.y_l.bind(on_press=self.show_numpad)

        # y upper limit
        self.y_u = Button()
        self.y_u.btn_name = 'y upper limit'
        self.y_u.bind(on_press=self.show_numpad)

        # ok and cancel
        self.ok = Button(text='OK')
        self.ok.bind(on_press=self.confirm_settings)
        self.cancel = Button(text='Cancel')
        self.cancel.bind(on_press=self.cancel_settings)

        self.x_l.text = str(self.x_min)
        self.x_u.text = str(self.x_max)
        self.y_l.text = str(self.y_min)
        self.y_u.text = str(self.y_max)

    def create_panel(self):
        panel = GridLayout(cols=2)

        panel.add_widget(Label(text='x lower limit'))
        panel.add_widget(self.x_l)
        panel.add_widget(Label(text='x upper limit'))
        panel.add_widget(self.x_u)
        panel.add_widget(Label(text='y lower limit'))
        panel.add_widget(self.y_l)
        panel.add_widget(Label(text='y upper limit'))
        panel.add_widget(self.y_u)
        panel.add_widget(self.ok)
        panel.add_widget(self.cancel)

        self.limit_pop = Popup(title='change the axis-limits',
                               content=panel,
                               size_hint=(0.5, 0.8))

    def show_numpad(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = btn.text
        self.editNumpad.title = btn.btn_name
        self.editNumpad.open()

    def cancel_settings(self, btn):
        '''resume the values shown on the buttons'''
        self.x_l.text = str(self.x_min)
        self.x_u.text = str(self.x_max)
        self.y_l.text = str(self.y_min)
        self.y_u.text = str(self.y_max)
        self.limit_pop.dismiss()

    def confirm_settings(self, btn):
        self.x_min = float(self.x_l.text)
        self.x_max = float(self.x_u.text)
        self.y_min = float(self.y_l.text)
        self.y_max = float(self.y_u.text)
        self.limit_pop.dismiss()

    def close_numpad(self):
        self.editNumpad.dismiss()

    def finished_numpad(self):
        self.focusBtn.text = str(float(self.numpad.lblTextinput.text))
        self.editNumpad.dismiss()


if __name__ == '__main__':
    from kivy.garden.graph import Graph, MeshLinePlot
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.slider import Slider
    from kivy.uix.scatter import Scatter

    class Main(App):

        def build(self):
            root = BoxLayout(orientation='vertical')
    #         root = Scatter()
            self.graph = ResizeGraph(
                y_grid_label=True, x_grid_label=True, padding=5,
                xmin=-11, xmax=100, ymin=0, ymax=30, x_ticks_major=20, y_ticks_major=5)
            self.graph1 = ResizeGraph(
                y_grid_label=True, x_grid_label=True, padding=5,
                xmin=0, xmax=100, ymin=0, ymax=30, x_ticks_major=20.456,
                y_ticks_major=5)

            line = MeshLinePlot(points=[(0, 0), (200, 30)])
            self.graph.add_plot(line)
            s = Slider(min=0, max=100, value=30)
            s.bind(value=self.set_ymax)
            root.add_widget(self.graph)
            root.add_widget(self.graph1)
    #         root.add_widget(s)
            root.on_touch_down = self.on_touch_down
            return root

        def set_ymax(self, instance, value):
            self.graph.ymax = value

        def on_touch_down(self, touch):
            print 'global'

    Main().run()
