'''
Created on 23.09.2016

@author: Yingxiong
'''
from specimen import Specimen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from plot.separator import Separator
from kivy.uix.popup import Popup
import numpy as np
from numpad import Numpad
from fem.tstepper import TStepper
from fem.matseval import MATSEval
from fem.tloop import TLoop
from multilinear_editor import MultilinearEditor


class Settings(Popup):

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.specimen = Specimen(size_hint=(1, 0.2))
        self.title = 'Settings'
        self.create_btns()
        # assign the text values to the buttons
        self.cancel_settings()
        self.create_content()
        self.numpad = Numpad()
        self.numpad.p = self
        self.editNumpad = Popup(content=self.numpad)
        self.multilinear = MultilinearEditor()
        self.damage_editor = Popup(
            content=self.multilinear, title='edit damage law')

    def create_btns(self):
        # matrix stiffness
        self.m_s = Button()
        self.m_s.btn_name = 'Matrix stiffness [MPa]'
        self.m_s.bind(on_press=self.show_numpad)

        # reinforcement stiffness
        self.r_s = Button()
        self.r_s.btn_name = 'Reinforcement stiffness [MPa]'
        self.r_s.bind(on_press=self.show_numpad)

        # bond property
        self.b_p = Button(text='configure...')
        self.b_p.bind(on_press=self.show_numpad)

        # matrix area
        self.m_a = Button()
        self.m_a.btn_name = 'Matrix area [mm2]'
        self.m_a.bind(on_press=self.show_numpad)

        # reinforcement area
        self.r_a = Button()
        self.r_a.btn_name = 'Reinforcement area [mm2]'
        self.r_a.bind(on_press=self.show_numpad)

        # specimen length
        self.s_l = Button()
        self.s_l.btn_name = 'Specimen length [mm]'
        self.s_l.bind(on_press=self.show_numpad)

        # number of elements
        self.n_e = Button()
        self.n_e.btn_name = 'Number of elements'
        self.n_e.bind(on_press=self.show_numpad)

        # pull-out displacement
        self.p_d = Button()
        self.p_d.btn_name = 'Maximum pullout displacement[mm]'
        self.p_d.bind(on_press=self.show_numpad)

    def create_content(self):
        box = BoxLayout(orientation='vertical')

        # material settings
        mat = GridLayout(cols=6, padding=[5, 5, 5, 5])
        mat.add_widget(Label(text='Matrix\nStiffness'))
        mat.add_widget(self.m_s)
        mat.add_widget(Label(text='Reinforcement\nStiffness'))
        mat.add_widget(self.r_s)
        mat.add_widget(Label(text='Bond\nProperty'))
        mat.add_widget(self.b_p)

        geo = GridLayout(cols=6, padding=[5, 5, 5, 5])
        geo.add_widget(Label(text='Matrix\nArea'))
        geo.add_widget(self.m_a)
        geo.add_widget(Label(text='Reinforcement\nArea'))
        geo.add_widget(self.r_a)
        geo.add_widget(Label(text='Specimen\nLength'))
        geo.add_widget(self.s_l)

        fe = GridLayout(cols=4, padding=[5, 5, 5, 5])
        fe.add_widget(Label(text='Number of Elements'))
        fe.add_widget(self.n_e)
        fe.add_widget(Label(text='Maximum displacement'))
        fe.add_widget(self.p_d)

        upper = BoxLayout(orientation='vertical')
        upper.add_widget(
            Label(text='material properties', size_hint=(1, 0.5)))
        upper.add_widget(mat)
        box.add_widget(upper)
        box.add_widget(Separator())
        middle = BoxLayout(orientation='vertical')
        middle.add_widget(
            Label(text='geometric properties', size_hint=(1, 0.5)))
        middle.add_widget(geo)
        box.add_widget(middle)
        box.add_widget(Separator())
        lower = BoxLayout(orientation='vertical')
        lower.add_widget(
            Label(text='general settings', size_hint=(1, 0.5)))
        lower.add_widget(fe)
        box.add_widget(lower)
        box.add_widget(Separator())

        # ok and cancel
        self.ok = Button(text='OK')
