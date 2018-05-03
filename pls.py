import PLSCORE as plsc
import numpy as np

class PLS(plsc.PLSCORE):


    index_permutaion = 0

    index_bootstraps = 0

    def __init__(self, X, Y, C=None, **kwargs):



        self.brain_orig = X
        self.bhv_orig = Y
        self.index = C



        if kwargs is not None:
            col_slct = np.array(kwargs.get("selected columns"))

            row_slct_dic = kwargs.get("selected row")

            row_method = kwargs.get("method")


            if row_method == "subset":
                if len(row_slct_dic.key()) > 1:
                    print("you only can select one index")
                else:
                    for key in row_slct_dic:
                        row_indx = [ i for i in range(X.shape[0]) if C[i,key] in row_slct_dic[key]]
                    X_s = X[row_indx,:]
                    C_s = C[row_indx,col_slct]
                    #for i in range()
                    #C_new










        super(PLS, self).__init__(X, Y, C)


    def getBrainScores(self):
        return np.dot(self.brain_orig, self.saliences_brain)

    def getBhvScores(self):
        Y = self.bhv_orig
        Y_d0 = Y.shape[0]
        Y_d1 = Y.shape[1]
        U = self.saliencs_bhv_dsgn
        bhvScores = np.zeros((Y_d0, U.shape[1]))
        C = self.cnd_indx
        cond_lst = plsc.set_order(C)
        for i in range(len(cond_lst)):
            bhvScores[C == cond_lst[i],:] = np.dot(Y[C == cond_lst[i],:], U[i*Y_d1:(i+1)*Y_d1,:])


        return bhvScores


    def getPermutation(self, num=1000, nonrotated=None):
        if self.index_permutaion == 0:


            #print(ind_X.shape)
            sv_len = len(self.singularvalues)

            X = self.brain_orig
            Y = self.bhv_orig
            C = self.cnd_indx
            X_new = np.empty((X.shape[0],X.shape[1]))


            svTotal = np.empty((num, sv_len))
            cond_lst = plsc.set_order(C)
            cnt_per = 0
            while cnt_per < num:
                ind_X = np.array(range(self.brain.shape[0]))
                #print(ind_X)


                for con_i in range(len(cond_lst)):
                    ind_tmp = ind_X[C == cond_lst[con_i]]
                    #print(ind_tmp)
                    np.random.shuffle(ind_tmp)
                    ind_X[C == cond_lst[con_i]] = ind_tmp
                    #print(ind_tmp)

                #print(ind_X.shape)
                #print(C.shape)
                X_new = X[ind_X,:]
                #C_new = C[ind_X,]

                #print(X_new.shape)
                temp = plsc.PLSCORE(X_new, Y, C)
                #print(ind_X)
                #print(temp.index_norm)
                if temp.index_norm == 0:

                    if nonrotated is None or nonrotated.lower() == "no" :
                        svTotal[cnt_per,:] = temp.singularvalues
                    else:
                        procrustes = np.dot(self.saliencs_bhv_dsgn.T, temp.saliencs_bhv_dsgn)
                        svTotal[cnt_per,:] = np.diag(np.dot(procrustes.T, np.dot(np.diag(temp.singularvalues), procrustes)))
                    #print(np.dot(procrust.T, np.dot(np.diag(temp.getSingularvalues()), procrust)))
                    cnt_per += 1
            svTotal_1d = svTotal.T.ravel(order = 'K')

            dict_sv = {}
            for i in range(sv_len):
                dict_sv[self.singularvalues[i]] = np.float(len(svTotal_1d[svTotal_1d <= self.singularvalues[i]]))/num/sv_len

            self.sv_dist = svTotal_1d
            self.sv_p = dict_sv

            self.index_permutaion = 1

            return self.sv_p


        else:
            print('You have run permutation test')









    def getBootstraps(self, num=1000, nonrotated = None):

        if self.index_bootstraps == 0:




            X = self.brain_orig
            Y = self.bhv_orig
            C = self.cnd_indx

            X_new = np.empty((X.shape[0],X.shape[1]))
            Y_new = np.empty((Y.shape[0],Y.shape[1]))

            saliencesBrain = self.saliences_brain
            saliencesBhv = self.saliencs_bhv_dsgn

            saliencesBrain_total= np.empty((saliencesBrain.shape[0], saliencesBrain.shape[1], num))
            saliencesBhv_total= np.empty((saliencesBhv.shape[0], saliencesBhv.shape[1], num))

            cond_lst = plsc.set_order(C)

            cnt_boot = 0
            while cnt_boot < num:
                ind_X = np.array(range(self.brain.shape[0]))

                for con_i in range(len(cond_lst)):
                    ind_tmp = ind_X[C == cond_lst[con_i]]
                    #print(ind_tmp)
                    ind_new = np.random.randint(len(ind_tmp),size=len(ind_tmp))
                    #print(ind_tmp[ind_new])
                    ind_X[C == cond_lst[con_i]] = ind_tmp[ind_new]

                #print(ind_X.shape)
                #print(C.shape)

                X_new = X[ind_X,:]
                Y_new = Y[ind_X,:]


                #print(X_new.shape)
                temp = plsc.PLSCORE(X_new, Y_new, C)
                #print(temp.index_norm)
                if temp.index_norm == 0:
                    if nonrotated is None or nonrotated.lower() == 'no':
                        saliencesBrain_total[:,:, cnt_boot] = temp.saliences_brain
                        saliencesBhv_total[:,:,cnt_boot] = temp.saliencs_bhv_dsgn
                    else:
                        procrustes = np.dot(self.saliencs_bhv_dsgn.T, temp.saliencs_bhv_dsgn)

                        saliencesBrain_total[:,:, cnt_boot] = np.dot(temp.saliences_brain, procrustes)
                        saliencesBhv_total[:,:,cnt_boot] = np.dot(temp.saliencs_bhv_dsgn, procrustes)
                    cnt_boot += 1



            saliencesBrain_std = np.std(saliencesBrain_total, axis=2)
            saliencesBhv_std = np.std(saliencesBhv_total, axis=2)

            #print(saliencesBhv_std.shape)
            #print(saliencesBrain_std.shape)

            self.saliencesBrain_std = saliencesBrain_std
            self.saliencesBhv_std = saliencesBhv_std


            self.index_bootstraps = 1

        else:
            print('You have run permutation test')


    def getBrainMtrx(self):
        return self.brain

    def getBhv_dsgnMrtx(self):
        return self.bhv_dsgn

    def getSaliencesBrain(self):
        return self.saliences_brain

    def getSaliencesBhv_dsgn(self):
        return self.saliencs_bhv_dsgn

    def getLatentBrain(self):
        return self.latent_brain

    def getLatentBhv_dsgn(self):
        return self.latent_bhv_dsgn

    def getSingularvalues(self):
        return self.singularvalues

    def getCorrelation(self):
        return self.correlation_crossblock

    def getSV_dist(self):
        if self.index_permutaion == 1:
            return self.sv_dist
        else:
            return 'no run permutation test'

    def getSV_p(self):
        if self.index_permutaion == 1:
            return self.sv_p
        else:
            return 'no run permutation test'


    def getSaliencesBrain_std(self):
        if self.index_bootstraps == 1:
            return self.saliencesBrian_std
        else:
            return 'no run bootstraps'

    def getSaliencesBhv_std(self):
        if self.index_bootstraps == 1:
            return self.salencesBhv_std
        else:
            return 'no run bootstraps'

    def getSaliencesBhv_stability(self):
        if self.index_bootstraps == 1:
            return self.saliencs_bhv_dsgn/self.salencesBhv_std
        else:
            return 'no run bootstraps'

    def getSaliencesBrain_stability(self):
        if self.index_bootstraps == 1:
            return self.saliences_brain/self.saliencesBrain_std
        else:
            return 'no run bootstraps'
