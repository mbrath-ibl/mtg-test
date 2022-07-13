#APPLICATION: TestMsg
import h5py
import hdf5plugin
from lib2to3.pgen2 import driver
import warnings

from satpy import Scene
from satpy import available_writers
from satpy.writers import compute_writer_results
from satpy import find_files_and_readers
from pprint import pprint
from satpy.utils import debug_on
from satpy.utils import check_satpy
from pyresample import load_area

import glob
import dask
import sys
import numpy as np
import logging

from satpy import available_writers
import satpy
import argparse
import re
import os


#############################################################################################################
# DEBUG INFO/DATA INFO
ap = argparse.ArgumentParser(description="""
    Tool for testing mtg data collection and transformation
    Example: python3.9 testMTGtoCOG.py --inpattern='*BODY*T_0073*.nc' --in='/mnt/hdd/mtgdata/MTG_data_0073/' --out='/mnt/hdd/mtgdata/output/' --satpyreader=fci_l1c_nc --channels=true_color_r
    Example: python3.9 testMTGtoCOG.py --inpattern='*202207121015*' --in='/home/mbrath/mtgdata/H-MSG4__-MSG4________' --out='/mnt/hdd/mtgdata/output/' --satpyreader=seviri_l1b_hrit --channels=seviri_l1b_hrit
    """
)
ap.add_argument("--debug", required=False, help="Turns on debug output", action='store_true')
ap.add_argument("--dependencies", required=False, help="Prints satpy dependencies status", action='store_true')
ap.add_argument("--in", help="Input dir '/mnt/hdd/mtgdata/MTG_data_0073/', '/mnt/hdd/mtgdata/RC0001_compressed/'", required=False)
ap.add_argument("--inpattern", help="Input filename pattern '/*BODY*T_0073*.nc', '/*BODY*T_0001*.nc'", required=False)
ap.add_argument("--out", help="Out dir '/mnt/hdd/mtgdata/output/'", required=False)
ap.add_argument("--channels", help="Comma separated list of channels: ir_133, ir_38, ir_87, ir_97", required=False)
ap.add_argument("--getcomposites", required=False, help="Retrieves list of available composites", action='store_true')
ap.add_argument("--getdatasets", required=False, help="Retrieves list of available datasets", action='store_true')
ap.add_argument("--satpyreader", required=False, help="One of satpy readers MTG='fci_l1c_nc' MSG='seviri_l1b_hrit'")

args = vars(ap.parse_args())

if args["debug"]:
    debug_on()
    
if args["dependencies"]:
    check_satpy()

srcdir = args["in"]
outdir = args["out"]

dask.config.set(num_workers=24, num_threads=24)
print('Glob filtering...')
files = glob.glob(os.path.join(srcdir, args["inpattern"]))

if files is None:
    print("No matched files found!")
    exit

print('Scene loading...')
scene = Scene(filenames=files, reader=args["satpyreader"])


if args["getcomposites"]:
    print("..................AVAILABLE COMPOSITES..................")
    print(scene.available_composite_names())

elif args["getdatasets"]:
    print("..................AVAILABLE DATASETS....................")
    print(scene.available_dataset_names())

else:
    if(args["channels"]):
        channels = re.split(', |,|,  | ,| , ', args["channels"])
        print('Channels loading : %s' % str(channels))
        scene.load(channels)

        print('Saving datasets...')
        outputFiles = outdir + "MTG_{name}_{start_time:%Y%m%d_%H%M%S}.geotiff"
        result = scene.save_datasets(datasets=channels, filename=outputFiles, compute=False, writer='geotiff', num_threads=24, num_workers=24)
        compute_writer_results([result])
    else:
        print("missing channels, example: --channels=\"natural_color_t, ir_133\"")


