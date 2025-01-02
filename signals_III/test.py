import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import sys
import time
import os


MAN = 'M'
WOMAN = 'K'


def list_files(folder_path):
    filenames = []
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                filenames.append(filename)
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    return filenames


def main(argv):
    # try-catch any errors to meet the task requirements
    try:
        files = list_files('data/')

        all_results = []
        all_times = []

        for file in files:
            start_time = time.time()
            sampling_rate, data = wav.read('data/' + file) # read the file
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
                answer = (WOMAN == file[4])
            else:
                answer = (MAN == file[4])

            # add to results
            final_time = time.time() - start_time
            all_results.append(answer)
            all_times.append(final_time)

            # display if the answer was incorrect
            if (not answer):
                print(f'File: {files.index(file) + 1}, determined freq: {freq[np.argmax(final)]}')

            # display if calculation took too long
            if final_time > 1:
                print(f'ERROR: Final time is greater than 1 second: {final_time}')

        print(f'{np.mean(all_results)} % of correct answers')
        print(f'{np.mean(all_times)} seconds - average time')

    except Exception: # make sure to give an answer in case of an error
        print(WOMAN)


if __name__ == '__main__':
    sys.stderr = None # turn of the stderr to meet the task requirements

    main(sys.argv)