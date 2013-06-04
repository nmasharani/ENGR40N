import numpy
import math
import cmath
import operator

# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier 
  of frequency fc, sampled at samplerate
  '''

  ns = numpy.array(range(0, len(samples)))
  ns = numpy.multiply(2.0 * math.pi * fc / samplerate, ns)

  mod_samples = numpy.multiply(samples, numpy.cos(ns))

  return mod_samples


def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  cutoff_freq = math.pi * fc / samplerate

  demod_samples =  lpfilter(samples, cutoff_freq)

  return demod_samples


def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  # building the lpf
  L = 50

  lpf = (L * 2 + 1) * [0.0]

  for n in range(-1 * L, L+1):
    if n != 0:
      lpf[n + L] = numpy.sin(omega_cut * n) / (n * math.pi)
    else:
      lpf[n + L] = omega_cut / math.pi


  # This is code that works. It's inconvenient because we're not supposed to use numpy.convolve
  '''
  sample_len = len(samples_in)
  lpf_len = len(lpf)

  to_be_filtered = sample_len * [0.0]

  for n in range(0, sample_len):
    to_be_filtered[n] = samples_in[n] * cmath.exp(complex(0, 2 * omega_cut * n))

  # compute demodulated samples

  demod_samples = numpy.convolve(to_be_filtered, lpf)
  '''

  # compute demodulated samples

  demod_samples = convolve(numpy.array(samples_in), numpy.array(lpf), omega_cut)

  demod_samples_mag = [abs(x) for x in demod_samples]

  return numpy.array(demod_samples_mag)

# LUKE THIS IS THE FUNCTION I NEED HELP WITH. Thank you so much. 
# this is a basic convolve function that works. 
# it's super slow and is obviously not good for our purposes.
def convolve(arr1, arr2, omega_cut):
  # the equation we're trying to satisfy is:
  # demod_samples[n] = (received[n]•e^(2j • omega_cut •n)) * lpf[n]
  # so in this function, we must BOTH 
  #   a) multiply the received samples by e^(2j • omega_cut •n) 
  #                                      = cmath.exp(complex(0, 2 * omega_cut * n))
  #      note that this depends on n and therefore must be done in a for loop (can't use numpy.multiply)
  #   b) convolve the multiplied received samples with the low pass filter
  # right now, I'm passing in the received samples as arr1, the lpf as arr2, and omega_cut as itself

  len_arr1 = len(arr1)
  len_arr2 = len(arr2)

  len_result = len_arr1 + len_arr2 - 1

  result = len_result * [0]

  # we have to iterate over n
  for n in range(0, len_result):

    # This calculating the sum is the slow part.
    # What we want is: y[n] = sum over k in range(0, len_arr2) of arr2[k]* arr1[n-k].
    
    # The fastest way to do this is probably to create 
    # two arrays of all values of arr2[k] and arr1[n-k],
    # then take the dot product of those arrays using numpy.dot and then using 
    # numpy.sum to sum over all of those products quickly. 
    
    # What I'm having trouble with is figuring out edge cases. When n-k is out of range,
    # we ideally want to pad with zeros (0.0). But for some reason, I can't wrap my 
    # head around the math to do so. 

    cursum = 0

    for k in range(0, len_arr2):
      if n - k >= 0 and n - k < len_arr1:
        cursum += arr2[k] * arr1[n-k]

    result[n] = cursum

  # return value should be a numpy array for best results
  return numpy.array(result)

  
# this snippet of code shows that the current function is working
'''
arr1 = [0, 1, 0, 1, 0, 1]
arr2 = [1, 1, 0]

print numpy.convolve(arr1, arr2)
print convolve(arr1, arr2, 0)
'''