#         self.ok.bind(on_press=self.confirm_settings)
        cancel = Button(text='Cancel')
        cancel.bind(on_press=self.dismiss_panel)
        ok_cancel = BoxLayout(
            orientation='horizontal', size_hint=(1, 0.5), padding=[5, 5, 5, 5])
        ok_cancel.add_widget(Label())
        ok_cancel.add_widget(Label())
        ok_cancel.add_widget(self.ok)
        ok_cancel.add_widget(cancel)
        box.add_widget(ok_cancel)
        self.content = box

    def show_damage_editor(self, btn):
        self.damage_editor.open()

    def dismiss_panel(self, btn):
        self.cancel_settings()
        self.dismiss()

    def reset(self, button):
        self.specimen.tl.initialize_arrays()
        self.specimen.x_current = 53.
        self.specimen.f_u_line.points = [(0, 0)]
        self.specimen.eps_sig_line.points = [(0, 0)]
        zero_line = self.specimen.list_tuple(
            self.specimen.x_coord, np.zeros_like(self.specimen.x_coord))
        self.specimen.shear_flow_line.points = zero_line
        self.specimen.reinf_disp_line.points = zero_line
        self.specimen.matrix_disp_line.points = zero_line
        self.specimen.slip_line.points = zero_line
        self.specimen.reinf.xrange = [10, 50]
        self.specimen.controller.xrange = [50, 56]

    def show_numpad(self, btn):
        self.focusBtn = btn
        self.numpad.lblTextinput.text = btn.text
        self.editNumpad.title = btn.btn_name
        self.editNumpad.open()

    def close_numpad(self):
        self.editNumpad.dismiss()

    def finished_numpad(self):
        self.focusBtn.text = str(float(self.numpad.lblTextinput.text))
        self.editNumpad.dismiss()

    def cancel_settings(self):
        self.m_s.text = str(self.specimen.tl.ts.mats_eval.E_m)
        self.r_s.text = str(self.specimen.tl.ts.mats_eval.E_f)
        self.m_a.text = str(self.specimen.tl.ts.A_m)
        self.r_a.text = str(self.specimen.tl.ts.A_f)
        self.s_l.text = str(self.specimen.tl.ts.L_x)
        self.n_e.text = str(self.specimen.tl.ts.n_e_x)
        self.p_d.text = str(self.specimen.max_displacement)

    def confirm_settings(self, btn):
        material = MATSEval(E_m=float(self.m_s.text),
                            E_f=float(self.r_s.text))
        tstepper = TStepper(mats_eval=material,
                            A_m=float(self.m_a.text),
                            A_f=float(self.r_a.text),
                            n_e_x=int(float(self.n_e.text)),
                            L_x=float(self.s_l.text))
#         tloop = TLoop(ts=tstepper)
#         self.specimen = Specimen(size_hint=(1, 0.2),
#                                  tl = tloop,
#                                  max_displacement = float(self.p_d.text))
#         self.dismiss()
#         self.reset(btn)
        print 'confirm settings'

        self.specimen.tl = TLoop(ts=tstepper)
        self.specimen.max_displacement = float(self.p_d.text)

        self.specimen.x_current = 53.
        self.specimen.f_u_line.points = [(0, 0)]
        self.specimen.eps_sig_line.points = [(0, 0)]
        zero_line = self.specimen.list_tuple(
            self.specimen.x_coord, np.zeros_like(self.specimen.x_coord))
        self.specimen.shear_flow_line.points = zero_line
        self.specimen.reinf_disp_line.points = zero_line
        self.specimen.matrix_disp_line.points = zero_line
        self.specimen.slip_line.points = zero_line
        self.specimen.reinf.xrange = [10, 50]
        self.specimen.controller.xrange = [50, 56]

        self.specimen.x_coord = np.linspace(
            0, self.specimen.tl.ts.L_x, self.specimen.tl.ts.n_e_x + 1)
        self.specimen.x_ip_coord = np.repeat(self.specimen.x_coord, 2)[1:-1]

        self.dismiss()


if __name__ == '__main__':

    from kivy.app import App

    class MainWindow(App):

        def build(self):
            s = Settings()
            return s

    MainWindow().run()
