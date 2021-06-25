##################################################################
# File: Merge sort vs Insertion sort speed comparison README     #
# Name: Jesus Sebastian Aviles                                   #
##################################################################

File Manifest: 
	• README.txt
	• a1.py

Compile Instructions:
	• Ensure that matplotlib dependencies are installed on local machine
		• python -m pip install matplotlib
		• python3 -m pip install matplotlib (for python3)

Operating Instructions:
	• The script does not require/take any command line arguments
	• When the script is ran, the user will be prompted to enter their desired length of 'n'
		• The user must enter a value > 0
	• After the user is done viewing the Time vs N plot, close the plot to continue where
	  the user will be prompted to print both sorted arrays to verify they are indeed sorted

Deficiencies/Bugs: 
	• For low values of n (around the range of 1-150ish), sometimes the time.time() function cannot capture
	  a value because depending on your machine, the sorting instructions are executed too quickly.
		• Therefore, if you wish to see insertion sort < merge sort run-time, try a couple of values between
		  125-200.

Lessons Learned: 
    1. How to implement 2 sorting algorithms using python
    2. Plotting multiple sets using matlab dependencies