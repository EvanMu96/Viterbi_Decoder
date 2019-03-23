# util functions of HMM

# read example.hmm file which is the configuration of Hidden Markov Model
# return data type dict
import re
import numpy as np
def read_cfg(file_path):
    print("reading configuration files")
    f = open(file_path, 'r')
    lines = f.readlines()
    cfg_dict = dict()
    line1 = lines[0].split(' ')
    cfg_dict['state_num'] = int(line1[0])
    cfg_dict['obn_num'] = int(line1[1])
    cfg_dict['pi'] = np.array([float(i) for i in lines[1].split(' ')])
    temp1, temp2 = [], []
    temp1.append(re.split('\s+', lines[2])[0:2])
    temp1.append(re.split('\s+', lines[2])[2:-1])
    temp2.append(re.split('\s+', lines[3])[0:2])
    temp2.append(re.split('\s+', lines[3])[2:-1])
    #print(temp1)
    #print(temp2)
    A1 = np.array([float('0'+i) for i in temp1[0]])
    A2 = np.array([float('0'+i) for i in temp2[0]])
    B1 = np.array([float('0'+i) for i in temp1[1]])
    B2 = np.array([float('0'+i) for i in temp2[1]])
    #print(A1.shape, A2.shape, B1.shape, B2.shape)
    cfg_dict['A'] = np.stack((A1, A2))
    cfg_dict['B'] = np.stack((B1, B2))
    return cfg_dict

# read genome series file
# return data type list
def read_series(file_path):
    print("reading series file")
    f = open(file_path, 'r')
    lines = f.readlines()
    lines = list(''.join([line.rstrip('\n').upper() for line in lines[1:]]))
    number_series = []
    for i in range(len(lines)):
        if lines[i] == 'A':
            number_series.append(0)
        elif lines[i] == 'C':
            number_series.append(1)
        elif lines[i] == 'G':
            number_series.append(2)
        elif lines[i] == 'T':
            number_series.append(3)
    return number_series

# write status list into a file
def write_result(status_list):
    f = open('result.txt', 'w')
    start_point = 1
    lines = []
    num = 0
    for i in range(len(status_list)-1):
        if status_list[i] != status_list[i+1]:
            lines.append("{} to {} is status {}\n".format(start_point, i+1, status_list[i]))
            start_point = i+2
            if status_list[i] == 'B':
                num += 1    
        if i == len(status_list)-2:
            lines.append("{} to {} is status {}\n".format(start_point, 1000000, status_list[i]))
            if status_list[i] == 'B':
                num += 1 

    f.writelines(lines)
    print('the reuslts are writen into ./result.txt')
    return num
            


if __name__ == "__main__":
    # unit test
    print(read_cfg('example.hmm'))
    #print(read_series('example.fa')[0:11]) # print the first ten data points
