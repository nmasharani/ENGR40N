from source import Source
from sink import Sink


src = Source(0, "testfiles/32pix.png")

src_payload, src_databits = src.process()

sink = Sink()


recd_bits = sink.process(src_databits)

