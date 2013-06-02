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
                temp = right
                right = left
                left = temp
        if (type(left[1]) == int) and (type(right[1]) != int):
            temp = right
            right = left
            left = temp
        if (left[0] == right[0] and ((type(left[1]) != int) and (type(right[1]) != int))):
            if left[1].node_id > right[1].node_id:
                temp = right
                right = left
                left = temp
            
        super_node = node(left, right, count)
        count = count + 1
        heapq.heappush(pq, (left[0] + right[0], super_node))

    return heapq.heappop(pq)

def walk_tree(curr_node, curr_code, codeword_map):
    if type(curr_node[1]) == int:
        symbol_val = curr_node[1]
        codeword_map[symbol_val] = curr_code
    else:
        left, right = curr_node[1].children()
        walk_tree(left, curr_code + "0", codeword_map)
        walk_tree(right, curr_code + "1", codeword_map)

def build_codeword_map(root_node):
    codeword_map = {}
    begin_string = ""
    walk_tree(root_node, begin_string, codeword_map)
    for key in codeword_map:
        print "key = " + str(key) + " and val = " + str(codeword_map[key])
    return codeword_map
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



#below is commented out code. The code is a replaced version of above with 
#what i think is a cleaner tree node handlng. However, the code does
#not work as well as the above, not sure why that is.

    '''# Nisha Masharani (nisham) and Luke Pappas (lpappas9)

import numpy
import math
import operator
import Queue
import heapq
import copy

class node(object):
    #left = None
    #right = None
    #frequency = 0
    #symbol_val = -1 #-1 to indicate a supernode
    #node_id = 0
    #node_type = 0 #0 for supernode, 1 for leaf node
    def __init__(self, left, right, frequency, symbol_val, curr_id, node_type):
        self.left = left
        self.right = right
        self.frequency = frequency
        self.symbol_val = symbol_val
        self.node_id = curr_id
        self.node_type = node_type
    def children(self):
        return self.left, self.right
    def get_node_frequency(self):
        return self.frequency
    def get_node_symbol_val(self):
        return self.symbol_val
    def get_node_id(self):
        return self.node_id
    def get_node_type(self):
        return self.node_type

def build_huffman_tree(symbol_frequencies_dict):
    pq = list([])
    for key in symbol_frequencies_dict:
        if symbol_frequencies_dict[key] != 0:
            curr = node(None, None, symbol_frequencies_dict[key], key, 0, 1)
            pq.append((curr.get_node_frequency(), curr))

    heapq.heapify(pq) # this now makes pq an ordered list of .
    count = 1 
    while 1:
        if len(pq) == 1:
            break
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        if left[1].get_node_frequency() > right[1].get_node_frequency():
            temp = left
            left = right
            right = temp
        elif (left[1].get_node_frequency() == right[1].get_node_frequency()):
            if (left[1].get_node_type() == 1) and (right[1].get_node_type() == 1):
                if left[1].get_node_symbol_val() > right[1].get_node_symbol_val():
                    temp = left
                    left = right
                    right = temp
            elif (left[1].get_node_type() == 0) and (right[1].get_node_type() == 1):
                temp = left
                left = right
                right = temp
            elif (left[1].get_node_type() == 0) and (right[1].get_node_type() == 0):
                if left[1].get_node_id() > right[1].get_node_id():
                    temp = left
                    left = right
                    right = temp
        supernode = node(left, right, (left[1].get_node_frequency() + right[1].get_node_frequency()), -1, count, 0)
        count = count + 1
        heapq.heappush(pq, (supernode.get_node_frequency, supernode))

    return heapq.heappop(pq)

def walk_tree(curr_node, curr_code, codeword_map):
    if curr_node[1].get_node_type() == 1:
        symbol_val = curr_node[1].get_node_symbol_val()
        codeword_map[symbol_val] = curr_code
        return
    else:
        left, right = curr_node[1].children()
        walk_tree(left, curr_code + "0", codeword_map)
        walk_tree(right, curr_code + "1", codeword_map)

def build_codeword_map(root_node):
    codeword_map = {}
    begin_string = ""
    walk_tree(root_node, begin_string, codeword_map)
    for key in codeword_map:
        print "key = " + str(key) + " and val = " + str(codeword_map[key])
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
    
    return hamming_d, ber'''
