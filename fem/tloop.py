'''
Created on 16.08.2016

@author: Yingxiong
'''
from tstepper import TStepper
import numpy as np
from solve_pentadiagonal import solve


class TLoop(object):

    def __init__(self, **kwargs):
        self.ts = TStepper()
        self.kmax = 50
        # set the keyword parameters (to replace the default values)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        self.initialize_arrays()

    def initialize_arrays(self):
        '''create the arrays to store the state variables'''
        n_e = self.ts.n_e_x
        n_ip = self.ts.fets_eval.n_gp
        n_s = self.ts.mats_eval.n_s
        self.eps = np.zeros((n_e, n_ip, n_s))
        self.sig = np.zeros((n_e, n_ip, n_s))
        self.alpha = np.zeros((n_e, n_ip))
        self.q = np.zeros((n_e, n_ip))
        self.kappa = np.zeros((n_e, n_ip))
        self.U = np.zeros(self.ts.n_dofs)
        self.F = np.zeros(self.ts.n_dofs)

        self.d, self.a, self.b = self.get_initial_k()

        self.U_record = [0.]
        self.F_record = [0.]

        self.eps_record = [0.]
        self.sig_record = [0.]

    def get_initial_k(self):
        '''calculate the initial stiffness matrix'''
        d_U = np.zeros_like(self.U)
        F_int, d, a, b, eps, sig, alpha, q, kappa = \
            self.ts.get_corr_pred(
                self.U, d_U, self.eps, self.sig, self.alpha, self.q, self.kappa)
        return d, a, b

    def get_p(self, d_u):
        '''update the displacement and force corresponding to d_u'''
        n_dofs = self.ts.n_dofs
        u_incre = np.zeros(n_dofs)
        u_incre[-1] = d_u
        k = 0
        while k <= self.kmax:
            if k == self.kmax:
                print 'non_convergence'

            k += 1
            # solve the trail displacement incremental
            x = solve(
                n_dofs, self.d, self.a, self.b, self.a, self.b, u_incre)
            d_U = np.append(0, x[0:-1])
            # update the stiffness matrix and calculate the internal force
            F_int, self.d, self.a, self.b, self.eps, self.sig, self.alpha, self.q, self.kappa = \
                self.ts.get_corr_pred(
                    self.U, d_U, self.eps, self.sig, self.alpha, self.q, self.kappa)
            # update U
            self.U += d_U
            # reset d_U
            d_U = np.zeros(n_dofs)

            # calculate the unbalanced force
            self.F[-1] = F_int[-1]
            R = self.F - F_int

            # check convergence
            if np.linalg.norm(R[1:-1]) < 1e-8:
                #                     U_record.append(np.copy(U))
                #                     F_record.append(np.copy(P))
                self.U_record.append(self.U[-1])
                self.F_record.append(self.F[-1])
                self.eps_record.append(self.eps[0, -1, 1])
                self.sig_record.append(self.sig[0, -1, 1])
                break

            # set the unbalanced force as the RHS
            u_incre = np.hstack((R[1:-1], [0, 0]))

    def eval(self):
        n_dofs = self.ts.n_dofs
        n_e = self.ts.n_e_x
        n_ip = self.ts.fets_eval.n_gp
        n_s = self.ts.mats_eval.n_s
        sf_record = np.zeros(2 * n_e)
        eps_record = [np.zeros_like(self.eps)]
        sig_record = [np.zeros_like(self.sig)]

        for i in np.arange(100):
            print '====', i, '===='
            if i <= 60:
                self.get_p(0.1)
            else:
                self.get_p(-0.05)

if __name__ == '__main__':
    tl = TLoop()
    import matplotlib.pyplot as plt
    tl.eval()
#     U_record, F_record = tl.eval()
#     plt.plot(U_record[:, -1], F_record[:, -1])
    plt.plot(tl.U_record, tl.F_record)
#     plt.plot(tl.eps_record, tl.sig_record)
#     print U_record[:, -1]
#     print F_record[:, -1]
    plt.show()
