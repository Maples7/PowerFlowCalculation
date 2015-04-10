# -*- coding: UTF-8 -*-

# Name:         PowerFlowCalculation.py
# Func:         To calc the power flow of elecrtcal grid using Newton-Raphson method, this is the main file of this project
# Author:       Maples7
# Addr:         EE of SDU, China
# Time:         2015-04-07 
# Link:         http://www.cnblogs.com/maples7/

import globalVariable as gv
import numpy as np
from math import sin, cos, fabs, pi

# const
MAX_ITER = 10               # max iter times
DIVERGENCE_ERROR = 1.0e4    


def read_data():
    """
    Read Data from input.txt, the global variables are in the globalVariable.py
    """
    try:
        fp = open("input.txt", "r+")

        firstLine = fp.readline().split(" ")
        gv.num_node = int(firstLine[0])
        gv.num_line = int(firstLine[1])
        gv.num_tran = int(firstLine[2])
        gv.num_gene = int(firstLine[3])
        gv.num_load = int(firstLine[4])
        gv.error_max = float(firstLine[5])

        gv.line = [None]
        for i in range(gv.num_line):
            nLine = fp.readline().split(" ")
            temp = gv.Line(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
            gv.line.append(temp)

        nLine = fp.readline()
        gv.tran = [None]
        for i in range(gv.num_tran):
            nLine = fp.readline().split(" ")
            temp = gv.Tran(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
            gv.tran.append(temp)

        nLine = fp.readline()
        gv.gene = [None]
        for i in range(gv.num_gene):
            nLine = fp.readline().split(" ")
            temp = gv.Gene(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
            gv.gene.append(temp)

        nLine = fp.readline()
        gv.load = [None]
        for i in range(gv.num_load):
            nLine = fp.readline().split(" ")
            temp = gv.Load(int(nLine[0]), float(nLine[1]), float(nLine[2]))
            gv.load.append(temp)

        fp.close()
    except:
        print "Error: Can't input Data into input.txt. (function read_data() error)"
        exit()

def output_file_ready():
    """
    make output.txt file ready to store output result
    """
    global fou
    try:
        fou = open("output.txt", "w+")
    except:
        print "Error: Can't create output.txt. (function output_file_ready() error)"
        exit()

def admt_matrix():
    """
    Create admittance matrix
    """
    global Y
    Y = np.zeros((gv.num_node+1, gv.num_node+1), dtype = complex)
    for lineNum in range(1, gv.num_line+1):
        i = gv.line[lineNum].i
        j = gv.line[lineNum].j
        r = gv.line[lineNum].a
        x = gv.line[lineNum].b
        comp = 1/complex(r, x)
        if i==j:
            Y[i][i] += comp
        else:
            c = gv.line[lineNum].c
            Y[i][j] -= comp
            Y[j][i] = Y[i][j]
            Y[i][i] += (comp + complex(0, c))
            Y[j][j] += (comp + complex(0, c))
    for tranNum in range(1, gv.num_tran+1):
        i = gv.tran[tranNum].i
        j = gv.tran[tranNum].j
        r = gv.tran[tranNum].a
        x = gv.tran[tranNum].b
        c = gv.tran[tranNum].c
        comp = 1/complex(r, x)
        Y[i][i] += comp
        Y[i][j] -= comp/c
        Y[j][i] = Y[i][j]
        Y[j][j] += comp/c/c


def Um_and_Ua():
    """
    Set the amplitude and phase angle of voltage
    """
    global Um
    global Ua
    Um = np.ones(gv.num_node+1)
    Ua = np.zeros(gv.num_node+1)
    for i in range(1, gv.num_gene+1):
        if gv.gene[i].j <= 0:
            Um[gv.gene[i].i] = gv.gene[i].c

def form_Jacobian():
    """
    Form Jacobian Matrix & Calc the Power error
    """
    global Um
    global Ua
    global Jacob
    global P 
    global Q
    global Y

    n2 = 2*gv.num_node
    nu = n2 + 1
    for i in range(1, gv.num_node+1):
        vi = Um[i]
        di = Ua[i]
        dp = 0.0
        dq = 0.0
        for j in range(1, gv.num_node+1):
            if j != i:                  # when i <> j, off-diagonal elements
                g = Y[i][j].real        # G        
                b = Y[i][j].imag        # B
                vj = Um[j]
                dj = Ua[j]
                dij = di - dj           # diff of Phase Angle
                Hij = -Um[i] * Um[j] * (g*sin(dij) - b*cos(dij))
                Lij = Hij
                Jacob[i][j] = Hij
                Jacob[i+gv.num_node][j+gv.num_node] = Lij
                Nij = -Um[i]*Um[j]*(g*cos(dij)+b*sin(dij))
                Mij = -Nij
                Jacob[i][j+gv.num_node]=Nij
                Jacob[i+gv.num_node][j] = Mij
                p = Um[j]*(g*cos(dij)+b*sin(dij))
                q = Um[j]*(g*sin(dij)-b*cos(dij))
                dp += p
                dq += q
        g = Y[i][i].real
        b = Y[i][i].imag
        Hii = vi*dq
        Nii = -vi*dp - 2*vi*vi*g
        Mii = -vi*dp
        Lii = -vi*dq + 2*vi*vi*b
        Jacob[i][i] = Hii
        Jacob[i][i+gv.num_node] = Nii
        Jacob[i+gv.num_node][i] = Mii
        Jacob[i+gv.num_node][i+gv.num_node] = Lii
        Jacob[i][nu] = -vi*(dp+vi*g)
        Jacob[i+gv.num_node][nu] = -vi*(dq-vi*b)
        P[i] = vi * (dp+vi*g)
        Q[i] = vi * (dq-vi*b)
    for i in range(1, gv.num_load+1):
        kk = gv.load[i].i
        lp = gv.load[i].a
        lq = gv.load[i].b
        Jacob[kk][nu] += -lp
        Jacob[kk+gv.num_node][nu] += -lq
    for i in range(1, gv.num_gene+1):
        kk = gv.gene[i].i
        gp = gv.gene[i].a
        gq = gv.gene[i].b
        Jacob[kk][nu] += gp
        Jacob[kk+gv.num_node][nu] += gq
    for k in range(1, gv.num_gene+1):
        ii = gv.gene[k].i
        kk = gv.gene[k].j
        if kk == 0:         # Balance nodes
            for j in range(1, n2+1):
                Jacob[ii][j] = 0.0
                Jacob[gv.num_node+ii][j] = 0.0
                Jacob[j][ii] = 0.0
                Jacob[j][gv.num_node+ii] = 0.0
            Jacob[ii][ii] = 1.0
            Jacob[gv.num_node+ii][gv.num_node+ii] = 1.0
            Jacob[ii][nu] = 0.0
            Jacob[gv.num_node+ii][nu] = 0.0
        if kk < 0:          # PV nodes
            for j in range(1, n2+1):
                Jacob[gv.num_node+ii][j] = 0.0
                Jacob[j][gv.num_node+ii] = 0.0
            Jacob[gv.num_node+ii][gv.num_node+ii] = 1.0
            Jacob[gv.num_node+ii][nu] = 0.0

def node_flow():
    """
    output the power flow of nodes
    """
    global fou
    global P
    global Q
    global Um
    global Ua
    fou.write("\n\n\n\t\t* - * - * - Rasult of Power Flow Calculation * - * - * -")
    fou.write("\n\n\t\t\t\t-------power flow of nodes-------")
    fou.write("\n\n\tno.i\t\tUm\t\tUa\t\tPG\t\tQG\t\tPL\t\tQL\n\n")
    for i in range(1, gv.num_node+1):
        b1,b2,c1,c2 = 0.0, 0.0, 0.0, 0.0
        for j in range(1, gv.num_gene+1):
            ii = gv.gene[j].i
            kk = gv.gene[j].j
            if i == ii and kk == 0:         # Balance nodes
                b1 = P[ii]
                b2 = Q[ii]
                for k in range(1, gv.num_load+1):
                    ii = gv.load[k].i
                    if i == ii:
                        c1 = gv.load[k].a
                        c2 = gv.load[k].b
                        b1 += c1
                        b2 += c2
                break
        if i == ii and kk == -1:            # PV nodes
            b1 = gv.gene[j].a
            b2 = Q[ii]
            for k in range(1, gv.num_load+1):
                ii = gv.load[k].i
                if i == ii:
                    c1 = gv.load[k].a
                    c2 = gv.load[k].b
                    b2 += c2
            # break  ????????  
        for j in range(1, gv.num_load+1):
            ii = gv.load[j].i
            if i == ii:
                c1 = gv.load[j].a
                c2 = gv.load[j].b
                break
        fou.write(" %6d %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f\n" %(i, Um[i], Ua[i]*180.0/pi, b1, b2, c1, c2))

def branch_flow():
    """
    output the power flow of branches
    """
    global Um
    global Ua
    fou.write("\n\n\t\t\t\t-------power flow of branches-------")
    fou.write("\n\n\ti\tj\t\tPij\t\tQij\t\tPji\t\tQji\t\tdP\t\tdQ\n\n")
    ph, qh = 0.0, 0.0
    for p in gv.line:
        if p == None:
            continue
        i = p.i
        j = p.j
        r = p.a
        x = p.b
        b = r*r + x*x
        if i == j:
            vi = Um[i]
            b = vi*vi/b
            pij = r*b
            qij = x*b
            pji = 0.0
            qji = 0.0
            dpb = pij
            ph += dpb
            dpb = qij
            qh += dpb
        else:
            r = r/b
            x = -x/b
            b = p.c
            dij = Ua[i] - Ua[j]
            vi = Um[i]
            vj = Um[j]
            vij = vi*vj
            vi *= vi
            vj *= vj
            cd = vij * cos(dij)
            sd = vij * sin(dij)
            pij = vi*r - r*cd - x*sd
            pji = vj*r - r*cd + x*sd
            dpb = pij + pji
            ph += dpb
            qij = -vi*(b+x) + x*cd - r*sd
            qji = -vj*(b+x) + x*cd + r*sd
            dqb = qij + qji
            qh += dqb
        fou.write(" %3d  %3d %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f\n" %(i, j, pij, qij, pji, qji, dpb, dqb))
    for p in gv.tran:
        if p == None:
            continue
        i = p.i
        j = p.j
        r = p.a
        x = p.b
        t = p.c
        b = t*(r*r+x+x)
        r /= b
        x /= -b
        b = t - 1.0
        ri = r*b
        xi = x*b
        rj = -ri/t
        xj = -xi/t
        vi = Um[i]
        vj = Um[j]
        vij = vi*vj
        vi *= vi
        vj *= vj
        dij = Ua[i] - Ua[j]
        cd = vij * cos(dij)
        sd = vij * sin(dij)
        pij = vi*(ri+r) - r*cd - x*sd
        pji = vj*(rj+r) - r*cd + x*sd
        dpb = pij + pji
        ph += dpb
        qij = -vi*(xi+x) + x*cd - r*sd
        qji = -vj*(xj+x) + x*cd + r*sd
        dpb = qij + qji
        qh += dpb
        fou.write(" %3d  %3d %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f\n" %(i, j, pij, qij, pji, qji, dpb, dqb))
    fou.write("\n\nThe total loss of the system: - Active power:%8.5f\t\tReactive power:%8.5f" %(ph, qh))

def solv_Eqn():
    """
    solve the Modified Equations
    """
    global Jacob
    n2 = 2*gv.num_node
    nu = n2 + 1
    for i in range(1, n2+1):
        i1 = i+1
        d = 1.0/Jacob[i][i]
        for j in range(i1, nu+1):
            e = Jacob[i][j]
            if e != 0.0:
                Jacob[i][j] = e*d
        if i != n2:
            for j in range(i1, n2+1):
                e = Jacob[j][i]
                if e != 0.0:
                    for k in range(i1, nu+1):
                        Jacob[j][k] -= Jacob[i][k]*e
    for k in range(2, n2+1):
        i = n2 - k + 1
        i1 = i + 1
        for j in range(i1, n2+1):
            Jacob[i][nu] = Jacob[i][nu] - Jacob[i][j]*Jacob[j][nu]

def close_file():
    """
    close output.txt
    """
    global fou
    try:
        fou.close()
    except:
        print "Error: Close Files Error. (function close_file() error)"
        exit()

# main 
read_data()
output_file_ready()
admt_matrix()
Um_and_Ua()

Jacob = np.zeros((2*gv.num_node+1, 2*gv.num_node+2))
P = np.zeros(gv.num_node+1)
Q = np.zeros(gv.num_node+1)

iter = 0  
while True:
    form_Jacobian()
    error = 0.0
    for i in range(1, 2*gv.num_node+1):
        if fabs(Jacob[i][2*gv.num_node+1]) > error:
            error = fabs(Jacob[i][2*gv.num_node+1])
    fou.write("Times of iteration: %2d\t\tThe maximum power error: %11.6f\n" %(iter+1, error))
    if error < gv.error_max:
        node_flow()
        branch_flow()
        break
    if iter > MAX_ITER or error > DIVERGENCE_ERROR:
        fou.write("\n\n\t\tThe power flow is Divergence.")
        break
    solv_Eqn()
    for i in range(1, gv.num_node+1):
        a = Jacob[i][2*gv.num_node+1]
        Ua[i] += -a
        a = Jacob[gv.num_node+i][2*gv.num_node+1]
        Um[i] *= 1-a
    iter += 1

close_file()

