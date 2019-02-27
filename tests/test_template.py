from unittest import TestCase
from pyaverage.template import generate_ring_template

class TestRingTemplate(TestCase):

    def test_gen_ring(self):
        ring = generate_ring_template(px_nm=20, 
                                      size=200,
                                      diam_nm=120,
                                      thick_nm=20,
                                      smooth_nm=20)
        expected_size = 200/20
        self.assertTupleEqual(ring.shape, (expected_size, expected_size))
