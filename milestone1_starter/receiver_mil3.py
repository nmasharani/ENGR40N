import numpy
import math
import operator
import random
import scipy.cluster.vq
import common_txrx as common

def detect_threshold(demod_samples): 
        # Now, we have a bunch of values that, for on-off keying, are
        # either near amplitude 0 or near a positive amplitude
        # (corresp. to bit "1").  Because we don't know the balance of
        # zeroes and ones in the input, we use 2-means clustering to
        # determine the "1" and "0" clusters.  In practice, some
        # systems use a random scrambler to XOR the input to balance
        # the zeroes and ones. We have decided to avoid that degree of
        # complexity in audiocom (for the time being, anyway).

	# initialization
  center1 = min(demod_samples)
  center2 = max(demod_samples) 

  # limit the number of iterations
  iterations = 10
  error = 0.05

  # insert code to implement 2-means clustering 	
  for i in range(0, iterations):
    cluster1 = list([])
    cluster2 = list([])
    for s in demod_samples:
      if abs(s - center1) < abs(s - center2):
        cluster1.append(s)
      else:
        cluster2.append(s)
    new_center1 = numpy.average(numpy.array(cluster1))
    new_center2 = numpy.average(numpy.array(cluster2))

    #if new_center1 == center1 or new_center2 == center2:
    if abs(center1 - new_center1)/new_center1 < error or abs(center2 - new_center2)/new_center2 < error:
      center1 = new_center1
      center2 = new_center2
      break

    center1 = new_center1
    center2 = new_center2

  # insert code to associate the higher of the two centers 
  # with one and the lower with zero

  if (center1 < center2):
    one = center2
    zero = center1
  else:
    one = center1
    zero = center2
  
  print "Threshold for 1: " + str(one)
  print "Threshold for 0: " + str(zero)

  # insert code to compute thresh
  thresh = (one + zero) / 2.0

  return one, zero, thresh

    
