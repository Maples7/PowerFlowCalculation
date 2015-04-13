# -*- coding: UTF-8 -*-

# Name:         PowerFlowCalculation.py
# Func:         To make input Data of this project, this can be the startup file of this project too.
# Author:       Maples7
# Addr:         EE of SDU, China
# Time:         2015-04-13 
# Link:         http://www.cnblogs.com/maples7/

import globalVariable as gv

# Read init Data
orignalInputFile = "input.txt"
try:
    fp = open(orignalInputFile, "r+")

    firstLine = fp.readline().split(" ")
    gv.num_node = int(firstLine[0])
    gv.num_line = int(firstLine[1])
    gv.num_tran = int(firstLine[2])
    gv.num_gene = int(firstLine[3])
    gv.num_load = int(firstLine[4])
    gv.error_max = float(firstLine[5])

    gv.line = []
    for i in range(gv.num_line):
        nLine = fp.readline().split(" ")
        temp = gv.Line(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
        gv.line.append(temp)

    nLine = fp.readline()
    gv.tran = []
    for i in range(gv.num_tran):
        nLine = fp.readline().split(" ")
        temp = gv.Tran(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
        gv.tran.append(temp)

    nLine = fp.readline()
    gv.gene = []
    for i in range(gv.num_gene):
        nLine = fp.readline().split(" ")
        temp = gv.Gene(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
        gv.gene.append(temp)

    nLine = fp.readline()
    gv.load = []
    for i in range(gv.num_load):
        nLine = fp.readline().split(" ")
        temp = gv.Load(int(nLine[0]), float(nLine[1]), float(nLine[2]))
        gv.load.append(temp)

    fp.close()
except:
    print "Error: Can't read Data from "+orignalInputFile+"."
    exit()

# output Created Data
inputFile = "input1.txt"
try:
    fou = open(inputFile, "w+")
except:
    print "Error: Can't create "+inputFile+"."
    exit()

fou.write(str(gv.num_node)+' '+str(gv.num_line)+' '+str(gv.num_tran)+' '+str(gv.num_gene)+' '+str(gv.num_load)+' '+str(gv.error_max)+'\n')

for e in gv.line:
    times = 1       # change the var to look into the regular pattern
    fou.write(str(e.i)+' '+str(e.j)+' '+str(e.a*times)+' '+str(e.b*times)+' '+str(e.c*times))
    fou.write('\n')
fou.write('\n')

for e in gv.tran:
    times = 1
    fou.write(str(e.i)+' '+str(e.j)+' '+str(e.a*times)+' '+str(e.b*times)+' '+str(e.c*times))
    fou.write('\n')
fou.write('\n')

for e in gv.gene:
    times = 1
    fou.write(str(e.i)+' '+str(e.j)+' '+str(e.a*times)+' '+str(e.b*times)+' '+str(e.c*times))
    fou.write('\n')
fou.write('\n')

for e in gv.load:
    times = 1
    fou.write(str(e.i)+' '+str(e.a*times)+' '+str(e.b*times))
    fou.write('\n')
fou.write('\n')

try:
    fou.close()
except:
    print "Error: Close Files Error."
    exit()