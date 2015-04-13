# -*- coding: UTF-8 -*-

# Name:         DrawConvergenceGraph.py
# Func:         To draw the convergence graph of this project, this can be the startup file of this project too.
# Author:       Maples7
# Addr:         EE of SDU, China
# Time:         2015-04-10 
# Link:         http://www.cnblogs.com/maples7/

from PowerFlowCalculation import *

import pylab as pl

# main
#y_down = 0
#y_up = 0.6
floatResBit = 7

plot = []
pl.title('Convergence Graph')
pl.xlabel('Times of Iteration')
pl.ylabel('Maximum Power Error')
pl.grid(True)
#pl.ylim(y_down, y_up)

# draw Newton-Raphson method
draw = pl.plot(x_axis, y_axis, 'blue', label='Newton-Raphson Method')
plot.append(draw)

for i in range(len(x_axis)):        # show points' data text
    pl.text(x_axis[i], y_axis[i], str(round(y_axis[i], floatResBit)))


# draw PQ decomposition method， The Data is from Page 115 in Reference book
# for comparison
#x_axis = [1, 2, 3, 4, 5, 6, 7]
#y_axis = [0.55580, 0.07135, 0.00715, 0.00078, 0.00020, 0.00005, 0.00001]
#draw = pl.plot(x_axis, y_axis, 'red', label='PQ Decomposition Method')
#plot.append(draw)

#for i in range(len(x_axis)):        # show points' data text
#    pl.text(x_axis[i], y_axis[i], str(round(y_axis[i], floatResBit)))


pl.legend()
pl.show()