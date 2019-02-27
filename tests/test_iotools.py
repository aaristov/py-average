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
        if not os.path.exists(self.test_csv_path):
            self.generate_test_table()
        df = iot.read_csv_to_pandas(self.test_csv_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), self.columns)
