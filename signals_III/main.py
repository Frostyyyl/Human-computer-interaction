import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import sys
import time
import os


MAN = 'M'
WOMAN = 'K'


def main(argv):

    try:
        sampling_rate, data = wav.read(argv)
        sampling_interval = 1 / sampling_rate
        n = len(data)

        if data.ndim > 1:
            signal = data[:, 0]
        else:
            signal = data

        domain = np.abs(np.fft.fft(signal) * 2 / n)[:n // 2]
        domain[:240] = 0
        freq = np.fft.fftfreq(n, sampling_interval)[:n // 2]
        
        fig = plt.figure(figsize=(8, 6)) # NOTE
        ax = fig.add_subplot(611) # NOTE
        ax.plot(freq[:n // 64], domain[:n // 64], linewidth=0.5) # NOTE
        ax.xaxis.set_minor_locator(AutoMinorLocator(5)) # NOTE
        ax.yaxis.set_minor_locator(AutoMinorLocator(5)) # NOTE

        final = domain

        for i in range(2, 5):
            shifted_domain = sig.decimate(domain, i)
            tmp = np.concatenate((shifted_domain, final[len(shifted_domain):]))
            final = np.concatenate((shifted_domain * final[:len(shifted_domain)], final[len(shifted_domain):]))

            ax = fig.add_subplot(610 + i) # NOTE
            ax.plot(freq[:n // 64], tmp[:n // 64], linewidth=0.5) # NOTE
            ax.set_ylabel(str(i)) # NOTE
            ax.xaxis.set_minor_locator(AutoMinorLocator(5)) # NOTE
            ax.yaxis.set_minor_locator(AutoMinorLocator(5)) # NOTE

        
        ax = fig.add_subplot(616) # NOTE
        ax.plot(freq[:n // 64], final[:n // 64], linewidth=0.5) # NOTE
        ax.set_ylabel('Final:') # NOTE
        ax.xaxis.set_minor_locator(AutoMinorLocator(5)) # NOTE
        ax.yaxis.set_minor_locator(AutoMinorLocator(5)) # NOTE


        if freq[np.argmax(final)] > 160:
            print(WOMAN)
        else:
            print(MAN)


        print(f'Argmax: {freq[np.argmax(final)]}, Correct answer: {argv[11]}') # NOTE
        plt.show() # NOTE

    except Exception:
        print(WOMAN)


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print(WOMAN)
    else:
        main(sys.argv[1])