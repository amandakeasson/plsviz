## TODO ##
# 1. add option to comment out data points

## importing packages
import os, getopt, sys 
import pandas as pd
import numpy as np
import nibabel as nib
from optparse import OptionParser

## Import mask
def importMask(mask_file):
	try:
		mask      = nib.load(mask_file)
		mask      = mask.get_data()
		mask_dims = mask.shape
		mask_vec  = reduce( (lambda x, y: x * y), mask_dims)
		mask_vec  = np.reshape(mask, (1,mask_vec))
		mask_vec  = (mask_vec > 0.5).astype(np.int_)
		st_coords = np.where(mask_vec == 1)[1]
	except:
		mask      = None
		st_coords = None
	print(mask_dims)
	print(st_coords.shape)
	return(mask_dims, st_coords)

## Import functional data
def importX(X_file, st_coords):
	dsets = [line.rstrip('\n') for line in open(X_file)]
	X_mat = np.array([])
	for dset in dsets:
		dset = nib.load(dset)
		dset_array = dset.get_data()
		
		#reshaping dset into vector
		dset_dims  = dset.shape
		dset_len   = reduce( (lambda x, y: x * y), dset_dims)
		dset_vec   = np.reshape(dset_array, (1,dset_len))

		# apply the mask
		dset_vec = np.array(dset_vec[0, st_coords])

		try:
			X_mat = np.vstack([X_mat, dset_vec])
		except:
			X_mat = dset_vec
	print(X_mat.shape)
	return(X_mat)

## import behavioural data
def importY(Y_file, X_mat):
	behav = pd.read_csv(Y_file, sep=',', header=None)
	Y_mat = behav.values
	print(Y_mat.shape)
	return(Y_mat)

def main():
	## define help text
	help_txt = 'test.py -f/--fun <functional_list.txt> -b/--behav <behav_data.csv> -g/--cond <group_index.txt> -m/--mask <mask.nii>'

	## get opts from terminal
	parser = OptionParser()
	parser.add_option("-x",           dest="X_file"   , type='str', help="Text file listing all image files to load into the PLS."       )
	parser.add_option("-y",           dest="Y_file"   , type='str', help="Absolute path to the behavioural data. First column defines group membership (use integers). Must be in .csv format.")
	parser.add_option("-m", "--mask", dest="mask_file", type='str', help="Absolute path to the brain/roi mask."                          )
	(options, args) = parser.parse_args()

	# define variables
	try:
		options.Y_file
	except:
		print('You need to include a behaviour/condition file.')
		print(help_txt)
		sys.exit()

	X_file    = options.X_file
	Y_file    = options.Y_file
	mask_file = options.mask_file

	mask_out  = importMask(mask_file)
	mask_dims = mask_out[0]
	st_coords = mask_out[1]

	X_mat = importX(X_file, st_coords)
	Y_mat = importY(Y_file, X_mat)

	return {'X_mat': X_mat, 'Y_mat': Y_mat, 'mask_dims': mask_dims, 'st_coords': st_coords}

if __name__ == '__main__':
	main()