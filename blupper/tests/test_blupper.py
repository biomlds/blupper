# from unittest import TestCase
#
# import funniest

# class TestJoke(TestCase):
#    def test_is_string(self):
#        s = funniest.joke()
#
#         self.assertTrue(isinstance(s, basestring))

import pandas as pd
import numpy as np
import nose
from blupper.mock_data import ex_eight_animals_data_table, ex_pedigree_six_animals
from blupper.mme import mme_solution, A_inverse_no_inbreeding


def test_mme_solution():
    """Check if BLUPS are properly calculated
    """

    sigma_sq_a = 20
    sigma_sq_e = 40
    df = ex_eight_animals_data_table()
    response_var = 'WWG'
    mme = mme_solution(df, sigma_sq_a, sigma_sq_e, response_var)
    blup_predicted = mme.BLUP.apply(lambda x: round(x, 3)).to_numpy()
    blups_true = np.array([0.098, -0.019, -0.041, -0.009, -
                           0.186,  0.177, -0.249,  0.183])
    assert (blup_predicted == blups_true).all()


def test_A_inverse_no_inbreeding():
    """Check inversion of A not accounting for inbreeding
    """

    df = ex_pedigree_six_animals()
    result = A_inverse_no_inbreeding(df)

    ground_truth = np.array([[1.83, 0.5, -1, -0.67,  0, 0],
                             [0.5, 2, -1,  0,  0.5, -1],
                             [-1, -1, 2.5,  0.5, -1, 0],
                             [-0.67, 0, 0.5, 1.83, -1, 0],
                             [0, 0.5, -1, -1, 2.5, -1],
                             [0, -1, 0, 0, -1, 2]])

    assert np.array_equal(result.round(2), ground_truth)
