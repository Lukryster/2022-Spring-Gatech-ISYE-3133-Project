# data
String = "CGUCUUCACUACAGCAUCGG"
length = len(String)
print(length)

S = list(String)
print(S[0])

# initialize weight
# print(S[0])
# print(S[3])
V = [[0 for i in range(length)] for j in range(length)]
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
        print(i,j,V[i][j])