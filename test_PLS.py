import numpy as np
import PLSCORE as plsc
import pls
import csv

X = np.random.randn(100, 500)
print(X.shape)
Y = np.random.randn(100,30)
print(Y.shape)
C = np.zeros((100,))

for i in range(5):
    C[i*20:(i+1)*20] = i*np.ones((20,))

#print(Y[C == 0,:].shape)

with open("testdata_PLS.csv", 'r') as f:
    data_row = csv.reader(f, delimiter= ',')
    #print(type(data_row))
    data = [data for data in data_row]

data = np.asarray(data)

X1 = np.asarray(data[:,2:], dtype= float)
Y10 = np.asarray(data[:,1], dtype= float)
C1 = np.asarray(data[:,0], dtype= int)

Y1 = np.empty((len(Y10),1))
Y1[:,0] = Y10

#print(Y1)
#test = plsc.PLSCORE(X1,Y1,C1)
test = pls.PLS(X1, Y1)
print(test.getSaliencesBrain())
print(test.getSaliencesBhv_dsgn())
print(test.getSingularvalues())
print(test.getLatentBhv_dsgn())
print(test.getLatentBrain())

print(test.correlation_crossblock)
print(test.brain_orig)
print(test.brain)
print(test.getBrainScores())
print(test.getBhvScores())

test.getPermutation()
#print(test.getLatentBrain())
#print(test.getLatentBhv_dsgn())
#test.getPermutation()
#test.getBootstraps(nonrotated='no')

print(test.getSV_p())
print(test.getSaliencesBrain_stability())
