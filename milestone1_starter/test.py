from source import Source
from sink import Sink
import common_srcsink
from transmitter import Transmitter
from receiver import Receiver
import numpy
import random


"""
src = Source(0, "testfiles/checkerboard.png")


src_payload, src_databits = src.process()

sink = Sink()

recd_bits = sink.process(src_databits)
a = [1,0,0,1]
b = [0,1,1,0]

one, two = common_srcsink.hamming(a, b)
print one
print two
"""
xmitter = Transmitter(1, 1, 5.0, 4, 1)

preambleadded = xmitter.add_preamble([0,0,0,0,0])

print preambleadded

samples = xmitter.bits_to_samples(preambleadded)

print samples

# carrier_freq, samplerate, spb

rec = Receiver(1, 1, 4)

zeros = numpy.zeros(10)

received = numpy.concatenate((zeros, samples), axis=0)

#received = numpy.zeros(50)
for i in range(0, len(received)):
	if received[i] > 1: 
		received[i] = received[i] - random.uniform(0,2)
	else: 
		received[i] = received[i] + random.uniform(0,2)


print received

print rec.detect_preamble(received, 2.5, 5.0)