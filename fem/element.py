
import numpy as np


class FETS1D52ULRH(object):

    '''
    Bar element with bond interface, the element is one-dimensional and has two nodes, each node has two DoFs
    '''

    def __init__(self):
        self.n_nodal_dofs = 2  # number of DoFs on each node
        self.dof_r = np.array([[-1], [1]])
        # the local coordinate of each node
        self.geo_r = np.array([[-1], [1]])
        # number of node positions associated with DoFs
        self.n_dof_r = len(self.dof_r)
        # number of DoFs in the element
        self.n_e_dofs = self.n_nodal_dofs * self.n_dof_r
        # number of integration points
        self.ngp_r = 2
        # coordinates of the integration points
        self.ip_coords = self.get_ip_coords()
        # weight of each integration points
        self.ip_weights = self.get_ip_weights()
        # number of integration points
        self.n_gp = len(self.ip_weights)

    def get_ip_coords(self):
        '''
        1st dimension: integration points
        2nd dimension: spatial dimension
        example: ip_coords[1, 1] -- 2nd integration point, y coordinate
        '''
        offset = 1e-8
        return np.array([[-1 + offset], [1 - offset]])

    def get_ip_weights(self):
        return np.array([1., 1.], dtype=float)

    def get_N_geo_mtx(self, r_pnt):
        '''
        Return geometric shape functions
        for the conversion of local coordinate r to global coordinate
        The matrix is a 2D array
        1st dimension: spatial dimension
        2nd dimension: element nodes
        example: N_geo_mtx[0, 1] -- x coordinate, second node
        for the present element
        x = (0.5-r/2)*x1 + (0.5+r/2)*x2,
        @param r_pnt:
        '''
        r = r_pnt[0]  # x coordinate of the point
        N_mtx = np.array([[0.5 - r / 2., 0.5 + r / 2.]])
        return N_mtx

    def get_dNr_geo_mtx(self, r_pnt):
        '''
        Return the matrix of shape function derivatives at the given points
        Used for the conrcution of the Jacobi matrix.
        The matrix is a 2D array
        1st dimension: spatial dimension
        2nd dimension: element nodes
        '''
        return np.array([[-1. / 2., 1. / 2.]])

    def get_N_mtx(self, r_pnt):
        '''
        Return shape functions for the displacement, 
        here we use the same functions as the geometric shape functions
        u = (0.5-r/2)*u1 + (0.5+r/2)*u2
        @param r_pnt:local coordinates
        '''
        return self.get_N_geo_mtx(r_pnt)

    def get_dNr_mtx(self, r_pnt):
        '''
        Return the derivatives of the shape functions
        '''
        return self.get_dNr_geo_mtx(r_pnt)

if __name__ == '__main__':

    f = FETS1D52ULRH()
    print f.get_dNr_geo_mtx(f.ip_coords)
