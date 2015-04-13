# -*- coding: UTF-8 -*-

# Name:         PowerFlowCalculation.py
# Func:         Change times of input Data to look into the regular pattern, this can be the startup file of this project too.
# Author:       Maples7
# Addr:         EE of SDU, China
# Time:         2015-04-13
# Link:         http://www.cnblogs.com/maples7/

import pylab as pl

result = {}

# Read Data
try:
    fp = open("timesResultComparison.txt", "r+")
    while True:
        try:
            line = fp.readline().split(" ")
            times = float(line[0])
            loopTimes = int(line[1])
            result[times] = []
            for i in range(loopTimes):
                line = fp.readline().split(" ")
                result[times].append(line[1])
            line = fp.readline()
        except:
            print "End of Read Data."
            break

    fp.close()
except:
    print "Error: Can't read Data."
    exit()

# Draw Graph
plot = []
y_down = 0
y_up = 0.55
pl.title('Convergence Graph Comparison')
pl.xlabel('Times of Iteration')
pl.ylabel('Maximum Power Error')
pl.grid(True)
pl.ylim(y_down, y_up)

for times in sorted(result.keys()):
    x_axis = [e+1 for e in range(len(result[times]))]
    y_axis = result[times][:]
    draw = pl.plot(x_axis, y_axis, label=str(times)+' times')
    plot.append(draw)

pl.legend()
pl.show()