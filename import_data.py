## importing imaging data
import os
import pandas as pd
import numpy as np
import nibabel as nib

## Check for mask
# sample_mask = '/Users/steveneusebio/Documents/brain_hack/pls_m2py/sample_datasets/bin_fun_MNI152.nii.gz'
# mask_path   = sample_mask

try:
  mask      = nib.load(mask_path)
  mask      = mask.get_data()

  mask_dims = mask.shape

  mask_vec  = reduce( (lambda x, y: x * y), mask_dims)
  mask_vec  = np.reshape(mask, (1,mask_vec))
  mask_vec  = (mask_vec > 0.5).astype(np.int_)

  st_coords = np.where(mask_vec == 1)[1]
except:
  mask = None

## Import functional data
# sample_fun = '/Users/steveneusebio/Documents/brain_hack/pls_m2py/sample_datasets/sample_list.txt'
# fun_name = sample_fun

# feed in a text file where each line is the absolute path to
# subject nifti data

with open(fun_name) as f:
  dsets = [line.rstrip('\n') for line in open(fun_name)]

  X_mat = np.array([])
  for dset in dsets:

    dset = nib.load(dset)
    dset_array = dset.get_data()
    
    #reshaping dset into vector
    dset_dims  = dset.shape
    dset_len   = reduce( (lambda x, y: x * y), dset_dims)
    dset_vec   = np.reshape(dset_array, (1,dset_len))

    # apply the mask
    dset_vec = [dset_vec[0,st_coords]]

    try:
      X_mat = np.append(X_mat, dset_vec, 0)
    except:
      X_mat = dset_vec

## import behavioural data
# behavioural data must be a csv, each row = 1 subject/run
#                                 each column = behav measure

# sample data

# sample_behav = '/Users/steveneusebio/Documents/brain_hack/pls_m2py/sample_datasets/behav_sample.csv'
# behav_nm = sample_behav

behav = pd.read_csv(behav_nm, sep=',')
Y_mat = behav.values

## define groups
## *optional

# group file must be a csv with one column, 
# each row defining subject group membership. 
try:
  G_mat = pd.read_csv(group_file, header=None)
  G_mat = G_mat.set_index([0]).index.values
except:
  G_mat = [1] * X_mat.shape[0]
  G_mat = pd.DataFrame(G_mat)