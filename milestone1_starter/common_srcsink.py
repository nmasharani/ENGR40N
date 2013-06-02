# Nisha Masharani (nisham) and Luke Pappas (lpappas9)

import numpy
import math
import operator
import Queue
import heapq

class node(object):
    left = None
    right = None
    node_id = 0
    def __init__(self, left, right, curr_id):
        self.left = left
        self.right = right
        self.node_id = curr_id
    def children(self):
        return self.left, self.right

def build_huffman_tree(symbol_frequencies_dict):
    pq = list([])
    for key in symbol_frequencies_dict:
        curr = (symbol_frequencies_dict[key], key)
        if symbol_frequencies_dict[key] != 0:
            pq.append(curr)

    heapq.heapify(pq) # this now makes pq an ordered list of (num occurences, symbol value) tuples.
    count = 1 
    while 1:
        if len(pq) == 1:
            break
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        if left[0] > right[0]:
            temp = right
            right = left
            left = temp
        if (left[0] == right[0]) and ((type(left[1]) == int) and (type(right[1]) == int)):
            if left[1] > right[1]:
                temp = left
                left = right
                right = temp
        if (type(left[1]) == int) and (type(right[1]) != int):
            temp = right
            right = left
            left = temp
        if (left[0] == right[0] and ((type(left[1]) != int) and (type(right[1]) != int))):
            if left[1].node_id > right[1].node_id:
                temp = left
                left = right
                right = temp
            
        super_node = node(left, right, count)
        count = count + 1
        heapq.heappush(pq, (left[0] + right[0], super_node))

    return heapq.heappop(pq)

def walk_tree(curr_node, curr_code, codeword_map):
    if type(curr_node[1]) == int:
        symbol_val = curr_node[1]
        print symbol_val
        codeword_map[symbol_val] = curr_code
    else:
        left, right = curr_node[1].children()
        walk_tree(left, curr_code + "0", codeword_map)
        walk_tree(right, curr_code + "1", codeword_map)

def build_codeword_map(root_node):
    codeword_map = {}
    begin_string = ""
    walk_tree(root_node, begin_string, codeword_map)
    return codeword_map


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
    
    ber = hamming_d * 1.0 / (count * 1.0)
    
    return hamming_d, ber
