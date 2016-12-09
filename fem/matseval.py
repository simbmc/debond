'''
Created on 26.07.2016

@author: Yingxiong
'''
import numpy as np


class MATSEval(object):

    def __init__(self, **kwargs):
        self.E_m = 28484.
        self.E_f = 170000.
        self.E_b = 4.0
        self.sigma_y = 0.55
        self.K_bar = 0.04
        self.H_bar = 0.0
        self.n_s = 3
        self.f_damage_x = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])
        self.f_damage_y = np.array([0, 0.15, 0.3, 0.45, 0.6, 0.75])
        # set the keyword parameters (to replace the default values)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def f_damage(self, k):
        '''the multi-linear damage function'''
        return np.interp(k, self.f_damage_x, self.f_damage_y)

    @staticmethod
    def derivative(f, x, dx):
        return (f(x + dx) - f(x)) / dx

    def get_corr_pred(self, eps, d_eps, sig, alpha, q, kappa):
        n_e, n_ip, n_s = eps.shape
        D = np.zeros((n_e, n_ip, 3, 3))
        D[:, :, 0, 0] = self.E_m
        D[:, :, 2, 2] = self.E_f
        sig_trial = sig[:, :, 1]/(1-self.f_damage(kappa)) + self.E_b * d_eps[:,:, 1]
        xi_trial = sig_trial - q
        f_trial = abs(xi_trial) - (self.sigma_y + self.K_bar * alpha)
        elas = f_trial <= 1e-8
        plas = f_trial > 1e-8
        d_sig = np.einsum('...st,...t->...s', D, d_eps)
        sig += d_sig

        d_gamma = f_trial / (self.E_b + self.K_bar + self.H_bar) * plas
        alpha += d_gamma
        kappa += d_gamma
        q += d_gamma * self.H_bar * np.sign(xi_trial)
        w = self.f_damage(kappa)

        sig_e = sig_trial - d_gamma * self.E_b * np.sign(xi_trial)
        sig[:, :, 1] = (1-w)*sig_e

        E_p = -self.E_b / (self.E_b + self.K_bar + self.H_bar) * \
            self.derivative(self.f_damage, kappa, dx=1e-6) * sig_e \
            + (1 - w) * self.E_b * (self.K_bar + self.H_bar) / \
            (self.E_b + self.K_bar + self.H_bar)

        D[:, :, 1, 1] = (1-w)*self.E_b*elas + E_p*plas

        return sig, D, alpha, q, kappa

    def get_bond_slip(self):
        '''for plotting the bond slip relationship
        '''
        s_arr = np.hstack((np.linspace(0, 4. * self.sigma_y / self.E_b, 100, dtype=float),
                           np.linspace(4. * self.sigma_y / self.E_b, 3. * self.sigma_y / self.E_b, 25, dtype=float)))
        sig_n_arr = np.zeros_like(s_arr)
        sig_e_arr = np.zeros_like(s_arr)
        w_arr = np.zeros_like(s_arr)

        sig_e = 0.
        alpha = 0.
        kappa = 0.

        for i in range(1, len(s_arr)):
            d_eps = s_arr[i] - s_arr[i - 1]
            sig_e_trial = sig_e + self.E_b * d_eps
            f_trial = abs(sig_e_trial) - (self.sigma_y + self.K_bar * alpha)
            if f_trial <= 1e-8:
                sig_e = sig_e_trial
            else:
                d_gamma = f_trial / (self.E_b + self.K_bar)
                alpha += d_gamma
                kappa += d_gamma
                sig_e = sig_e_trial - d_gamma * self.E_b * np.sign(sig_e_trial)
            w = self.f_damage(kappa)
            w_arr[i] = w
            sig_n_arr[i] = (1. - w) * sig_e
            sig_e_arr[i] = sig_e

        return s_arr, sig_n_arr, sig_e_arr, w_arr

if __name__ == '__main__':

    from kivy.app import App
    from plot.resize_graph import ResizeGraph
    from plot.line import LinePlot
    from plot.dashedLine import DashedLine
    from kivy.uix.boxlayout import BoxLayout

    class MainWindow(App):

        def build(self):
            slip, sig_n_arr, sig_e_arr, w_arr = MATSEval().get_bond_slip()
            graph = ResizeGraph(y_grid_label=True, x_grid_label=True, padding=5,
                                xmin=float(min(slip)), xmax=round(1.1 * max(slip), 4),
                                ymin=float(min(sig_e_arr)), ymax=round(1.1 * max(sig_e_arr), 4),
                                n_x_ticks=5., n_y_ticks=5.,
                                xlabel='slip [mm]', ylabel='bond [N/mm]')
            sig_n_line = LinePlot(width=1.5)
            sig_n_line.points = self.list_tuple(slip, sig_n_arr)

            sig_e_line = DashedLine(color=[255, 0, 0])
            sig_e_line.points = self.list_tuple(slip, sig_e_arr)

            w_line = DashedLine(color=[0, 0, 255])
            w_line.points = self.list_tuple(slip, w_arr)

            graph.add_plot(sig_n_line)
            graph.add_plot(sig_e_line)
            graph.add_plot(w_line)

            root = BoxLayout()
            root.add_widget(graph)

            return root

        @staticmethod
        def list_tuple(xdata, ydata):
            return list(map(tuple, np.vstack((xdata, ydata)).T))

    MainWindow().run()
