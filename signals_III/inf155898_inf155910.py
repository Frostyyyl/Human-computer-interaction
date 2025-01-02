import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import sys


MAN = 'M'
WOMAN = 'K'


def main(argv):
    """
    Program designed to determine gender of a person based on their voice

    Autors:
    - 155898
    - 155910
    """

    # try-catch any errors to meet the task requirements
    try:
        sampling_rate, data = wav.read(argv[1]) # read the file passed as an argument
        sampling_interval = 1 / sampling_rate
        n = len(data)

        if data.ndim > 1: # pull out the signal depending on number of the channels
            signal = data[:, 0]
        else:
            signal = data
        
        # cut out the symmetric part as its irrelevant
        domain = np.abs(np.fft.fft(signal) * 2 / n)[:n // 2] 
        freq = np.fft.fftfreq(n, sampling_interval)[:n // 2]
        # get rid of y-shift and some noise by
        # zeroing the values below index with value of 80 Hz
        domain[:np.where(freq >= 80)[0][0]] = 0 
        final = domain

        # calculate the harmonic product spectrum
        for i in range(2, 5):
            shifted_domain = sig.decimate(domain, i) # squish the domain by i = [2, 3, 4]
            final = np.concatenate((shifted_domain * final[:len(shifted_domain)], final[len(shifted_domain):]))

        # determine the answer
        if freq[np.argmax(final)] > 160:
            print(WOMAN)
        else:
            print(MAN)

    except Exception: # make sure to give an answer in case of an error
        print(WOMAN)


if __name__ == '__main__':
    sys.stderr = None # turn of the stderr to meet the task requirements

    main(sys.argv)