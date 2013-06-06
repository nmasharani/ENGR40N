
Modulation: Used numpy functions to multiply samples by cosine at carrier frequency
Demodulation: Used 2-means clustering to find threshhold 
(as seen in http://www.cs.utahedu/~piyush/teaching/4-10-print.pdf). 
Used quadrature demodulation as described in the writeup. Wrote a separate convolution
function to use in demodulation; used numpy functions for speed. Built LPF as described
in the writeup.