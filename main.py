from kivy.app import App
from kivy.core.window import Window
import numpy as np
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from specimen import Specimen
# Window.size = (1280, 720)


class MainWindow(App):

    def build(self):
        root = BoxLayout(orientation='vertical')

        specimen = Specimen(size_hint=(1, 0.3))
        force_disp = Graph()
        bond_slip = Graph()

        upper = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        upper.add_widget(specimen.eps_sig_wid)
        upper.add_widget(specimen.f_u_wid)

        root.add_widget(upper)
        root.add_widget(specimen)
        return root

if __name__ == '__main__':
    MainWindow().run()
