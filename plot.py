# Some legacy data is stored as .csv files
# New datafiles store one nautilus json object per line instead of csv
# This scipt is mostly obsolete.


import matplotlib.pyplot as plt
import datetime
import csv
import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<datafile.csv>')
    exit()

with open(sys.argv[1], 'rb') as fin:
    data_reader = csv.reader(fin)
    time = []*0
    depth = []*0
    temp = []*0
    for row in data_reader:
        print(row)
        time.append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
        temp.append(row[1])
        depth.append('-' + row[2])
plt.figure(1)
plt.subplot(211)
plt.xlabel('time (UTC)')
plt.ylabel('depth (meters)')
plt.plot(time,depth, marker='.', linestyle='')
plt.subplot(212)
plt.xlabel('time (UTC)')
plt.ylabel('temperature (celsius)')
plt.plot(time,temp, marker='', linestyle='-')
plt.show()
