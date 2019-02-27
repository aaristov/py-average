from unittest import TestCase
from pyaverage.hist import generate_hist2d
import numpy as np

class TestGenHist2D(TestCase):

    def test_gen_hist2d(self):
        xy = np.random.standard_normal((50,2)) * 100
        hist, _ = generate_hist2d(xy, px=20, shift=1, plot=False)
        self.assertEqual(hist.ndim, 2)
        
