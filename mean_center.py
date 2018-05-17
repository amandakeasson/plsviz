## importing packages
import os, getopt, sys 
import pandas as pd
import numpy as np
import nibabel as nib
from optparse import OptionParser

def main(all, center_type):

	## get opts from terminal
	parser = OptionParser()
	parser.add_option("-a", "--all", dest="all", type='str', help="The dictionary containing the X, Y, and mask data.")
	parser.add_option("-c", "--center", dest="center_type", type='int', help="")
	(options, args) = parser.parse_args()

	X_mat       = options.all.X_mat
	Y_mat       = options.all.Y_mat
	center_type = options.center_type

	## Identify the groups present
	groups = np.unique(Y_mat[:,0])
	conds  = np.unique(Y_mat[:,1])

	if np.isin(False, np.equal(np.mod(groups,1), 0)):
		sys.exit('Group membership must be defined using integers in the first column of Y data.')
	if np.isin(False, np.equal(np.mod(conds,1), 0)):
		sys.exit('Conditions must be defined using integers in the second column of Y data.')

	# remove group mean from condition mean
	if center_type == 0:
		for grp in groups:
			grp_ind = np.where(Y_mat[:,0] == grp)
			
			tmp_Y_centered = Y_mat[grp_ind,2:] - Y_mat[grp_ind,2:].mean(axis=1)
			tmp_X_centered = X_mat[grp_ind, :] - X_mat[grp_ind, :].mean(axis=1)
			
			try:
				Y_centered = np.vstack([Y_centered, tmp_Y_centered])
				X_centered = np.vstack([X_centered, tmp_X_centered])
			except:
				Y_centered = tmp_Y_centered
				X_centered = tmp_X_centered

	# remove grand condition mean from each group condition mean
	if center_type == 1:
		for cond in conds:
			print(grp)
			cond_ind  = np.where(Y_mat[:,1] == cond)
			
			cond_mean_Y = Y_mat[cond_ind,2:].mean(axis=1)
			cond_mean_X = X_mat[cond_ind, :].mean(axis=1)
			for grp in groups:
				grp_ind = np.where(Y_mat[:,0] == grp)
				
				intersect_idn = np.intersect1d(cond_ind, grp_ind)

				tmp_Y_centered = Y_mat[intersect_idn,2:] - cond_mean_Y
				tmp_X_centered = X_mat[intersect_idn, :] - cond_mean_X

				try:
					Y_centered = np.vstack([Y_centered, tmp_Y_centered])
					X_centered = np.vstack([X_centered, tmp_X_centered])
				except:
					Y_centered = tmp_Y_centered
					X_centered = tmp_X_centered

	# remove grand mean over all subjects and all conditions
	elif center_type == 2:
		mean_Y = Y_mat[:,2:].mean(axis=1)
		mean_X = X_mat[:, :].mean(axis=1)
		
		tmp_Y_centered = Y_mat[:,2:] - mean_Y
		tmp_X_centered = X_mat[:, :] - mean_X
		try:
			Y_centered = np.vstack([Y_centered, tmp_Y_centered])
			X_centered = np.vstack([X_centered, tmp_X_centered])
		except:
			Y_centered = tmp_Y_centered
			X_centered = tmp_X_centered

	# Remove all main effects by subtracting all group and condition means (group * condition)
	elif center_type == 3:
		for cond in conds:
			cond_ind  = np.where(Y_mat[:,1] == cond)
			
			for grp in groups:
				grp_ind       = np.where(Y_mat[:,0] == grp)
				intersect_idn = np.intersect1d(cond_ind, grp_ind)
				
				intersect_mean_Y = Y_mat[intersect_idn,2:].mean(axis=1)
				intersect_mean_X = X_mat[intersect_idn, :].mean(axis=1)

				tmp_Y_centered = Y_mat[intersect_idn,2:] - intersect_mean_Y
				tmp_X_centered = X_mat[intersect_idn, :] - intersect_mean_X
				try:
					Y_centered = np.vstack([Y_centered, tmp_Y_centered])
					X_centered = np.vstack([X_centered, tmp_X_centered])
				except:
					Y_centered = tmp_Y_centered
					X_centered = tmp_X_centered

	else:
		sys.exit('Choose a mean-centering option from 0-3.')

	Y_centered = np.hstack([Y_mat[:,:2], Y_centered])

	return {'X_centered': X_centered, 'Y_centered': Y_centered}

if __name__ == '__main__':
	main()