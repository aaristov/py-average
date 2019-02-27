import numpy as np
from scipy import ndimage as ndi
from skimage.feature import match_template, peak_local_max
import pyaverage.hist as h
from tqdm import tqdm

import logging

#logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)



def generate_ring_template(px_nm=20, 
                           size=200,
                           diam_nm=120,
                           thick_nm=20,
                           smooth_nm=20):
    _size=size // px_nm
    _diam=diam_nm // px_nm
    _thick=thick_nm // px_nm
    qy,qx = np.indices((_size,_size))
    c = _size/2.
    ring = np.ones((_size, _size))
    ring[((qx-c)**2+(qy-c)**2)<((_diam - _thick)/2)**2]=0
    ring[((qx-c)**2+(qy-c)**2)>((_diam + _thick)/2)**2]=0
    if smooth_nm: ring= ndi.gaussian_filter(ring,smooth_nm / px_nm)
    return ring

def conv(img,kern):
    return match_template(img,kern,pad_input=True)

def detect_peaks(img, smooth=1, threshold=0.5):
    wga = ndi.gaussian_filter(np.array(img),smooth)
    peaks = peak_local_max(wga,min_distance=5,threshold_rel=threshold)
    return peaks


def extract_single_pore_coordinates(table_xy, peaks, crop_size, pixel_size, plot=False, limit=None):
    logger.debug(f'data shape: {table_xy.shape}')
    x_min, y_min = table_xy.min(axis=0)
    x_max, y_max = table_xy.max(axis=0)
    
    logger.debug(f'x span: {x_min, x_max}')
    logger.debug(f'y span: {y_min, y_max}')

    if plot: 
        hist = h.generate_hist2d(table_xy, px=pixel_size)
    extraction = []
    for y, x in tqdm(peaks[:limit], ascii=True, desc='Crop NUPs'):
        if plot: 
            h.plot_hist_with_peaks(hist, [(y, x)])
            
        logger.debug(f'peak xy: {x}, {y}')
        center_coordiantes = [x_min + y * pixel_size,
                              y_min + x * pixel_size] 
        x_range = (center_coordiantes[0] - crop_size/2, center_coordiantes[0] + crop_size/2)
        y_range = (center_coordiantes[1] - crop_size/2, center_coordiantes[1] + crop_size/2)
        
        
        logger.debug(f'x_range: {x_range}')
        logger.debug(f'y_range: {y_range}')
        selection_x = np.logical_and(table_xy[:,0] < x_range[1],
                                       table_xy[:,0] > x_range[0])
        
        selection_y = np.logical_and(table_xy[:,1] < y_range[1],
                                       table_xy[:,1] > y_range[0])
        
        selection = np.logical_and(selection_x, selection_y)
        
        crop = table_xy[selection] - np.array(center_coordiantes).reshape((1,2))
        extraction.append(crop)
        
        if plot:
            h.generate_hist2d(crop, px=pixel_size, plot=True)
    return extraction

def concatenate_pores(nup_crops_xy):
    return np.concatenate(nup_crops_xy, axis=0)
   