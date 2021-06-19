###########################################################
# File: Assignment #1 Question 1
# Name: Jesus Sebastian Aviles
# REDID: 823931557
# Class: CS560 Spring 2021
###########################################################

import random, time
import matplotlib.pyplot as plt
import numpy as np

#global variables to store and analyze the sorting method "time"
insertTime = []
mergeTime = []

#Function to generate a pseudo random filled array
def generateAr(length):
    ar = []
    for i in range (0, length):
        ar.append(random.randint(1, 99999))
    return ar

#Function for the insertion sort algorithm
def insertionSort(ar):
    for j in range (1, len(ar)):
        key = ar[j]
        i = (j - 1)
        while (i >= 0) & (ar[i] > key):
            ar[i+1] = ar[i]
            i = (i - 1)
        insertTime.append(time.time()-startMod)
        ar[i+1] = key

#Functions for the merge sort algorithm
def mergeSort(A, p, r):
    mergeTime.append(time.time()-startMod)
    if(p<r):
        q = ((p+r)//2)
        mergeSort(A, p, q)
        mergeSort(A, q+1, r)
        merge(A, p, q, r)

def merge(A, p, q, r):
    n1 = q - p + 1
    n2 = r - q

    #create empty subarrays left/right with their respective lengths
    left = [0] * (n1)
    right = [0] * (n2)

    # copy the original elements in A to Left and Right, to their respective index
    for i in range (0,n1):
        left[i] = A[p + i]
    for j in range (0,n2):
        right[j] = A[q+j+1]
    mergeTime.append(time.time()-startMod)#

    #compare and merge
    i = 0
    j = 0
    k = p
    while (i<n1 and j<n2):
        if (left[i] <= right[j]):
            A[k] = left[i]
            i=i+1
        else:
            A[k]=right[j]
            j=j+1
        k=k+1
    mergeTime.append(time.time()-startMod)#
    while i < n1: 
        A[k] = left[i] 
        i += 1
        k += 1
    while j < n2: 
        A[k] = right[j] 
        j += 1
        k += 1
    mergeTime.append(time.time()-startMod)#

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                             MAIN
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#let user input value for N
n = int(input("\nPlease enter desired array length: "))

#####################################################
#                  Insertion sort                   #
#####################################################
iAr = generateAr(n)
#startMod = time.time()//1
startMod = time.time()
startTime = (time.time()-startMod)
insertTime.append(time.time()-startMod)#
insertionSort(iAr)
insertTime.append(time.time()-startMod)

#####################################################
#                    Merge sort                     #
#####################################################
mAr = generateAr(n)
startMod = time.time()
mergeTime.append(time.time()-startMod)#
mergeSort(mAr, 0, len(mAr)-1)
mergeTime.append(time.time()-startMod)#

#####################################################
#                   Data Analysis                   #
#####################################################

#print total time it took for each sorting method to complete
#low values of 'n' produce a 0 time because they run too fast so added +00000000000001 for visualization
print("\nInsertion sort Time  =  {:.15f}".format((insertTime[len(insertTime)-1]- insertTime[0])+.000000000000001) + "(s)")
print("Merg sort Time       =  {:.15f}".format((mergeTime[len(mergeTime)-1]- mergeTime[0])+.000000000000001)+ "(s)")

# customize plot to merge and insertion time data
X1 = np.linspace(0,n,len(insertTime))
plt.plot(X1, insertTime, label = "insertion sort")
X2 = np.linspace(0,n,len(mergeTime))
plt.plot(X2, mergeTime, label = "merge sort")

#Show plot
print("\nPlotting time vs n for sorting methods...close plot to continue...\n")
plt.xlabel('n = ' + str(n)) 
plt.ylabel('Time (s)') 
plt.legend()
plt.show() 

flag = input("Would you like to view the sorted arrays? (y/n): ")

if flag == 'y':
    print("\nInsertion array:\n" + str(iAr) + "\n\nMerge array:\n" + str(mAr))
elif flag == 'Y':
    print("\nInsertion array:\n" + str(iAr) + "\n\nMerge array:\n" + str(mAr))

print("\nEnding Session...\n")