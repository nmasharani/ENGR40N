from source import Source
from sink import Sink


#src = Source(20, None)

#src_payload, src_databits = src.process()

sink = Sink()


send_bits = [1,0,0,0,0,0,0,0,1,1,1]
recd_bits = sink.process(send_bits)

