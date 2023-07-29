import sys
import time
import psutil
import Matching_dp

# ******** INPUT DATA : STARTS ********

start_time = time.time()
process = psutil.Process()

input_file = sys.argv[1]
output_file = sys.argv[2]

infile = open(input_file, 'r')

input_data = infile.read().split('\n')

strings = []
numbers = [[],[]]

for iter in input_data:
    if(iter.isalpha()):
        strings.append(iter)
    if(iter.isnumeric()):
        if(len(strings) == 1):
            numbers[0].append(int(iter))
        else:
            numbers[1].append(int(iter))

# ******** INPUT DATA : ENDS ********
missCost = {
    'A': {'A' : 0 ,   'C' : 110, 'G' : 48,  'T' : 94},
    'C': {'A' : 110 , 'C' : 0,   'G' : 118, 'T' : 48},
    'G': {'A' : 48 ,  'C' : 118, 'G' : 0,   'T' : 110},
    'T': {'A' : 94 ,  'C' : 48,  'G' : 110, 'T' : 0}
}

gapCost = 30

# ******** String Generator : STARTS ********

s1 = strings[0]
s2 = strings[1]

# s_m = StringMaker
s_m_1 = numbers[0]
s_m_2 = numbers[1]

for i in range(len(s_m_1)):
    s1 = s1[:s_m_1[i]+1] + s1 + s1[s_m_1[i]+1:]

for j in range(len(s_m_2)):
    s2 = s2[:s_m_2[j]+1] + s2 + s2[s_m_2[j]+1:]

##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################



def findTwo(s1,s2):
    s1_len = len(s1)
    s2_len = len(s2)

    DP = [[0 for _ in range(s1_len+1)] for _ in range(2)]

    for j in range(s1_len+1):
        DP[0][j] = gapCost*j

    for i in range(1,s2_len+1):
        DP[1][0] = i*gapCost
        for j in range(1,s1_len+1):
            DP[1][j] = min(DP[0][j] + gapCost,
                           DP[1][j-1] + gapCost,
                           DP[0][j-1] + missCost[s1[j-1]][s2[i-1]])

        for i in range(0,s1_len):
            DP[0][i] = DP[1][i]


    # for i in DP:
    #     print(i)
    # print(DP[s2_len][s1_len])

    return DP[-1]

def SolveDC(s1,s2):

    s1_len = len(s1)
    s2_len = len(s2)

    if(s1_len <= 2 or s2_len <= 2):
        return Matching_dp.SolveDp(s1,s2)[1:]

    s2_left = s2[:s2_len//2]
    s2_right = s2[s2_len//2:]

    minsum = 10**14
    splitpoint = 10**14

    dp_left = findTwo(s1,s2_left)
    dp_right = findTwo(s1[::-1],s2_right[::-1])[::-1]
    # dp = []
    #
    # for i in range(len(dp_right)):
    #     dp.append(dp_left[i]+dp_right[i])
    #
    for i in range(len(dp_right)):
        s = dp_left[i]+dp_right[i]
        if(s<=minsum):
            minsum = s
            splitpoint = i
    print(s1)
    print(s2_left)
    print('finding split point  ;; ',dp_left)
    print(s1[::-1])
    print(s2_right[::-1])
    print('finding split point  ;; ',dp_right)
    # print(dp)
    # splitpoint = dp.index(min(dp[1:]))
    print(splitpoint)
    s1_left = s1[:splitpoint]
    s1_right = s1[splitpoint:]

    print('s1   = ',s1_left,s1_right)
    print('s2   = ',s2_left,s2_right)
    print('splitpoint = ',splitpoint)
    print('\n')

    (s1_left_out,s2_left_out) = SolveDC(s1_left,s2_left)
    (s1_right_out,s2_right_out) = SolveDC(s1_right,s2_right)

    return (s1_left_out + s1_right_out, s2_left_out + s2_right_out)

# print('main inputs : s1 :: ',s1)
# print('main inputs : s2 :: ',s2)
output = []
for i in SolveDC(s1,s2):
    output.append(i)
    print(i)

# for test purpose
print('sequence matching cost ne sequence cost :::: ',Matching_dp.SolveDp(output[0],output[1])[0][-1][-1])

print('sequence matching cost optimal :::: ',findTwo(s1,s2)[-1])
print('True output ::: ')
Matching_dp.SolveDp(s1,s2)[1:]


