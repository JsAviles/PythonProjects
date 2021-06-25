##############################################################
# File: Maximum Subarray Brute Force vs. DP solution README  #
# Name: Jesus Sebastian Aviles                               #
##############################################################

File Manifest: 
	• README.txt
	• a2.py

Compile Instructions:
	• Ensure that matplotlib dependencies are installed on local machine
		• python -m pip install matplotlib
		• python3 -m pip install matplotlib (for python3)
	• On terminal use $ python3 a2.py to run the program from directory
		• Note that the Program should still run using python 2.7 

Operating Instructions:
	• The script does not require/take any command line arguments
	• When the script is ran, the user will be prompted to enter their desired length of 'n'
		• The user must enter a value > 0
		• The program then takes the input value of n and created a pseudo random array.
		• Then the array is turned into a new array A, similar to the stock daily price change example from class,
		  and both methods of finding max are tested.
	• The user will be shown a display of the time vs n plotted points, which compares run-time
	  of the bruteforce and recursive implementations

Deficiencies/Bugs: 
	• For low values of n (around the range of 1-100ish), sometimes the time.time() function cannot capture
	  a value because depending on your machine, the sorting instructions are executed too quickly.
		• Therefore, try a couple values for n ranging from 1-1000, or even higher for more plotted points

Lessons Learned: 
    1. How to implement 2 the recursive and bruteforce methods of Finding the Maximum contiguous subarray
    2. Intuitively deciphering pseudo code and implementing it using python

Notes:
	• The implementation was used following the example of the daily price change in stock quotes.
	• The brute force method has the Day[i] - Day[i-1] logic implemented, but the recursive algorithm needs to be supplied
	  with the daily change array A, which is what the for loop on line 103 is designed to accomplish.