import pandas as pd
import logging

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

def open_csv(table_path):
    try:
        table = pd.read_csv(table_path)
        logger.info(f'table.shape: {table.shape}')
        return table
    except IOError:
        logger.error('Wrong path')
        return False


    
