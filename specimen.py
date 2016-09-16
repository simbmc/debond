'''
Created on 25.07.2016

@author: Yingxiong
'''
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from plot.filled_rect import FilledRect
from fem.tloop import TLoop
import numpy as np


class Specimen(BoxLayout):

    def __init__(self, **kwargs):
        super(Specimen, self).__init__(**kwargs)
        self.add_graph()
        self.max_displacement = 4.0
        self.tl = TLoop()
        self.x_current = 53.
        self.selected = False
        self.x_coord = np.linspace(0, self.tl.ts.L_x, self.tl.ts.n_e_x + 1)
        self.x_ip_coord = np.repeat(self.x_coord, 2)[1:-1]

    def add_graph(self):
        self.graph = Graph(
            x_ticks_major=10., y_ticks_major=10.,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=100, ymin=0, ymax=30)
        self.matrix = FilledRect(xrange=[10, 50],
                                 yrange=[5, 25],
                                 color=[255, 255, 255])
        self.reinf = FilledRect(xrange=[10, 50],
                                yrange=[13, 17],
                                color=[255, 0, 0])
        self.controller = FilledRect(xrange=[50, 56],
                                     yrange=[12, 18],
                                     color=[0, 0, 255])
        self.graph.add_plot(self.matrix)
        self.graph.add_plot(self.reinf)
        self.graph.add_plot(self.controller)
        self.add_widget(self.graph)

    @property
    def f_u_wid(self):
        graph = Graph(xlabel='displacement', ylabel='force', x_ticks_minor=5,
                      x_ticks_major=1, y_ticks_major=100,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0, xmax=self.max_displacement, ymin=-100, ymax=500)
        self.f_u_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.f_u_line.points = [(0, 0)]
        graph.add_plot(self.f_u_line)
        return graph

    @property
    def eps_sig_wid(self):
        graph = Graph(xlabel='slip', ylabel='bond', x_ticks_minor=5,
                      x_ticks_major=0.5, y_ticks_major=0.2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0.0 * self.max_displacement, xmax=0.8 * self.max_displacement, ymin=-1, ymax=1)
        self.eps_sig_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.eps_sig_line.points = [(0, 0)]
        graph.add_plot(self.eps_sig_line)
        return graph

    @property
    def shear_flow_wid(self):
        graph = Graph(xlabel='length', ylabel='shear flow', background_color=[0, 0, 0, 1],
                      x_ticks_major=100., y_ticks_major=0.2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0.0, xmax=self.tl.ts.L_x, ymin=-1, ymax=1)
        self.shear_flow_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.shear_flow_line.points = self.list_tuple(
            self.x_coord, np.zeros_like(self.x_coord))
        graph.add_plot(self.shear_flow_line)
        return graph

    @property
    def disp_slip_wid(self):
        graph = Graph(xlabel='length', ylabel='displacement',  background_color=[0, 0, 0, 1],
                      x_ticks_major=100., y_ticks_major=1.0,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0.0, xmax=self.tl.ts.L_x, ymin=0., ymax=self.max_displacement)
        self.reinf_disp_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.reinf_disp_line.points = self.list_tuple(
            self.x_coord, np.zeros_like(self.x_coord))
        self.matrix_disp_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.matrix_disp_line.points = self.list_tuple(
            self.x_coord, np.zeros_like(self.x_coord))
        self.slip_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.slip_line.points = self.list_tuple(
            self.x_coord, np.zeros_like(self.x_coord))
        graph.add_plot(self.reinf_disp_line)
        graph.add_plot(self.matrix_disp_line)
        graph.add_plot(self.slip_line)
        return graph

    @staticmethod
    def list_tuple(xdata, ydata):
        '''convert the x and y data for line plot'''
        return list(map(tuple, np.vstack((xdata, ydata)).T))

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lower-left
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.graph.xmax
        y = (touch.y - y0) / gh * self.graph.ymax
        # to check is the controller is selected
        x0, x1 = self.controller.xrange
        y0, y1 = self.controller.yrange
        if (x >= x0) * (x <= x1) * (y >= y0) * (y <= y1):
            self.selected = True

    def on_touch_up(self, touch):
        self.selected = False

    def on_touch_move(self, touch):
        if self.selected:
            x0, y0 = self.graph._plot_area.pos  # position of the lower-left
            gw, gh = self.graph._plot_area.size  # graph size
            x = (touch.x - x0) / gw * self.graph.xmax
            # make sure the controller doesn't enter the matrix
            x = max(x, 53.)
            x = min(x, 93.)
            if abs(x - self.x_current) >= 2:
                d_u = (x - self.x_current) * self.max_displacement / 40.
                self.tl.get_p(d_u)
                self.x_current = x
#                 print self.tl.U_record[-1]
#                 print self.tl.F_record[-1]
                self.f_u_line.points.append(
                    (self.tl.U_record[-1], self.tl.F_record[-1]))
                self.eps_sig_line.points.append(
                    (self.tl.eps_record[-1], self.tl.sig_record[-1]))

                U = np.reshape(self.tl.U, (-1, 2)).T
                self.matrix_disp_line.points = self.list_tuple(
                    self.x_coord, U[0])
                self.reinf_disp_line.points = self.list_tuple(
                    self.x_coord, U[1])
                self.slip_line.points = self.list_tuple(
                    self.x_coord, U[1] - U[0])

                shear_flow = self.tl.sig[:, :, 1].flatten()
                self.shear_flow_line.points = self.list_tuple(
                    self.x_ip_coord, shear_flow)

            self.controller.xrange = [x - 3., x + 3.]
            self.reinf.xrange = [x - 43., x - 3.]


if __name__ == '__main__':

    from kivy.app import App
    from kivy.core.window import Window
    Window.size = (1280, 216)

    class MainWindow(App):

        def build(self):
            return Specimen()

    MainWindow().run()
