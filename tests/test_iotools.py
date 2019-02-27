from unittest import TestCase
import pyaverage.iotools as iot
import numpy as np
import pandas as pd
import os
import logging
logger = logging.getLogger(__name__)

class TestReadCsv(TestCase):

    def setUp(self):
        self.test_csv_path = os.path.join('tests','test_fxy.csv')
        self.columns = ['frame', 'x [nm]', 'y [nm]']
        if not os.path.exists(self.test_csv_path):
            self.generate_test_table()
        self.df = iot.read_csv_to_pandas(self.test_csv_path)

    def tearDown(self):
        self.rm_test_table()
    
    def generate_test_table(self):
        logger.info('creating test csv')
        data = np.random.rand(10, 3)
        df = pd.DataFrame(data=data, columns=self.columns)
        df.to_csv(self.test_csv_path, index=False)

    def rm_test_table(self):
        logger.info('removing test csv')
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)
        

    def test_read_csv_to_pandas(self):
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertListEqual(list(self.df.columns), self.columns)

    def test_extract_xy_from_pandas(self):
        xy = iot.get_xy_from_pandas(self.df, keys=['x [nm]', 'y [nm]'])
        self.assertTupleEqual(xy.shape, (10,2))
        

