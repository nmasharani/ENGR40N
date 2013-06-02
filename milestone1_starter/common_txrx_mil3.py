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

  for n in range(-L, L+1):
    if n != 0:
      lpf[n + L] = numpy.sin(omega_cut * n) / (n * math.pi)
    else:
      lpf[n + L] = omega_cut / math.pi

  sample_len = len(samples_in)
  lpf_len = len(lpf)

  to_be_filtered = sample_len * [0.0]

  for n in range(0, sample_len):
    to_be_filtered[n] = samples_in[n] * cmath.exp(complex(0, 2 * omega_cut * n))

  # compute demodulated samples

  demod_samples = numpy.convolve(to_be_filtered, lpf)

  '''
  for n in range(0, sample_len-lpf_len):
    convolve_sum = numpy.dot(to_be_filtered[n:n + lpf_len], lpf[::-1])
    demod_samples[n] = convolve_sum
  '''



  '''
  for n in range(0, sample_len):
    convolve_sum = 0.0
    for k in range(n-(lpf_len-1), n):
      if k >= 0:
        convolve_sum += to_be_filtered[k] * lpf[n - k]

    demod_samples[n] = convolve_sum
  '''
  demod_samples_mag = [abs(x) for x in demod_samples]
  return numpy.array(demod_samples_mag)
