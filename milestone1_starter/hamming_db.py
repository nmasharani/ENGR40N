import numpy
import math
import operator
import common_txrx_mil3
import binascii
import sys

#generating_matrices is an array of numpy arrays. 
generating_matrices = [numpy.array([1, 1, 1]),
                       numpy.array([1,    1,    0,    1,    0,    0,    0,
                                    0,    1,    1,    0,    1,    0,    0,
                                    1,    1,    1,    0,    0,    1,    0,
                                    1,    0,    1,    0,    0,    0,    1]),
                       numpy.array([1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                    0,     1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                    0,     0,     1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,
                                    1,     1,     0,     1,     0,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,
                                    1,     0,     1,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,     0,     0,
                                    0,     1,     0,     1,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,     0,
                                    1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,
                                    0,     1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,     0,
                                    1,     1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,
                                    1,     0,     1,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1,     0,
                                    1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1]),
                       numpy.array([ 1,    0,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                     0,    1,    0,    1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                     0,    0,    1,    0,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    1,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    0,    1,    1,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    0,    0,    1,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,
                                     1,    0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,
                                     1,    1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,
                                     1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,
                                     0,    1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,
                                     1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,
                                     0,    1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1])]
# paramaters in the form [n,k] 
# where n is the length of the codeword (databits + parity bits),
# and k is the length of the databits
parameters = [[3,1],[7,4],[15,11],[31,26]]


def gen_lookup(cc_len):
    ''' 
    returns
    (1) n (=cc_len, codeword length)
    (2) k (length of data bit in each codeword)
    (3) index (index of the corresponding code in the above lookup table)
    (4) generater matrix
    for Hamming code with n = cc_len
    '''
    if cc_len == 3:
        index = 0
    elif cc_len == 7:
        index = 1
    elif cc_len == 15:
        index = 2
    elif cc_len == 31:
        index = 3
    else:
        print '\tNo Hamming code with n =', cc_len
        sys.exit(1)

    n = parameters[index][0]
    k = parameters[index][1]
    
    # Reshape G:
    # k = num rows
    # n = num columns

    

    return n, k, index, reshape(index, n, k)

def reshape(index, n, k):
    gen_matrix = [generating_matrices[index][i * n: i * n + n] for i in range(0, k)]
    G = [numpy.concatenate((gen_matrix[i][n-k:n], gen_matrix[i][0:n-k]), axis=0) for i in range(0, k)]
    return numpy.array(G)


def parity_lookup(index):
    '''
    returns the
    (1) n (=cc_len, codeword length)
    (2) k (length of data bit in each codeword)
    (3) index (index of the corresponding code in the above lookup table)
    (4) parity check matrix
    matched by the lookup table above given the index
    The reason why this takes the index as the input while gen_lookup takes cc_len
    is, because containing index is efficient than containing n in the header.
    The decoder reads the header to pick the right parity check matrix.
    ''' 
    n = parameters[index][0]
    k = parameters[index][1]
    
    # Reshape G, extract A and compute H:

    G = reshape(index, n, k)

    A = [G[i][k:n] for i in range(0,k)]
    AT = numpy.transpose(A)

    I = numpy.identity(n-k, dtype=int)


    H = [numpy.concatenate((AT[i], I[i]), axis=0) for i in range(0,n-k)]

    return n, k, numpy.array(H)

    

