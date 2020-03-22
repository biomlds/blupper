# from unittest import TestCase
#
# import funniest

# class TestJoke(TestCase):
#    def test_is_string(self):
#        s = funniest.joke()
#
#         self.assertTrue(isinstance(s, basestring))

import pandas as pd
import pandas as np
import nose
from blupper.mock_data import ex_eight_animals_data_table
from blupper.mme import mme_solution


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
