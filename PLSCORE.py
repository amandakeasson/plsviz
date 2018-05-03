import numpy as np

class PLSCORE(object):

    """
    inputs: X: ndarray I by J matrix  Brain activity  which is arranged by the following


            Y:  ndarray I by K matrix  Behavior or design variables, which is arranged the same way as X

            C: array   number of colunms: 0 1 2
variables:
    self.brain
    self.bhv_dsgn
    self.cnd_indx
    self.saliencs_bhv_dsgn
    self.saliences_brain
    self.singularvalues

    self.latent_brain

    self.latent_bhv_dsgn


methods:


    """
# initial empty array
    index_norm = 0

    brain = np.array([])
    bhv_dsgn = np.array([])
    cnd_indx = np.array([])

    saliencs_bhv_dsgn = np.array([])
    saliences_brain = np.array([])
    singularvalues = np.array([])

    latent_brain = np.array([])

    latent_bhv_dsgn = np.array([])
    correlation_crossblock = np.array([])

    def __init__(self, X, Y, C = None):

        if C is None:
            C_d1 = 0
        elif len(C.shape)< 2:
                C_d1 = 1
        else:
                C_d1 = C.shape[1]
###################### C no. of columns 0##############################################################################################
        if C is None or len(C) == 0 :


            X_d0 = X.shape[0]

            if len(X.shape)< 2:
                X_d1 = 1
            else:
                X_d1 = X.shape[1]
            Y_d0 = Y.shape[0]

            if len(Y.shape) < 2:
                Y_d1 = 1
            else:
                Y_d1 = Y.shape[1]




            if X_d0 == Y_d0:

                X1 = np.empty((X_d0, X_d1))
                Y1 = np.empty((Y_d0, Y_d1))

                X_dmean = np.empty((X_d0, X_d1))
                Y_dmean = np.empty((Y_d0, Y_d1))


                X_dmean = X - np.dot(np.ones((X_d0,1)), np.mean(X, axis= 0).reshape((1,X_d1)))
                Y_dmean = Y - np.dot(np.ones((Y_d0,1)), np.mean(Y, axis= 0).reshape((1,Y_d1)))

                if np.sum(np.linalg.norm(X_dmean) == 0)== 0 and np.sum(np.linalg.norm(Y_dmean) == 0)== 0:
                    X1 = X_dmean / np.linalg.norm(X_dmean)
                    Y1 = Y_dmean / np.linalg.norm(Y_dmean)

                    R = np.dot(Y1.T, X1)

                    U, s, V = np.linalg.svd(R)

                    self.brain = X1
                    self.bhv_dsgn = Y1
                    self.saliencs_bhv_dsgn = U
                    self.saliences_brain = V
                    self.singularvalues = s

                    self.latent_brain = np.dot(X1, V)

                    self.latent_bhv_dsgn = np.dot(Y1, U)
                else:
                    self.index_norm = 1
                    return



            else:
                print('Initialization failed: matrices not match')
                return

######################################################################################################################################################################

        elif C_d1 == 1:

            X_d0 = X.shape[0]

            if len(X.shape)< 2:
                X_d1 = 1
            else:
                X_d1 = X.shape[1]
            Y_d0 = Y.shape[0]

            if len(Y.shape) < 2:
                Y_d1 = 1
            else:
                Y_d1 = Y.shape[1]

            C_d = C.shape[0]


            if X_d0 == Y_d0 and Y_d0 == C_d:


            ### generate empty variables otherwise they share the same memory
                X1 = np.empty((X.shape[0], X.shape[1]))
                Y1 = np.empty((Y.shape[0], Y.shape[1]))

                cond_lst = set_order(C)


                ind_X = np.array(range(X.shape[0]))
                print(ind_X)


                for con_i in range(len(cond_lst)):



                    tmp_Y = Y[ind_X[C == cond_lst[con_i]],:]

                    tmp_Y_dmean = tmp_Y - np.dot(np.ones((tmp_Y.shape[0],1)), np.mean(tmp_Y, axis= 0).reshape((1,tmp_Y.shape[1])))




                    tmp_X = X[ind_X[C == cond_lst[con_i]],:]

                    tmp_X_dmean = tmp_X - np.dot(np.ones((tmp_X.shape[0],1)), np.mean(tmp_X, axis= 0).reshape((1,tmp_X.shape[1])))

                    #print(np.linalg.norm(tmp_X_dmean, axis=0)==0)
                    if np.sum(np.linalg.norm(tmp_X_dmean, axis=0)==0)==0 and np.sum(np.linalg.norm(tmp_Y_dmean, axis=0)==0)==0:
                        tmp_X_n = tmp_X_dmean/np.linalg.norm(tmp_X_dmean, axis=0)

                        X1[ind_X[C == cond_lst[con_i]],:] = tmp_X_n

                        tmp_Y_n = tmp_Y_dmean/np.linalg.norm(tmp_Y_dmean, axis=0)


                        Y1[ind_X[C == cond_lst[con_i]],:] = tmp_Y_n
                    else:
                        self.index_norm = 1
                        return
                print(ind_X)
                self.brain = X1
                self.bhv_dsgn = Y1
                self.cnd_indx = C





                #print(cond_lst)
                R = np.zeros((len(cond_lst)*Y_d1, X_d1))
                #print('R')
                #print(R.shape)
                for i in range(len(cond_lst)):
                    R[i*Y_d1:(i+1)*Y_d1,:]= np.dot(self.bhv_dsgn[C == cond_lst[i],:].T, self.brain[C == cond_lst[i],:])

                self.correlation_crossblock = R


                U, s, V = np.linalg.svd(R, full_matrices=False)

                self.saliencs_bhv_dsgn = U
                self.saliences_brain = V.T
                self.singularvalues = s

                self.latent_brain = np.dot(self.brain, V.T)
                latent_bhv_dsgn = np.zeros((Y_d0, U.shape[1]))
                for i in range(len(cond_lst)):
                    latent_bhv_dsgn[C == cond_lst[i],:] = np.dot(self.bhv_dsgn[C == cond_lst[i],:], U[i*Y_d1:(i+1)*Y_d1,:])


                self.latent_bhv_dsgn = latent_bhv_dsgn

            else:
                print('Initialization failed: matrices not match')
                return





        else:
            print("The max of column number should be 2")



















def set_order(seq, idfun=None):
    ### order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for i in range(len(seq)):
        marker = idfun(seq[i])
        if marker in seen: continue
        seen[marker] = 1
        result.append(seq[i])
    return result