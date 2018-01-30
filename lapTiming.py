import math
import time


#finds line intersections
def lineCrossing(l1P1=[], l1P2=[], l2P1=[], l2P2=[]):
    x = l1P1[0]
    y = l1P2[1]

    return False
#last laptime
#best laptime
#current laptime

l1P1 = [0,0]
l1P2 = [10,0]

startTime = time.time()
l2P1 = [5,20.5]

i = 20.5
while i > -20.5:
    print(i)
    l2P2 = [5, l2P1[1]]
    l2P1 = [5,i]
    print(l1P1, l1P2, l2P1, l2P2)
    if lineCrossing(l1P1, l1P2, l2P1, l2P2) == True:
        endTime = time.time()
        timeDiff = endTime-startTime
        print("timeDiff:", timeDiff)
    i = i - 1
    time.sleep(0.1)

