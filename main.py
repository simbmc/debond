from kivy.app import App
from kivy.core.window import Window
import numpy as np
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from specimen import Specimen
# Window.size = (1280, 720)


class MainWindow(App):

    def build(self):
        root = BoxLayout(orientation='vertical')

        specimen = Specimen(size_hint=(1, 0.3))
        force_disp = Graph()
        bond_slip = Graph()
        page = PageLayout(border=20, swipe_threshold=0.2)
#         p2 = PageLayout()
        p1 = BoxLayout(orientation='horizontal', background_color=[1, 1, 1, 1])
        p1.add_widget(specimen.eps_sig_wid)
        p1.add_widget(specimen.f_u_wid)
        page.add_widget(p1)

        p2 = BoxLayout(orientation='horizontal', background_color=[1, 1, 1, 1])
        p2.add_widget(specimen.disp_slip_wid)
        p2.add_widget(specimen.shear_flow_wid)
        page.add_widget(p2)

        upper = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
#         upper.add_widget(specimen.eps_sig_wid)
#         upper.add_widget(specimen.f_u_wid)
        upper.add_widget(page)
#         upper.add_widget(p2)

        root.add_widget(upper)
        root.add_widget(specimen)
        return root

if __name__ == '__main__':
    MainWindow().run()
