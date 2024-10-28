import numpy as np
import pandas as pd

def read_data(file_path) -> tuple[pd.DataFrame, pd.DataFrame]: # pandas
    header = pd.read_csv(file_path, nrows=1, header=None, sep=r'\s+')
    data_reader = pd.read_csv(file_path, skiprows=1, header=None, sep=r'\s+')

    return header, data_reader
    
    # for (i, j), v in data.stack().items(): # pandas
    # for (i, j), v in np.ndenumerate(data): # numpy
    
    # params[0] - numpy
    # params.loc[0, 0] - pandas

def read_data(file_path) -> tuple[np.ndarray, np.ndarray]: # numpy
    with open(file_path, 'r') as file:
        # read the first line
        header = np.fromstring(file.readline().strip(), sep=' ')

        # read the rest of the file
        data = np.loadtxt(file)

        return header, data


h, d = read_data('color_visualization/data/big.dem')

a = np.arange(6).reshape(2, 3)


data = np.zeros((3, 3))

for (x, y), v in np.ndenumerate(data):
    data[x, y] = x

print(a)