from kivy.app import App
from kivy.core.window import Window
import numpy as np
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from specimen import Specimen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from settings import Settings
# Window.size = (1280, 720)


class MainWindow(App):

    settings_popup = Settings()

    def add_widgets(self, root):
        self.settings_popup.ok.bind(on_press=self.re_build)
        page = PageLayout(border=30, swipe_threshold=0.2)
        p1 = BoxLayout(orientation='horizontal', background_color=[1, 1, 1, 1])
        p1.add_widget(self.settings_popup.specimen.eps_sig_wid)
        p1.add_widget(self.settings_popup.specimen.f_u_wid)
        page.add_widget(p1)

        p2 = BoxLayout(orientation='horizontal', background_color=[1, 1, 1, 1])
        p2.add_widget(self.settings_popup.specimen.disp_slip_wid)
        p2.add_widget(self.settings_popup.specimen.shear_flow_wid)
        page.add_widget(p2)

        upper = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        upper.add_widget(page)
        root.add_widget(upper)

        btns = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        settings = Button(text='Settings')
        settings.bind(on_press=self.settings_popup.open)

        reset = Button(text='Reset')
        reset.bind(on_press=self.settings_popup.reset)

        btns.add_widget(Label())
        btns.add_widget(Label())
        btns.add_widget(settings)
        btns.add_widget(reset)
        root.add_widget(self.settings_popup.specimen)
        root.add_widget(btns)

    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.add_widgets(self.root)
        return self.root

    def re_build(self, btn):
        self.settings_popup.confirm_settings(btn)
        self.root.clear_widgets()
        self.add_widgets(self.root)
        self.settings_popup.reset(None)


if __name__ == '__main__':
    MainWindow().run()
