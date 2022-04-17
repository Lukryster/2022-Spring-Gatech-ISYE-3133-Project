#----------------------------------------------------------------------------
# Created By  : Bijie Liu
# ---------------------------------------------------------------------------
from gurobipy import * 

# data
S = "CGUCUUCACUACAGCAUCGG"
length = len(S)
print(length)

# initialize weight
W = [[0 for i in range(length)] for j in range(length)]


for i in range(0, length):
    for j in range(i+1, length):
        if (S[i] == "C" and S[j] == "G") or (S[i] == "G" and S[j] == "C"):
            W[i][j] = 1
        elif (S[i] == "A" and S[j]) == "U" or (S[i] == "U" and S[j] == "A"):
            W[i][j] = 1

m = Model("Project")
P = m.addVars(length,length, vtype=GRB.BINARY, name = "P")


# objective
m.setObjective(quicksum(W[i][j]*P[i,j] for i in range(0,length) for j in range(i+1,length)), GRB.MAXIMIZE)
m.update()


# contrains
for i in range (0,length):
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
    m.write("1_1.lp")
