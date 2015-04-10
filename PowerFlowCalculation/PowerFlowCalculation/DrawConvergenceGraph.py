# -*- coding: UTF-8 -*-

# Name:         DrawConvergenceGraph.py
# Func:         To draw the convergence graph of this project
# Author:       Maples7
# Addr:         EE of SDU, China
# Time:         2015-04-10 
# Link:         http://www.cnblogs.com/maples7/

from PowerFlowCalculation import *

import pylab as pl

# main
y_down = 0
y_up = 0.5

plot = []
pl.title('Convergence Graph')
pl.xlabel('Times of Iteration')
pl.ylabel('Maximum Power Error')
pl.grid(True)
pl.ylim(y_down, y_up)

# draw Newton-Raphson method
draw = pl.plot(x_axis, y_axis, label='Newton-Raphson method')
plot.append(draw)

for i in range(len(x_axis)):        # show points' data text
    pl.text(x_axis[i], y_axis[i], str(round(y_axis[i], 7)))


pl.legend()
pl.show()