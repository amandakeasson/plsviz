## TODO
# Make sure this is taking in the CENTERED matrices

## importing packages
import os, getopt, sys 
import pandas as pd
import numpy as np
import nibabel as nib
from optparse import OptionParser

## get opts from terminal
parser = OptionParser()
parser.add_option("-a", "--all", dest="all", type='str', help="The dictionary containing the X, Y, and mask data.")
parser.add_option("-r", "--correl", dest="correl_mode", type='int', help="Correlation Mode feature applies to Regular Behav PLS, Non-Rotated Behav PLS, Multiblock PLS, Non-Rotated Multiblock PLS.")
(options, args) = parser.parse_args()

X_mat       = options.all.X_mat
Y_mat       = options.all.Y_mat
correl_mode = options.correl_mode

if correl_mode = 0:
    R_mat = np.dot( np.transpose(Y_mat), X_mat )