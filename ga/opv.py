#!/usr/bin/env python

import numpy as np
import re

class opv(object):  
    def __init__(self,in_str):  
        vec_find = re.compile('e[0-9]')
        self.dim = max(int(vec[1]) for vec in vec_find.findall(in_str))
        in_check = re.compile('^(-?([0-9]*\.[0-9]*|[0-9]*)?e?[1-%d]?\^)*-?([0-9]*\.[0-9]*|[0-9]*)?e?[1-%d]?$|^-?([0-9]*\.[0-9]*|[0-9]*)?e?[1-%d]?$'%(self.dim,self.dim,self.dim))                           
        assert(in_check.match(in_str).span()[1] == len(in_str))

        in_str = in_str.replace('-e','-1e')
        in_str = re.sub('^e','1e',in_str)
        in_str = re.sub(r'\^e',r'^1e',in_str)
        
        vec_list = in_str.split('^')
        print("You input",in_str)

        #Extract grade-0 vectors
        self.coeff = 1
        new_vec_list = []
        try:
            for i,vec in enumerate(vec_list):
                if 'e' not in vec:
                    self.coeff *= float(vec)
                else:
                    new_vec_list.append(vec)
            vec_list = new_vec_list
        except ValueError:
            raise ValueError("Invalid vector: "+str(vec))

        self.vec_bin,self.coeff = self.get_vecbin(vec_list,self.coeff)
        self.num_shifts = 0
        if self.coeff != 0:
            more_coeff,self.num_shifts = self.op_standardize(vec_list,self.dim)
            self.coeff *= more_coeff
            self.vectors = self.get_binvec(self.vec_bin)
        else:
            self.vectors = []

        print("Created "+str(self.vectors)+" with a coefficient of "+str(self.coeff)+'.')
        print("number of shifts= ",self.num_shifts)


    def get_coeff(self,vec_list):
        return np.product([float(vec[:-2]) if 'e' in vec else float(vec) for vec in vec_list])

    def get_vecbin(self,vec_list,coeff):
        #Need to correct order problem.  e1^e2 != e2^e1
        vec_bin = 0
        for vec in vec_list:
            vec_split = vec.split('e')
            if len(vec_split) > 1:
                temp_num = 2**int(vec_split[1])
                if vec_bin&temp_num == temp_num:
                    coeff = 0
                    vec_bin = 0
                    break
                else:
                    vec_bin += temp_num
        return vec_bin,coeff

    def get_binvec(self,vec_bin):   
        vectors = []
        for i,val in enumerate(reversed(bin(vec_bin)[2:])):
            if int(val) == 1:
                vectors.append('e'+str(i))
        return vectors

    def op_standardize(self,in_list,dim):
        coeff_list = []
        vec_list = []
        shift_total = 0
        normalization = 0

        #Extract attached grade-0 vectors and
        # Create int only vector list
        for i,vec in enumerate(in_list):
            split_vec = vec.split('e')
            if len(split_vec) < 1:
                raise ValueError("List length error on ",split_vec)
            vnum = int(split_vec[1])
            vec_list.append(vnum)
            coeff_list.append(float(split_vec[0]))

        for i,vec_num in enumerate(vec_list):
            #Compensate if it is shorter than pseudoscalar length
            if vec_num >= len(in_list):
                vec_num = vec_num - (dim-len(in_list))
            
            temp_shift = i+1-vec_num

            new_shift = temp_shift + normalization
            if new_shift > 0:
                break

            if temp_shift < 0:
                normalization -= 1
            shift_total += -new_shift

        coeff = (-1)**shift_total*np.product(coeff_list)
        return coeff,shift_total

if __name__=='__main__':
    w1 = opv('e4^e3^e2^e1')

