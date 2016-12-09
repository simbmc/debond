'''
Created on 13.10.2016

@author: Yingxiong
'''
from plot.resize_graph import ResizeGraph
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from numpad import Numpad
from kivy.uix.popup import Popup
from plot.line import LinePlot
from plot.filled_ellipse import FilledEllipse
from kivy.properties import ListProperty
import numpy as np


class MultilinearEditor(BoxLayout):

    n_points = NumericProperty(5.)
    points = ListProperty(
        [(0, 0), (0.2, 0.15), (0.4, 0.3), (0.6, 0.45), (0.8, 0.6), (1.0, 0.75)])

    def on_n_points(self, instance, value):
        x = np.linspace(self.graph.x_min, self.graph.x_max, self.n_points)
        y = np.linspace(self.graph.y_min, self.graph.y_max, self.n_points)
        self.points = [tuple([i, j]) for i, j in zip(x, y)]
        self.line.points = self.points
        self.draw_points()

    def __init__(self,  **kwargs):
        super(MultilinearEditor, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        # list to record the ellipse representing the points
        self.points_figure_lst = []
        self.create_graph()
        self.numpad = Numpad()
        self.numpad.p = self
        self.editNumpad = Popup(content=self.numpad)
        self.create_panel()
        self.selected = None  # the selected point
        self.check_input = Popup(title='pleas check input value',
                                 content=Label(
                                     text='The damage function should be a monotonic \nfunction with function values in [0, 1]'),
                                 size_hint=(0.5, 0.4))

    def create_graph(self):
        self.graph = ResizeGraph(y_grid_label=True, x_grid_label=True, padding=5,
                                 xmin=0, xmax=1, ymin=0, ymax=1,
                                 n_x_ticks=5, n_y_ticks=5,
                                 xlabel='gamma', ylabel='damage factor')
        self.graph.bind(x_max=self.draw_points)
        self.graph.bind(x_min=self.draw_points)
        self.graph.bind(y_max=self.draw_points)
        self.graph.bind(y_min=self.draw_points)
        self.line = LinePlot()
        self.line.points = self.points
        self.graph.add_plot(self.line)
        self.draw_points()
        self.add_widget(self.graph)
        self.graph.on_touch_down = self.graph_touch_down
        self.graph.on_touch_move = self.graph_touch_move

    def draw_points(self, instance=None, value=None):
        for p in self.points_figure_lst:
            self.graph.remove_plot(p)
        self.points_figure_lst = []
        self.rx = (self.graph.xmax - self.graph.xmin) / 80.
        self.ry = (self.graph.ymax - self.graph.ymin) / 80.
        for point in self.points:
            p = FilledEllipse(xrange=[point[0] - self.rx, point[0] + self.rx],
                              yrange=[point[1] - self.ry, point[1] + self.ry])
            self.points_figure_lst.append(p)
            self.graph.add_plot(p)

    def create_panel(self):
        self.panel = GridLayout(cols=2)

        self.panel.add_widget(Label(text='number of points'))
        self.n_p_button = Button()
        self.n_p_button.btn_name = 'number of points'
        self.n_p_button.bind(on_press=self.show_numpad)
        self.n_p_button.text = '5'
        self.panel.add_widget(self.n_p_button)

        self.panel.add_widget(Label(text='x coordinate'))
        self.x_button = Button()
        self.x_button.btn_name = 'x coordinate'
        self.x_button.bind(on_press=self.show_numpad)
        self.panel.add_widget(self.x_button)

        self.panel.add_widget(Label(text='y coordinate'))
        self.y_button = Button()
        self.y_button.btn_name = 'y coordinate'
        self.y_button.bind(on_press=self.show_numpad)
        self.panel.add_widget(self.y_button)

        self.ok_button = Button(text='OK')
        self.cancel_button = Button(text='Cancel')

        self.panel.add_widget(self.ok_button)
        self.panel.add_widget(self.cancel_button)

        # place holder
        self.panel.add_widget(Label(size_hint=(1, 3)))

        self.add_widget(self.panel)

    def show_numpad(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = btn.text
        self.editNumpad.title = btn.btn_name
        self.editNumpad.open()

    def close_numpad(self):
        self.editNumpad.dismiss()

    def finished_numpad(self):
        #         self.focusBtn.text = str(float(self.numpad.lblTextinput.text))
        if self.focusBtn == self.n_p_button:
            self.focusBtn.text = str(int(self.numpad.lblTextinput.text))
            self.n_points = int(self.numpad.lblTextinput.text)

        if self.focusBtn == self.x_button:
            if self.selected:

                x = float(self.numpad.lblTextinput.text)
                # the damage function should be a monotonic function

                # the last point is selected
                if self.selected == len(self.points) - 1:
                    if x < self.points[self.selected - 1][0]:
                        self.editNumpad.dismiss()
                        self.check_input.open()
                        return
                elif x < self.points[self.selected - 1][0] or x > self.points[self.selected + 1][0]:
                    self.editNumpad.dismiss()
                    self.check_input.open()
                    return
                self.focusBtn.text = str(x)
                self.points_figure_lst[self.selected].xrange = [
                    x - self.rx, x + self.rx]
                self.points[self.selected] = (x, float(self.y_button.text))
                self.line.points = self.points

        if self.focusBtn == self.y_button:
            if self.selected:
                y = float(self.numpad.lblTextinput.text)
                # make sure that the damage function is a monotonic function

                # the last point is selected
                if self.selected == len(self.points) - 1:
                    if y < self.points[self.selected - 1][1] or y > 1:
                        self.editNumpad.dismiss()
                        self.check_input.open()
                        return

                elif y < self.points[self.selected - 1][1] or y > self.points[self.selected + 1][1]:
                    self.editNumpad.dismiss()
                    self.check_input.open()
                    return
                self.focusBtn.text = str(y)
                self.points_figure_lst[self.selected].yrange = [
                    y - self.ry, y + self.ry]
                self.points[self.selected] = (float(self.x_button.text), y)
                self.line.points = self.points

        self.editNumpad.dismiss()

    def set_n_points(self, btn):
        self.n_points = int(btn.text)

    def convert_to_graph_coord(self, x_g, y_g):
        '''convert the global coord to the graph coord'''
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        x0 += self.pos[0]
        y0 += self.pos[1]
        gw, gh = self.graph._plot_area.size  # graph size
        x = (x_g - x0) / gw * \
            (self.graph.xmax - self.graph.xmin) + self.graph.xmin
        y = (y_g - y0) / gh * \
            (self.graph.ymax - self.graph.ymin) + self.graph.ymin
        return x, y

    def graph_touch_down(self, touch):

        if touch.is_double_tap:
            if self.graph.collide_point(touch.x, touch.y):
                self.graph.limit_pop.open()

        t_factor = 4  # tolerence for selecting the points with finger
        rx = t_factor * self.rx
        ry = t_factor * self.ry

        x, y = self.convert_to_graph_coord(touch.x, touch.y)

        for i, point in enumerate(self.points):
            # check if the point is selected
            if (abs(x - point[0]) < rx) * (abs(y - point[1]) < ry) == True:
                if i <> 0:  # the first point is not movable
                    # make the previous selected points to white (if any)
                    if self.selected:
                        self.points_figure_lst[
                            self.selected].color = [255, 255, 255]
                    self.selected = i
                    self.points_figure_lst[i].color = [255, 0, 0]
                    self.x_button.text = str(self.points[self.selected][0])
                    self.y_button.text = str(self.points[self.selected][1])

    def graph_touch_move(self, touch):
        if self.selected:
            if self.graph.collide_point(touch.x, touch.y):
                x, y = self.convert_to_graph_coord(touch.x, touch.y)
                # to make sure the function is a monotonic function
                if self.selected == len(self.points) - 1:
                    x = max(x, self.points[self.selected - 1][0])
                    y = max(y, self.points[self.selected - 1][1])
                    y = min(y, 1)
                else:
                    x = max(x, self.points[self.selected - 1][0])
                    x = min(x, self.points[self.selected + 1][0])
                    y = max(y, self.points[self.selected - 1][1])
                    y = min(y, self.points[self.selected + 1][1])

                self.points_figure_lst[self.selected].xrange = [
                    x - self.rx, x + self.rx]
                self.points_figure_lst[self.selected].yrange = [
                    y - self.ry, y + self.ry]
                self.line.points[self.selected] = (x, y)
                self.points[self.selected] = (x, y)
                self.x_button.text = str(round(x, 5))
                self.y_button.text = str(round(y, 5))


if __name__ == '__main__':

    from kivy.app import App

    class MainWindow(App):

        def build(self):
            return MultilinearEditor()

    MainWindow().run()
