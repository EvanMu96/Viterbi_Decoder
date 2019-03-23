import numpy as np
import sys
from utils import read_cfg, read_series, write_result

class Bin_Viterbi:
    def __init__(self, states_num, observations_num, A, B, pi):
        self.state_num = states_num
        self.observation_num = observations_num
        self.A = A
        self.B = B
        self.pi = pi

    # Viterbi decoder
    def decode(self, series):
        dp_list = np.zeros((len(series), self.state_num))   # initialize a table to use dynamic programming
        psi_list = np.zeros((len(series)-1, self.state_num), dtype=np.int64) # memorize the best step from the second state
        # initialize first two state
        # notice that to avoid underflow I used log2 space
        dp_list[0,0] = np.log2(self.pi[0])+np.log2(self.B[0, series[0]])
        dp_list[0,1] = np.log2(self.pi[1])+np.log2(self.B[1, series[0]])
        # traverse the series data
        for i in range(1, len(series)):
            ob = series[i]
            # fill two state's probabilities
            for j in range(self.state_num):
                temp = np.array([dp_list[i-1, 0]+np.log2(self.A[j,0]), dp_list[i-1, 1]+np.log2(self.A[j,1])])
                dp_list[i, j] = np.max(temp)+np.log2(self.B[j, ob])
                # record the best last step
                psi_list[i-1, j] = np.argmax(temp)
        predict_list = []
        # find the final state
        cur = np.argmax(dp_list[len(series)-1, :])
        predict_list.append(cur)
        # backtrack the best steps
        for i in range(len(series)-2, -1, -1):
            #print(type(i), type(cur))
            #print(cur)
            if psi_list[i, cur]==0:
                C = 'A'
            elif psi_list[i, cur]==1:
                C = 'B'
            else:
                raise UserWarning()
            predict_list.append(C)
            cur = psi_list[i, cur]
        return predict_list[::-1] # reverse the status list. the first data should be no.1
            

if __name__ == "__main__":
    print('program start')
    hmm_path = sys.argv[1]
    fa_path = sys.argv[2]
    cfg_dict = read_cfg(hmm_path)
    series = read_series(fa_path)
    #print(len(series))
    model = Bin_Viterbi(cfg_dict['state_num'], cfg_dict['obn_num'], cfg_dict['A'], cfg_dict['B'], cfg_dict['pi'])
    status_series = model.decode(series)
    num = write_result(status_series)
    print("The total number of B state segment is {}".format(num))
    print("The detail result has been writen into the file result.txt")
    #print(opt_mat.shape)


            

