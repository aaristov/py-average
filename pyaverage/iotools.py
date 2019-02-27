import pandas as pd
import logging

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

def read_localization_table_from_disk(table_path: str, read_func):
    """
    Reading csv file into pandas.Dataframe
    """
    try:
        table = read_func(table_path)
        logger.info(f'table.shape: {table.shape}')
        return table
    except IOError:
        logger.error('Wrong path')
        return False

def read_csv_to_pandas(path):
    return read_localization_table_from_disk(table_path=path, read_func=pd.read_csv)


def get_xy_from_pandas(pd_table: pd.DataFrame, keys=['x [nm]', 'y [nm]']):
    """
    Extracts xy columns from the table.
    Input: 
    pd_table – pandas DataFrame
    keys – colunm titles
    Returns:
    numpy array
    """
    return pd_table[keys].values
    
