import numpy as np


## Euler Angles
"""
Euler angles to single axis rotation matrices.

The mX notation came from the order of rotations in the
Euler angle definitions. m1 represent the Direction Cosine Matrix
rotation along the ex 1, and so on.
"""

def _dcm_from_x_axis_rotation(ang):
    return np.array([
        [1, 0, 0],
        [0, np.cos(ang), np.sin(ang)],
        [0, -np.sin(ang), np.cos(ang)]
    ])


def _dcm_from_y_axis_rotation(ang):
    return np.array([
        [np.cos(ang), 0, -np.sin(ang)],
        [0, 1, 0],
        [np.sin(ang), 0, np.cos(ang)]
    ])


def _dcm_from_z_axis_rotation(ang):
    return np.array([
        [np.cos(ang), np.sin(ang), 0],
        [-np.sin(ang), np.cos(ang), 0],
        [0, 0, 1]
    ])

class EulerAngles:
    """
    This class represent a rotation in euler angles.
    """
    _single_axis_rotations = {
        'x': _dcm_from_x_axis_rotation,
        'y': _dcm_from_y_axis_rotation,
        'z': _dcm_from_z_axis_rotation,
    }
    allowed_orders = ['xyx', 'xyz', 'xzx', 'xzy', 'yxy', 'yxz', 'yzx', 'yzy', 'zxy',
                      'zxz', 'zyx', 'zyz']

    def __init__(self, r1, r2, r3, order='xyz'):
        """
        :param r1: Angle in radians for first rotation
        :param r2: Angle in radians for second rotation
        :param r3: Angle in radians for third rotation
        :param order: Order of the rotation axes. Default is 'xyz'
        """
        self.order = order.lower()
        if order not in self.allowed_orders:
            raise NotImplementedError(
                f"Euler angles with order {order} are not allowed")
        self.vector = np.array([r1, r2, r3])
        self.dcm = None
        self.B = None
        self.invB = None

    def compute_B_matrix(self):
        s1 = np.sin(self.vector[0])
        c1 = np.cos(self.vector[0])
        s2 = np.sin(self.vector[1])
        c2 = np.cos(self.vector[1])
        s3 = np.sin(self.vector[2])
        c3 = np.cos(self.vector[2])
        if self.order == 'xyx':
            self.B = 1/s2 * np.array([
                [0, s3, c3],
                [0, s2*c3, -s2*s3],
                [s2, -c2*s3, -c2*c3]
            ])
            self.invB = np.array([
                [c2, 0, 1],
                [s2*s3, c3, 0],
                [s2*c3, -s3, 0]
            ])
        elif self.order == 'xyz':
            self.B = 1/c2 * np.array([
                [c3, -s3, 0],
                [c2*s3, c2*c3, 0],
                [-s2*c3, s2*s3, c2]
            ])
            self.invB = np.array([
                [c2*c3, s3, 0],
                [-c2*s3, c3, 0],
                [s2, 0, 1]
            ])
        elif self.order == 'xzx':
            self.B = 1/s2 * np.array([
                [0, -c3, s3],
                [0, s2*s3, s2*c3],
                [s2, c2*c3, -c2*s3]
            ])
            self.invB = np.array([
                [c2, 0, 1],
                [-s2*c3, s3, 0],
                [s2*s3, c3, 0]
            ])
        elif self.order == 'xzy':
            self.B = 1/c2 * np.array([
                [c3, 0, s3],
                [-c2*s3, 0, c2*c3],
                [s2*c3, c2, s2*s3]
            ])
            self.invB = np.array([
                [c2*c3, -s3, 0],
                [-s2, 0, 1],
                [c2*s3, c3, 0]
            ])
        elif self.order == 'yxy':
            self.B = 1/s2 * np.array([
                [s3, 0, -c3],
                [s2*c3, 0, s2*s3],
                [-c2*s3, s2, c2*c3]
            ])
            self.invB = np.array([
                [s2*s3, c3, 0],
                [c2, 0, 1],
                [-s2*c3, s3, 0]
            ])
        elif self.order == 'yxz':
            self.B = 1/c2 * np.array([
                [s3, c3, 0],
                [c2*c3, -c2*s3, 0],
                [s2*s3, s2*c3, c2]
            ])
            self.invB = np.array([
                [c2*s3, c3, 0],
                [c2*c3, -s3, 0],
                [-s2, 0, 1]
            ])
        elif self.order == 'yzx':
            self.B = 1/c2 * np.array([
                [0, c3, -s3],
                [0, c2*s3, c2*c3],
                [c2, -s2*c3, s2*s3]
            ])
            self.invB = np.array([
                [s2, 0, 1],
                [c2*c3, s3, 0],
                [-c2*s3, c3, 0]
            ])
        elif self.order == 'yzy':
            self.B = 1/s2 * np.array([
                [c3, 0, s3],
                [-s2*s3, 0, s2*c3],
                [-c2*c3, s2, -c2*s3]
            ])
            self.invB = np.array([
                [s2*c3, -s3, 0],
                [c2, 0, 1],
                [s2*s3, c3, 0]
            ])
        elif self.order == 'zxy':
            self.B = 1/c2 * np.array([
                [-s3, 0, c3],
                [c2*c3, 0, c2*s3],
                [s2*s3, c2, -s2*c3]
            ])
            self.invB = np.array([
                [-c2*s3, c3, 0],
                [s2, 0, 1],
                [c2*c3, s3, 0]
            ])
        elif self.order == 'zxz':
            self.B = 1/s2 * np.array([
                [s3, c3, 0],
                [s2*c3, -s2*s3, 0],
                [-c2*s3, -c2*c3, s2]
            ])
            self.invB = np.array([
                [s3*s2, c3, 0],
                [s2*c3, -s3, 0],
                [c2, 0, 1]
            ])
        elif self.order == 'zyx':
            self.B = 1/c2 * np.array([
                [0, s3, c3],
                [0, c2*c3, -c2*s3],
                [c2, s2*s3, s2*c3]
            ])
            self.invB = np.array([
                [-s2, 0, 1],
                [c2*s3, c3, 0],
                [c2*c3, -s3, 0]
            ])
        else:
            # This ends to be zyz order
            self.B = 1/s2 * np.array([
                [-c3, s3, 0],
                [s2*s3, s2*c3, 0],
                [c2*c3, -c2*s3, s2]
            ])
            self.invB = np.array([
                [-s2*c3, s3, 0],
                [s2*s3, c3, 0],
                [c2, 0, 1]
            ])

    @staticmethod
    def is_order_symmetric(order):
        return order == order[::-1]

    def compute_dcm(self):
        """
        Compute the Direction Cosine Matrix from the euler angles.
        The method used is concatenate single axis rotations instead of direct formula.
        TODO: Compute benchmarks of concatenate single axis Vs direct formulas
        """
        dcm = np.identity(3)
        for axis, ang in zip(reversed(self.order), reversed(self.vector)):
            dcm = dcm @ self._single_axis_rotations[axis](ang)
        self.dcm = dcm

    @classmethod
    def from_dcm(cls, dcm, order='zyx'):
        """
        Compute euler angles from a Direction Cosine Matrix
        """
        order = order.lower()
        if order not in cls.allowed_orders:
            raise NotImplementedError(
                f"Euler angles with order {order} are not allowed")
        if order == 'xyx':
            r2 = np.arccos(dcm[0][0])
            r1 = np.arctan(-dcm[0][1]/dcm[0][2])
            r3 = np.arctan(dcm[1][0]/dcm[2][0])
        elif order == 'xyz':
            r2 = np.arcsin(dcm[2][0])
            r1 = np.arctan(-dcm[2][1]/dcm[2][2])
            r3 = np.arctan(-dcm[1][0]/dcm[0][0])
        elif order == 'xzx':
            r2 = np.arccos(dcm[0][0])
            r1 = np.arctan(dcm[0][2]/dcm[0][1])
            r3 = np.arctan(dcm[2][0]/(-dcm[1][0]))
        elif order == 'xzy':
            r2 = np.arcsin(-dcm[1][0])
            r1 = np.arctan(dcm[1][2]/dcm[1][1])
            r3 = np.arctan(dcm[2][0]/dcm[0][0])
        elif order == 'yxy':
            r2 = np.arccos(dcm[1][1])
            r1 = np.arctan(dcm[1][0]/dcm[1][2])
            r3 = np.arctan(dcm[0][1]/(-dcm[2][1]))
        elif order == 'yxz':
            r2 = np.arcsin(-dcm[1][2])
            r1 = np.arctan(dcm[2][0]/dcm[2][2])
            r3 = np.arctan(dcm[0][1]/dcm[1][1])
        elif order == 'yzx':
            r2 = np.arcsin(dcm[0][1])
            r1 = np.arctan(-dcm[0][2]/dcm[0][0])
            r3 = np.arctan(-dcm[2][1]/dcm[1][1])
        elif order == 'yzy':
            r2 = np.arccos(dcm[1][1])
            r1 = np.arctan(-dcm[1][2]/dcm[1][0])
            r3 = np.arctan(dcm[2][1]/dcm[0][1])
        elif order == 'zxy':
            r2 = np.arcsin(dcm[1][2])
            r1 = np.arctan(-dcm[1][0]/dcm[1][1])
            r3 = np.arctan(-dcm[0][2]/dcm[2][2])
        elif order == 'zxz':
            r2 = np.arccos(dcm[2][2])
            r1 = np.arctan(dcm[2][0]/(-dcm[2][1]))
            r3 = np.arctan(dcm[0][2]/dcm[1][2])
        elif order == 'zyx':
            r2 = np.arcsin(-dcm[0][2])
            r1 = np.arctan(dcm[0][1]/dcm[0][0])
            r3 = np.arctan(dcm[1][2]/dcm[2][2])
        else:
            # This is from wikipedia: https://en.wikipedia.org/wiki/Euler_angles
            # This ends to be zyz order
            r2 = np.arccos(dcm[2][2])
            r1 = np.arctan(dcm[1][2]/dcm[0][2])
            r3 = np.arctan(dcm[2][1]/(-dcm[2][0]))
        euler = cls(r1, r2, r3, order)
        return euler