from source import Source
from sink import Sink
import common_srcsink



src = Source(0, "testfiles/A.txt")


src_payload, src_databits = src.process()

sink = Sink()

recd_bits = sink.process(src_databits)
a = [1,0,0,1]
b = [0,1,1,0]

one, two = common_srcsink.hamming(a, b)
print one
print two
