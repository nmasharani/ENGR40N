import numpy
import math
import operator
import common_txrx_mil3
import binascii
# Methods common to both the transmitter and receiver

'''
These functions are for modulation and demodulation
(which is currently presented as a black box)
No need to touch them
'''
def modulate (fc, samplerate, samples):
   return common_txrx_mil3.modulate(fc, samplerate, samples) 

def demodulate (fc, samplerate, samples):
   return common_txrx_mil3.demodulate(fc, samplerate, samples)

################
'''
If you need any functions that 
you need commonly in both transmitter and receiver,
implement here
'''
def get_Preamble_Samples (spb, preamble, one):
	preamble_samples = list([])

	for bit in preamble:
		if bit == 1:
			for i in range(0, spb):
				preamble_samples.append(one)
		else:
			for i in range(0,spb):
				preamble_samples.append(0.0)

	return numpy.array(preamble_samples)


def get_Preamble ():
	preamble = [1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,
   1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0]
	return preamble

# get preamble bits
# get preamble samples