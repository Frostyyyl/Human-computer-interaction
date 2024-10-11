import matplotlib.pyplot as plot
import csv

with open('2cel-rs.csv') as csvfile: 
    data_reader = csv.reader(csvfile, delimiter = ',')
    x = next(data_reader)
    for row in data_reader:
       avg = sum(list(map(float, row[2:]))) / len(list(map(float, row[2:])))
       print("Gry: " + row[0] 
             + "\tPokolenie: " + row[1]
             + "\tSrednia: " + str(avg))

with open('2cel.csv') as csvfile: 
    data_reader = csv.reader(csvfile, delimiter = ',')
    x = next(data_reader)
    for row in data_reader:
       avg = sum(list(map(float, row[2:]))) / len(list(map(float, row[2:])))
       print("Gry: " + row[0] 
             + "\tPokolenie: " + row[1]
             + "\tSrednia: " + str(avg))

with open('cel-rs.csv') as csvfile: 
    data_reader = csv.reader(csvfile, delimiter = ',')
    x = next(data_reader)
    for row in data_reader:
       avg = sum(list(map(float, row[2:]))) / len(list(map(float, row[2:])))
       print("Gry: " + row[0] 
             + "\tPokolenie: " + row[1]
             + "\tSrednia: " + str(avg))

with open('cel.csv') as csvfile: 
    data_reader = csv.reader(csvfile, delimiter = ',')
    x = next(data_reader)
    for row in data_reader:
       avg = sum(list(map(float, row[2:]))) / len(list(map(float, row[2:])))
       print("Gry: " + row[0] 
             + "\tPokolenie: " + row[1]
             + "\tSrednia: " + str(avg))

with open('rsel.csv') as csvfile: 
    data_reader = csv.reader(csvfile, delimiter = ',')
    x = next(data_reader)
    for row in data_reader:
       avg = sum(list(map(float, row[2:]))) / len(list(map(float, row[2:])))
       print("Gry: " + row[0] 
             + "\tPokolenie: " + row[1]
             + "\tSrednia: " + str(avg))
