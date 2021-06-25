###########################################################
# File: Maximum Subarray Brute Force vs. DP solution      #
# Name: Jesus Sebastian Aviles                            #
###########################################################

import random, time
import matplotlib.pyplot as plt
import numpy as np

#Arrays used to track run-time of implemented functions
bruteforceTime = []
recursiveTime = []

#Brute force implementation of the Find Max
def BRUTE_FORCE_FIND_MAX(A, low, high):
    bruteforceTime.append(time.time()-startMod)#
    maxProfit = 0
    maxLeft = None
    maxRight = None

    #nested for loops with traverse the array in Θ(n^2) and search for a sequence over 
    #which the net change from the first element to the last is the maximum
    for i in range(low, (high-1)):
        bruteforceTime.append(time.time()-startMod)#
        for j in range((i+1), high):
            bruteforceTime.append(time.time()-startMod)#
            profit = (A[j] - A[i])
            #if there is a new max profit then set new indices and update maxprofit
            if (profit > maxProfit):
                maxLeft = i
                maxRight = j
                maxProfit = profit
    return (maxLeft, maxRight, maxProfit)

#Recursive implementation of Find Max 
def FIND_MAXIMUM_SUBARRAY(A, low, high):
    recursiveTime.append(time.time()-startMod)#

    #python arrays start from 0 unlike textbook pseudo code
    if (low == (high-1)):
        return (low, high, A[low])
    else:
        mid = ((low + high)//2)
        #recursive calls to divide and conquer
        leftLow, leftHigh, leftSum = FIND_MAXIMUM_SUBARRAY(A, low, mid)
        rightLow, rightHigh, rightSum = FIND_MAXIMUM_SUBARRAY(A, mid, high)
        crossLow, crossHigh, crossSum = FIND_MAX_CROSSING_SUBARRAY(A, low, mid, high)

        #return the maximum of the 3 values, whether the max subarray is in the left
        #portion of the array, the right portion, or the middle cross section
        if (leftSum >= rightSum and leftSum >= crossSum):
            return (leftLow, leftHigh, leftSum)
        elif (rightSum >= leftSum and rightSum >= crossSum):
            return (rightLow, rightHigh, rightSum)
        else:
            return (crossLow, crossHigh, crossSum)

#Function to search the "crossing point" in the sub array for the MAX
#which is called from within the recursive Maximum Subarray function
def FIND_MAX_CROSSING_SUBARRAY(A, low, mid, high):
    recursiveTime.append(time.time()-startMod)#
    leftSum = float('-inf')
    sum = 0
    maxLeft = mid
    #find the max left sum
    for i in range(mid, low-1, -1):
        recursiveTime.append(time.time()-startMod)#   
        sum = sum +  A[i]
        if (sum > leftSum):
            leftSum = sum
            maxLeft = i
    rightSum = float('-inf')
    sum = 0
    maxRight = mid + 1
    #find the max right sum
    for j in range(mid+1, high):
        recursiveTime.append(time.time()-startMod)#
        sum = sum + A[j]
        if(sum > rightSum):
            rightSum = sum
            maxRight = j + 1
    #return the indices and the max cross sum
    return maxLeft, maxRight, (leftSum + rightSum)

#Function to generate a pseudo random filled array
def generateAr(length):
    ar = []
    for i in range (0, length):
        ar.append(random.randint(0, 1000000))
    return ar

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                             MAIN
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#let user input value for N
n = int(input("\nPlease enter desired array length: "))
Arr = generateAr(n)
A = []

#Using the stock daily price change example from lecture, create change array A where element is is the difference from the day before.
for i in range(0,len(Arr)-1):
    A.append(Arr[i+1]-Arr[i])

#Proceed with the bruteforce FIND MAX
startMod = time.time()
bLeft, bRight, bMax = BRUTE_FORCE_FIND_MAX(Arr, 0, len(Arr))
bruteforceTime.append(time.time()-startMod)#

#Proceed with the Recursive FIND MAX
startMod = time.time()
rLeft, rRight, rMax = FIND_MAXIMUM_SUBARRAY(A, 0, len(A))
recursiveTime.append(time.time()-startMod)#

#####################################################
#                   Data Analysis                   #
#####################################################

#Print the values returned from both FIND MAX implementations
print("\nLeft index = " + str(bLeft) + ", Right index = " + str(bRight) +", Maximum profit = " + str(bMax))
print("Left index = " + str(rLeft) + ", Right index = " + str(rRight) +", Maximum profit = " + str(rMax) + "\n")

#print total time it took for each sorting method to complete
#low values of 'n' produce a 0 time because they run too fast so added +00000000000001 for visualization
print("BruteForce Time  =  {:.15f}".format((bruteforceTime[len(bruteforceTime)-1]- bruteforceTime[0])+.000000000000001) + "(s)")
print("Recursion Time   =  {:.15f}".format((recursiveTime[len(recursiveTime)-1]- recursiveTime[0])+.000000000000001)+ "(s)\n")

# customize plot to merge and insertion time data
X1 = np.linspace(0,n,len(bruteforceTime))
plt.plot(X1, bruteforceTime, label = "BruteForce")
X2 = np.linspace(0,n,len(recursiveTime))
plt.plot(X2, recursiveTime, label = "Recursive")

#Show plot
print("\nPlotting time vs n for Find Max Methods...close plot to continue...\n")
plt.xlabel('n = ' + str(n)) 
plt.ylabel('Time (s)') 
plt.legend()
plt.show() 