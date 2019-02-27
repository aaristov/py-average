import pyaverage.iotools as iot
import pyaverage.hist as h
import pyaverage.template as t
import argparse 
import logging

#logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)


def get_parser():
    # Main parser
    parser = argparse.ArgumentParser('pyaverage')
    subparsers = parser.add_subparsers(dest='command')

    for command in ['average']:
        subparsers.add_parser(command)

    # trace
    av_parser = subparsers.add_parser('average', help='average NUPs')
    av_parser.add_argument('--csv', type=str, default='', required=True,
                              help='localization data in Thundestorm format')
    av_parser.add_argument('--diameter', '-d',  type=int, default='120',
                              help='expected diameter of NUP')
    av_parser.add_argument('--pixelsize', '-px',  type=int, default='20',
                              help='pixel size in nm to plot histogram')
    av_parser.add_argument('--size', '-s',  type=int, default='200',
                              help='crop size in nm to select NUPs')
    av_parser.add_argument('--threshold', '-t',  type=float, default='0.5',
                              help='relative threhold for peak detection after cross-correlation')
    av_parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
                

                    
    
    return parser

def get_args(argsv):
    parser = get_parser()
    try:
        if argsv is None:
            args = parser.parse_args()
        else:
            args = parser.parse_args(argsv)
        return args

    except TypeError:
        logger.error(f'Wrong args while parsing: {argsv}')
        exit(1)


def main(argsv=None):
    
    args = get_args(argsv)
    
    if args.command == 'average':
        logger.info('Start averaging')
        
        csv_path = args.csv
        px = args.pixelsize
        diam = args.diameter
        size = args.size
        threshold = args.threshold
        debug = args.debug

        if debug:
            logging.basicConfig(level='DEBUG')
        else:

            logging.basicConfig(level='INFO')

        logger.info(f'debug mode {debug}')

        df = iot.read_csv_to_pandas(csv_path)    
        logger.debug(f'Open table with columns {list(df.columns)} and {len(df)} lines')

        xy = iot.get_xy_from_pandas(df)
        logger.debug(f'Get xy table with shape {xy.shape}')
        hist, limits = h.generate_hist2d(xy, px=px)
        logger.debug(f'Generate histogram with size {hist.shape}')
        
        mask = t.generate_ring_template(px_nm=px, size=size, diam_nm=diam)
        logger.debug(f'Generate template with shape {mask.shape}')
        
        cc = t.conv(hist, mask)
        logger.debug(f'Run convolution')
        
        peaks = t.detect_peaks(cc, smooth=1, threshold=threshold)
        logger.info(f'Detect {len(peaks)} nups')

        extract = t.extract_single_pore_coordinates(xy,
                                          peaks=peaks,
                                          crop_size=size,
                                          pixel_size=px)
        logger.info(f'Crop {len(extract)} NUPs with cropsize {size}')

        concat = t.concatenate_pores(extract)
        logger.info('Concatenate NUPs')

        h.generate_hist2d(concat, plot=True, px=5)








if __name__ == "__main__":
    main()

