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

def get_xy_from(pd_table: pd.DataFrame, keys=['x [nm]', 'y [nm]']):
    """
    Extracts xy columns from the table.
    Input: 
    pd_table – pandas DataFrame
    keys – colunm titles
    Returns:
    numpy array
    """
    return pd_table[keys].values
    
