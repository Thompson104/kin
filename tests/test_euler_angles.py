import math
import numpy as np

import pytest
from kin.euler_angles import EulerAngles
from kin.helpers import are_radians_close
from .cfg import KNOWN_CASES_TOLERANCE, ALL_ANGLES


# Singularities in Euler angles ocur when:
# - the order is simetric and the pitch angle is multiple of np.pi
# - the order is not simetric and the pitch angle is multiple of np.pi/2

non_singular_params = [(r1, r2, r3, order) for r1 in ALL_ANGLES
                       for r2 in ALL_ANGLES
                       for r3 in ALL_ANGLES
                       for order in EulerAngles.allowed_orders[9:11]
                       if (order[0] != order[-1] and not np.isclose(np.abs(r2), np.pi/2))
                       or (order[0] == order[-1] and
                           (not np.isclose(r2, 0.0) or not np.isclose(r2, np.pi)))]

singular_params = [(r1, r2, r3, order) for r1 in ALL_ANGLES
                   for r2 in ALL_ANGLES
                   for r3 in ALL_ANGLES
                   for order in EulerAngles.allowed_orders[9:11]
                   if (order[0] != order[-1] and np.isclose(np.abs(r2), np.pi/2))
                   or (order[0] == order[-1] and
                       (np.isclose(r2, 0.0) or np.isclose(r2, np.pi)))]


@pytest.mark.parametrize('r1,r2,r3,order', non_singular_params)
def test_dcm_conversion(r1, r2, r3, order):
    """
    Test the conversion from euler angles to DCM and vice-versa.
    The conversion is tested for non-singular cases.
    Thus this test case alwsays test for `angle % np.pi` is different than zero
    """
    euler_1 = EulerAngles(r1, r2, r3, order)
    euler_1.compute_dcm()
    euler_2 = EulerAngles.from_dcm(euler_1.dcm, order)
    euler_2.compute_dcm()

    assert np.isclose(np.transpose(euler_1.dcm) @ euler_2.dcm, np.eye(3)).all() or \
           np.isclose(euler_1.dcm @ euler_2.dcm, np.eye(3)).all()

@pytest.mark.parametrize('r1,r2,r3,order', singular_params)
def test_singular_dcm_conversion(r1, r2, r3, order):
    """
    For those cases where `angle % np.pi/2`, the related DCM will be identity.
    """
    euler_1 = EulerAngles(r1, r2, r3, order)
    euler_1.compute_dcm()
    euler_2 = EulerAngles.from_dcm(euler_1.dcm, order)
    euler_2.compute_dcm()

    assert np.isnan(euler_2.vector).any() or np.isinf(euler_2.vector).any()


@pytest.mark.parametrize('r1,r2,r3,order', non_singular_params)
def test_B_matrix_and_inverse(r1, r2, r3, order):
    """
    Test that $[B] . [B]^{-1} = [I_{3 \times 3}]$
    """
    euler = EulerAngles(r1, r2, r3, order)
    euler.compute_B_matrix()
    # if the determinant is close to 1.0 the test passes
    assert np.isclose(np.linalg.det((euler.invB @ euler.B)), 1.0)


@pytest.mark.parametrize('r1,r2,r3,order', singular_params)
def test_singular_B_matrix(r1, r2, r3, order):
    """
    Test that singular angles return a B matrix with some infinity values
    """
    euler = EulerAngles(r1, r2, r3, order)
    euler.compute_B_matrix()
    # if `(angle % np.pi) == 0` the B matrix will contain some values as np.Inf
    assert (euler.B == np.Inf).any()


@pytest.mark.parametrize('dcm,r1,r2,r3,order',
[(np.array( # From some Coursera Concept Check
    [[0.92541658, 0.33682409, -0.17364818],
     [-0.36515929, 0.91510341, -0.17101007],
     [0.10130573, 0.2216648, 0.96984631]]),
  0.3490658503988659, 0.17453292519943295, -0.17453292519943295, 'zyx'),
 (np.array( # Hanspeter Schaub and John L. Junkins - Example 3.2
     [[0.303372, -0.0049418, 0.952859],
      [-0.935315, 0.1895340, 0.298769],
      [-0.182075, -0.9818620, 0.052877]]),
  np.deg2rad(0.933242), np.deg2rad(-1.26252), np.deg2rad(-57.6097), 'zyx')
 ])
def test_dcm_conversion_known_cases(dcm, r1, r2, r3, order):
    euler_1 = EulerAngles(r1, r2, r3, order)
    euler_1.compute_dcm()
    euler_2 = EulerAngles.from_dcm(dcm, order)
    euler_2.compute_dcm()

    # Are both DCMs close to be equal?
    assert math.isclose(np.linalg.det(euler_1.dcm @ euler_2.dcm),
                        1.0)
    # Are euler angles close to be equal?
    assert np.isclose(euler_1.vector - euler_2.vector, 0.).all()