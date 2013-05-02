from source import Source
from sink import Sink
import common_srcsink
from transmitter import Transmitter


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
xmitter = Transmitter(1, 1, 5.0, 1 ,1)

preambleadded = xmitter.add_preamble([0,0,0,0,0])

print preambleadded

samples = xmitter.bits_to_samples(preambleadded)

print samples