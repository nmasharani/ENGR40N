import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
    
    lenS1 = len(s1)
    hamming_d = 0
    ber = 0
    lenS2 = len(s2)
    count = 0
    if (lenS1 < lenS2):
        s1 = s1[0:(lenS1)]
        s2 = s2[0:(lenS1)]
        count = lenS1
    else:
        s1 = s1[0:(lenS2)]
        s2 = s2[0:(lenS2)]
        count = lenS2
    
    for i in range(0, count):
        if s1[i] != s2[i]:
            hamming_d += 1
    
    ber = hamming_d / count
    
    return hamming_d, ber
