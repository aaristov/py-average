import numpy as np
from scipy import ndimage as ndi


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