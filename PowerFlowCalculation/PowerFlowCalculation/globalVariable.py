# -*- coding: UTF-8 -*-

# Name:         globalVariable.py
# Func:         To state the all global variables of this project
# Author:       Maples7
# Addr:         EE of SDU, China
# Time:         2015-04-07 
# Link:         http://www.cnblogs.com/maples7/

# totle number of nodes
num_node = 0

# totle number of lines and parallel capacitors
num_line = 0

# totle number of transformer branches
num_tran = 0

# totle number of generator nodes
num_gene = 0

# totle number of load buses
num_load = 0

# admissible error of the unbalance of node power
error_max = 0.0


# obj of lines and parallel capacitors
class Line:
    def __init__(self, i, j, a, b, c):
        self.i = i
        self.j = j
        self.a = a
        self.b = b
        self.c = c
line = []

# obj of transformer branches
class Tran:
    def __init__(self, i, j, a, b, c):
        self.i = i
        self.j = j
        self.a = a
        self.b = b
        self.c = c
tran = []

# obj of generator nodes
class Gene:
    def __init__(self, i, j, a, b, c):
        self.i = i
        self.j = j
        self.a = a
        self.b = b
        self.c = c
gene = []

# obj of load buses
class Load:
    def __init__(self, i, a, b):
        self.i = i
        self.a = a
        self.b = b
load = []
          