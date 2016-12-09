'''
Created on 24.10.2016

@author: Yingxiong
'''
from multilinear_editor import MultilinearEditor
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from plot.resize_graph import ResizeGraph
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from fem.matseval import MATSEval
from plot.line import LinePlot
from plot.dashedLine import DashedLine
import numpy as np
from numpad import Numpad


class BondEditor(BoxLayout):

    def __init__(self, **kwargs):
        super(BondEditor, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.mats = MATSEval()
        self.create_pop()
        self.create_graph()
        self.create_panel()
        self.numpad = Numpad()
        self.numpad.p = self
        self.editNumpad = Popup(content=self.numpad)

    def create_pop(self):
        self.multilinear = MultilinearEditor()
        self.damage_pop = Popup(content=self.multilinear,
                                title='damage law editor')
        self.multilinear.ok_button.bind(on_press=self.multilinear_ok)
        self.multilinear.cancel_button.bind(on_press=self.multilinear_cancel)

    def multilinear_ok(self, btn):
        self.damage_pop.dismiss()
        coord = np.array(self.multilinear.points).T
        self.mats.f_damage_x = coord[0]
        self.mats.f_damage_y = coord[1]
        self.update_graph()

    def multilinear_cancel(self, btn):
        self.damage_pop.dismiss()
        # resume the points
        self.multilinear.n_points = len(self.mats.f_damage_x)
        self.multilinear.points = self.list_tuple(
            self.mats.f_damage_x, self.mats.f_damage_y)
        self.multilinear.draw_points()
        self.multilinear.line.points = self.multilinear.points

    def create_graph(self):
        slip, sig_n_arr, sig_e_arr, w_arr = self.mats.get_bond_slip()
        self.graph = ResizeGraph(y_grid_label=True, x_grid_label=True, padding=5,
                                 xmin=float(min(slip)), xmax=round(1.1 * max(slip), 4),
                                 ymin=float(min(sig_e_arr)), ymax=round(1.1 * max(sig_e_arr), 4),
                                 n_x_ticks=5., n_y_ticks=5.,
                                 xlabel='slip [mm]', ylabel='bond [N/mm]')
        self.sig_n_line = LinePlot(width=1.5)
        self.sig_n_line.points = self.list_tuple(slip, sig_n_arr)

        self.sig_e_line = DashedLine(color=[255, 0, 0])
        self.sig_e_line.points = self.list_tuple(slip, sig_e_arr)

        self.w_line = DashedLine(color=[0, 0, 255])
        self.w_line.points = self.list_tuple(slip, w_arr)

        self.graph.add_plot(self.sig_n_line)
        self.graph.add_plot(self.sig_e_line)
        self.graph.add_plot(self.w_line)

        self.add_widget(self.graph)

    def update_graph(self):
        slip, sig_n_arr, sig_e_arr, w_arr = self.mats.get_bond_slip()
        self.graph.x_min = float(min(slip))
        self.graph.x_max = round(1.1 * max(slip), 4)
        self.graph.y_min = float(min(sig_e_arr))
        self.graph.y_max = round(1.1 * max(sig_e_arr), 4)
        self.sig_n_line.points = self.list_tuple(slip, sig_n_arr)
        self.sig_e_line.points = self.list_tuple(slip, sig_e_arr)
        self.w_line.points = self.list_tuple(slip, w_arr)

    def create_panel(self):
        self.panel = GridLayout(cols=2)

        self.panel.add_widget(Label(text='elastic modulus [N/mm]'))
        self.e_b_button = Button()
        self.e_b_button.text = str(self.mats.E_b)
        self.e_b_button.btn_name = 'elastic shear modulus [N/mm]'
        self.e_b_button.bind(on_press=self.show_numpad)
        self.panel.add_widget(self.e_b_button)

        self.panel.add_widget(Label(text='yielding stress [N/mm]'))
        self.sig_y_button = Button()
        self.sig_y_button.text = str(self.mats.sigma_y)
        self.sig_y_button.btn_name = 'yielding stress [N/mm]'
        self.sig_y_button.bind(on_press=self.show_numpad)
        self.panel.add_widget(self.sig_y_button)

        self.panel.add_widget(Label(text='plasticity modulus'))
        self.K_button = Button()
        self.K_button.text = str(self.mats.K_bar)
        self.K_button.btn_name = 'plasticity modulus'
        self.K_button.bind(on_press=self.show_numpad)
        self.panel.add_widget(self.K_button)

        self.panel.add_widget(Label(text='hardening modulus'))
        self.H_button = Button()
        self.H_button.text = str(self.mats.H_bar)
        self.H_button.btn_name = 'hardening modulus'
        self.H_button.bind(on_press=self.show_numpad)
        self.panel.add_widget(self.H_button)

        self.panel.add_widget(Label(text='damage law'))
        self.damage_button = Button()
        self.damage_button.text = 'configure...'
        self.damage_button.bind(on_press=self.show_damage_editor)
        self.panel.add_widget(self.damage_button)

        self.ok_button = Button(text='OK')
        self.cancel_button = Button(text='Cancel')
        self.panel.add_widget(self.ok_button)
        self.panel.add_widget(self.cancel_button)

        self.add_widget(self.panel)

    def show_damage_editor(self, btn):
        self.damage_pop.open()

    @staticmethod
    def list_tuple(xdata, ydata):
        '''convert arrays to list of tuples for line plot'''
        return list(map(tuple, np.vstack((xdata, ydata)).T))

    def show_numpad(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = btn.text
        self.editNumpad.title = btn.btn_name
        self.editNumpad.open()

    def close_numpad(self):
        self.editNumpad.dismiss()

    def finished_numpad(self):
        self.editNumpad.dismiss()

        if self.focusBtn == self.e_b_button:
            self.e_b_button.text = self.numpad.lblTextinput.text
            self.mats.E_b = float(self.e_b_button.text)
        elif self.focusBtn == self.sig_y_button:
            self.sig_y_button.text = self.numpad.lblTextinput.text
            self.mats.sigma_y = float(self.sig_y_button.text)
        elif self.focusBtn == self.K_button:
            self.K_button.text = self.numpad.lblTextinput.text
            self.mats.K_bar = float(self.K_button.text)
        elif self.focusBtn == self.H_button:
            self.H_button.text = self.numpad.lblTextinput.text
            self.mats.H_bar = float(self.H_button.text)

        self.update_graph()


if __name__ == '__main__':

    from kivy.app import App

    class MainWindow(App):

        def build(self):
            return BondEditor()

    MainWindow().run()
