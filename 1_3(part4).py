#----------------------------------------------------------------------------
# Created By  : Bijie Liu
# ---------------------------------------------------------------------------
from audioop import cross
import pandas as pd
from gurobipy import * 

# data
S = "CGUCUUCACUACAGCAUCGG"
# S = "GACCUUACUGGGUACGAUUUACUGGAGGAC"
# S = "GGCCAGACUGGUGGUGUGACUCCAGGCUAACCGGAUACGCGUGCCUCGGG"
length = len(S)
print(length)

# initialize weight and distance for each pair
W = [[0 for i in range(length)] for j in range(length)]
V = [[0 for i in range(length)] for j in range(length)]
D = [[0 for i in range(length)] for j in range(length)]

# pair weight
for i in range(0, length):
    for j in range(i+1, length):
        if (S[i] == "C" and S[j] == "G") or (S[i] == "G" and S[j] == "C"):
            W[i][j] = 3
        elif (S[i] == "A" and S[j]) == "U" or (S[i] == "U" and S[j] == "A"):
            W[i][j] = 2
        elif (S[i] == "G" and S[j] == "U") or (S[i] == "U" and S[j] == "G"):
            W[i][j] = 0.1
        elif (S[i] == "A" and S[j] == "C") or S[i] == "C" and S[j] == "A":
            W[i][j] = 0.05

# quartet weight
for i in range(0,length-3):
    for j in range(i+3, length-1):
        if (S[i] == "A" and S[j] == "U" and S[i+1] == "A" and S[j-1] == "U"):
            V[i][j] = 9
            print(i,j)
        elif (S[i] == "A" and S[j] == "U" and S[i+1] == "C" and S[j-1] == "G"):
            V[i][j] = 21
        elif (S[i] == "A" and S[j] == "U" and S[i+1] == "G" and S[j-1] == "C"):
            V[i][j] = 24
        elif (S[i] == "A" and S[j] == "U" and S[i+1] == "U" and S[j-1] == "A"):
            V[i][j] = 13
        elif (S[i] == "C" and S[j] == "G" and S[i+1] == "A" and S[j-1] == "U"):
            V[i][j] = 22
        elif (S[i] == "C" and S[j] == "G" and S[i+1] == "C" and S[j-1] == "G"):
            V[i][j] = 33
        elif (S[i] == "C" and S[j] == "G" and S[i+1] == "G" and S[j-1] == "C"):
            V[i][j] = 34
        elif (S[i] == "C" and S[j] == "G" and S[i+1] == "U" and S[j-1] == "A"):
            V[i][j] = 24
        elif (S[i] == "G" and S[j] == "C" and S[i+1] == "A" and S[j-1] == "U"):
            V[i][j] = 21
        elif (S[i] == "G" and S[j] == "C" and S[i+1] == "C" and S[j-1] == "G"):
            V[i][j] = 24
        elif (S[i] == "G" and S[j] == "C" and S[i+1] == "G" and S[j-1] == "C"):
            V[i][j] = 33
        elif (S[i] == "G" and S[j] == "C" and S[i+1] == "U" and S[j-1] == "A"):
            V[i][j] = 16

# decision variables
m = Model("Project")
P = m.addVars(length,length, vtype=GRB.BINARY, name = "P")
C = m.addVars(length,length,length,length, vtype=GRB.BINARY, name = "C")
Q = m.addVars(length,length, vtype=GRB.BINARY, name = "Q")
F = m.addVars(length,length, vtype=GRB.BINARY, name = "F")
L = m.addVars(length,length, vtype=GRB.BINARY, name = "L")

# objective
m.setObjective(
    quicksum(F[i,j] + L[i,j] + Q[i,j] for i in range(0,length-3) for j in range(i+1,length))+
    quicksum(W[i][j]*P[i,j] for i in range(0,length) for j in range(i+1,length))
    , GRB.MAXIMIZE)




# contrains
crossingBuffer = 0
# (f): distance >= 3
for i in range (0,length):
    for q in range (i+1, length):
        D[i][q] = min(q-i, abs(length-q+i+1))
        if D[i][q] < 3:
            m.addConstr(P[i,q] == 0)
    # set duplicated pairs to 0
    for j in range (i+1, length):
        if (i>j):
            m.addConstr(P[i,j] == 0)
        # (h&i): yes crossing
        for p in range (i+2,length):
            for q in range(i+3,length):
                if i<p<j<q:
                    m.addConstr(P[i,j]+P[p,q]-C[i,p,j,q] <= 1)
                    crossingBuffer += C[i,p,j,q]
m.addConstr(crossingBuffer <= 10)

for i in range(0,length -3):
    for j in range(i+3, length):
        # Counting Stacked Quartets:
        # (j)
        m.addConstr(P[i,j] + P[i+1,j-1] - Q[i,j] <= 1)
        # (k) 
        m.addConstr(2*Q[i,j] - P[i,j] - P[i+1,j-1] <= 0)
        # Determining first/last stacked quartet in a stack
        # skip the case for i=0 and j = length case for the following constrains
        if i == 0 or j == length-1:
            continue
        # # (l)
        # m.addConstr(Q[i,j] - Q[i-1,j+1] - F[i,j] <= 0)
        # # (m)
        # m.addConstr(2*F[i,j] - Q[i,j] + Q[i-1,j+1] <= 1)
        # # (n)
        # m.addConstr(P[i,j] - P[i-1,j+1] - L[i,j] <= 0)
        # # (o)
        # m.addConstr(2*L[i,j] - P[i,j] + P[i-1,j+1] <= 1)
        m.addConstr(Q[i,j] >= F[i,j])
        m.addConstr(Q[i,j] + (1-Q[i-1,j+1]) >= 2*F[i,j])
        m.addConstr(Q[i,j] >= L[i,j])
        m.addConstr(Q[i,j] + (1-Q[i+1, j-1]) >= 2*L[i,j])
        
        # (p) & (q)
        W[i][j] += F[i,j]*W[i][j]
        W[i][j] += L[i,j]*W[i][j]

# (g) unique(each position can only be in one pair)
for k in range(0, length):
    buffer = 0
    for i in range(0,length):
        buffer = buffer + P[i,k]
    for j in range(1,length):
        buffer = buffer + P[k,j]
    m.addConstr(buffer <= 1)







m.optimize()
status_code = {1: 'LOADED', 2: 'OPTIMAL', 3: 'INFEASIBLE', 4: 'INF_OR_UNBD', 5: 'UNBOUNDED'}
status = m.status


print("The optimization status is {}".format(status_code[status]))
if status == 2:
# Retrieve variables value
    print("Optimal solution:")
    for v in m.getVars():
        print("%s = %g" % (v.varName, v.x))
    print("Optimal objective value:\n{}".format(m.objVal))
    m.write("1_3(part4).lp")
