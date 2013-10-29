#!/usr/bin/env python

import numpy
import matplotlib.pyplot as plt

amr_file_path = "./_output/fort.amr"
search_key = "total mass ="

amr_file = open(amr_file_path, 'r')
time = []
total_mass = []
mass_diff = []
for line in amr_file:
    if search_key in line:
        split_line = line.split()

        # Extract line info
        time.append(float(split_line[3][:-1]))
        total_mass.append(float(split_line[7]))
        mass_diff.append(float(split_line[10]))

amr_file.close()

# Change to numpy arrays
t = numpy.array(time)
days = t / (24.0 * 3600.0)
mass = numpy.array(total_mass)
diff = numpy.array(mass_diff)
print "Percent increase over start: ", 100.0 * (numpy.max(mass) - mass[0]) / mass[0]

# Plot
fig, axes = plt.subplots(1,1)
axes.plot(days, mass - mass[0])

fig, axes = plt.subplots(1,1)
axes.plot(days, diff)

plt.show()
