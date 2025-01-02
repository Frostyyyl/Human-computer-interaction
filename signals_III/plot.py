import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import matplotlib.pyplot as plt
import sys


MAN = 'M'
WOMAN = 'K'


def main(argv):
    sampling_rate, data = wav.read(argv[1])
    sampling_interval = 1 / sampling_rate
    n = len(data)
    t = np.arange(0, n * sampling_interval, sampling_interval) 

    if data.ndim > 1:
        signal = data[:, 0]
    else:
        signal = data
    
    domain = np.abs(np.fft.fft(signal) * 2 / n)[:n // 2]
    freq = np.fft.fftfreq(n, sampling_interval)[:n // 2]
    domain[:np.where(freq >= 80)[0][0]] = 0
    final = domain
    
    fig = plt.figure(figsize=(8, 6))         
    ax = fig.add_subplot(611) 
    ax.plot(t, signal, linewidth=0.5) 
    ax.set_ylabel('Signal')
    ax = fig.add_subplot(612) 
    ax.plot(freq[:n // 64], domain[:n // 64], linewidth=0.5) 
    ax.set_ylabel('Domain')

    for i in range(2, 5):
        shifted_domain = sig.decimate(domain, i)
        tmp = np.concatenate((shifted_domain, final[len(shifted_domain):])) 
        final = np.concatenate((shifted_domain * final[:len(shifted_domain)], final[len(shifted_domain):]))


        ax = fig.add_subplot(611 + i) 
        ax.plot(freq[:n // 64], tmp[:n // 64], linewidth=0.5)
        ax.set_ylabel(str(i))

    ax = fig.add_subplot(616) 
    ax.plot(freq[:n // 64], final[:n // 64], linewidth=0.5) 
    ax.set_ylabel('Final')

    if freq[np.argmax(final)] > 160:
        print(WOMAN)
    else:
        print(MAN)

    print(f'Argmax: {freq[np.argmax(final)]}, Correct answer: {argv[1][11]}') 
    plt.show() 


if __name__ == '__main__':
    main(sys.argv)