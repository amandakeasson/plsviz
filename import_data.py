## importing imaging data
import os
import pandas as pd
import numpy as np
import nibabel as nib

## Import functional data
# sample = '/Users/steveneusebio/Documents/brain hack/pls_m2py/sample_datasets/sample_list.txt'
# feed in a text file where each line is the absolute path to
# subject nifti data
# fun_name = sample

with open(fun_name) as f:
  dsets = [line.rstrip('\n') for line in open(fun_name)]

  X_mat = np.array([])
  for dset in dsets:
    print(dset)

    dset = nib.load(dset)
    dset_array = dset.get_data()
    
    #reshaping dset into vector
    dset_dims  = dset.shape
    dset_len   = reduce( (lambda x, y: x * y), dset_dims)
    dset_vec   = np.reshape(dset_array, (1,dset_len))

    try:
      X_mat = np.append(X_mat, dset_vec, 0)
    except:
      X_mat = dset_vec

## import behavioural data
# behavioural data must be a csv, each row = 1 subject/run
#                                 each column = behav measure

# sample data
# sample = '/Users/steveneusebio/Documents/brain hack/pls_m2py/sample_datasets/behav_sample.csv'
# behav_nm = sample

behav = pd.read_csv(behav_nm, sep=',')
Y_mat = behav.values

## define groups
# *optional
# group file must be a csv with one column, 
# each row defining subject group membership. 
try:
  G_mat = pd.read_csv(group_file, header=None)
  G_mat = G_mat.set_index([0]).index.values
except:
  print('no groups defined')