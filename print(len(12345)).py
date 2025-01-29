import time

T = time.localtime()
if T[3] == 12 or T[3] < 7:
    p = "pm"
else: p="am"

today = "Today is: "+str(T[2])+"/"+str(T[1])+"/"+str(T[0])+"  "+str(T[3])+":"+str(T[4])+" "+str(p)
