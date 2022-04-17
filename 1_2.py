import pandas as pd
from gurobipy import * 

# data
S = "CGUCUUCACUACAGCAUCGG"
length = len(S)
print(length)

# initialize weight
W = [[0 for i in range(length)] for j in range(length)]
D = [[0 for i in range(length)] for j in range(length)]


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

m = Model("Project")
P = m.addVars(length,length, vtype=GRB.BINARY, name = "P")


# objective
m.setObjective(quicksum(W[i][j]*P[i,j] for i in range(0,length) for j in range(i+1,length)), GRB.MAXIMIZE)
m.update()


# contrains
# (b): distance >= 3
for i in range (0,length):
    for q in range (i+1, length):
        D[i][q] = min(q-i, abs(length-q+i+1))
        if D[i][q] < 3:
            # print("i: ",i, "q: ", q,"D: ", D[i][q])
            m.addConstr(P[i,q] == 0)
    
    # set duplicated pairs to 0
    for j in range (1, length):
        if (i>j):
            m.addConstr(P[i,j] == 0)
        # (d): none-crossing
        for p in range (2,length):
            for q in range(3,length):
                if i<p<j<q:
                    m.addConstr(P[i,j]+P[p,q] <= 1)

# (c) unique

for k in range(0, length):
    # m.addConstr(
    #     (quicksum(P[i,k]+P[k,i] for i in range(0,length))) <= 1
    # )
    buffer = 0
    for i in range(0,length):
        buffer = buffer + P[i,k]
    for j in range(1,length):
        buffer = buffer + P[k,j]
    m.addConstr(buffer <= 1)

# m.addConstr(quicksum(P[i,j] for j in range(0,length) for i in range(1,length)) <= 1)

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
    m.write("1_2.lp")
