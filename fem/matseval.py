'''
Created on 26.07.2016

@author: Yingxiong
'''
import numpy as np


class MATSEval:

    def __init__(self, **kwargs):
        self.E_m = 28484.
        self.E_f = 170000.
        self.E_b = 4.0
        self.sigma_y = 0.55
        self.K_bar = 0.04
        self.H_bar = 0.0
        self.n_s = 3
        self.f_damage_x = np.array([0, 1])
        self.f_damage_y = np.array([0, 0.8])
        # set the keyword parameters (to replace the default values)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def f_damage(self, k):
        '''the multi-linear damage function'''
        return np.interp(k, self.f_damage_x, self.f_damage_y)

    @staticmethod
    def derivative(f, x, dx):
        return (f(x + dx) - f(x)) / dx

    def get_corr_pred1(self, eps, d_eps, sig, alpha, q, kappa):
        n_e, n_ip, n_s = eps.shape
        D = np.zeros((n_e, n_ip, 3, 3))
        D[:, :, 0, 0] = self.E_m
        D[:, :, 2, 2] = self.E_f
        sig_trial = sig[:, :, 1] + self.E_b * d_eps[:,:, 1]
        xi_trial = sig_trial - q
        f_trial = abs(xi_trial) - (self.sigma_y + self.K_bar * alpha)
        elas = f_trial <= 1e-8
        plas = f_trial > 1e-8
        E_p = ( self.E_b * ( self.K_bar + self.H_bar ) ) / \
            (self.E_b + self.K_bar + self.H_bar)
        D[:, :, 1, 1] = self.E_b*elas + E_p*plas
        d_sig = np.einsum('...st,...t->...s', D, d_eps)
        sig += d_sig

        d_gamma = f_trial / (self.E_b + self.K_bar + self.H_bar) * plas
        alpha += d_gamma
        q += d_gamma * self.H_bar * np.sign(xi_trial)

        sig[:, :, 1] = sig_trial - d_gamma * self.E_b * np.sign(xi_trial)

        return sig, D, alpha, q, kappa

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
        s_arr = np.hstack((np.linspace(0, 4. * self.sigma_y / self.E_b, 100),
                           np.linspace(4. * self.sigma_y / self.E_b, 3. * self.sigma_y / self.E_b, 25)))
        b_arr = np.zeros_like(s_arr)
        sig_e = 0.
        alpha = 0.

        for i in range(1, len(s_arr)):
            d_eps = s_arr[i] - s_arr[i - 1]
            sig_e_trial = sig_e + self.E_b * d_eps
            f_trial = abs(sig_e_trial) - (self.sigma_y + self.K_bar * alpha)
            if f_trial <= 1e-8:
                sig_e = sig_e_trial
            else:
                d_gamma = f_trial / (self.E_b + self.K_bar)
                alpha += d_gamma
                sig_e = sig_e_trial - d_gamma * self.E_b * np.sign(sig_e_trial)
            b_arr[i] = sig_e

        return s_arr, b_arr

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    s_arr, b_arr = MATSEval().get_bond_slip()
    plt.plot(s_arr, b_arr)
    plt.show()
