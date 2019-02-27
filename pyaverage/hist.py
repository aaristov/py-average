from scipy import ndimage as ndi
import numpy as np
import logging
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt


logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

def generate_hist2d(xy, 
                px:int=20, 
                shift:int=0, 
                plot=False, 
                vmax=None, 
                cmap='hot'):
    '''
    Generates 2D histogram using numpy with given px and shift.
    Returns histogram, limits
    '''
    if px <=0: raise(ValueError(f'px must be positive number, got {px}'))
    logger.debug(f'data shape: {xy.shape}')
    assert xy.shape[0] > 0, 'data empty'
    assert xy.shape[1] == 2, 'data shape wrong'
    min_lim = xy.min(axis=0)
    max_lim = xy.max(axis=0)
    
    limits = list(zip(min_lim, max_lim))
    
    bins = list(np.floor((max_lim - min_lim)/px))
    
    logger.debug(f'pixel: {px}')
    logger.debug(f'limits: {limits}')
    logger.debug(f'nbins: {bins}')
    
    hist, xedges, yedges = np.histogram2d(x=xy[:,0].ravel(), y=xy[:,1].ravel(), bins=bins, range=limits)
    logger.debug(f'hist shape: {hist.shape}')
    while shift: 
        shift -= 1
        hist = average_shift_hist(hist)

    if plot:
        logger.debug(f'plot histogram')
    
        import itertools
        limits_list = list(itertools.chain(*limits))
        plot = plot_hist(hist, limits_list, vmax=vmax, cmap=cmap)

    return hist, limits


def average_shift_hist(a):
    for i in range(a.ndim):
        a = ndi.convolve1d(a,(1,2,1),i)
    return a


def plot_hist(hist, limits_list, vmax=None, cmap='hot'):
    try:
        plt.imshow(hist,
                    cmap=cmap,
                    vmax=vmax,
                    interpolation=None,
                    extent=[i/1000. for i in limits_list])
        plt.xlabel('x, µm')
        plt.ylabel('y, µm')
        plt.axis('square')
        plt.colorbar()
        plt.show()
    
        return True

    except Exception as e:
        logger.error(f'plot canceled: {e}')
        logger.error(f'limits: {limits_list}')
        return False
    
