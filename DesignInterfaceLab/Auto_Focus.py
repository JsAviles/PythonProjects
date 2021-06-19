import numpy as np
import sys, pyautogui, time
import cv2

#pop up dialog box, ask user which orientation camera is, create horizontal button and vertical button.
camera_position = input("Camera Orientation : Enter 'V' for vertical or Enter 'H' for horizontal. \n")

filename = sys.argv[1]
data_file = np.loadtxt(filename)

true = 1
counter = 0
z_in = 0
z_out = 0
stop_zooming = 0
z_out_ctr = 0
difference = 0

while(true): 

    #Ensure there are atleast 2 elements to compare before continuing, once data_file has atleat 2 elements, loop will no longer execute.
    while(len(data_file)<2):
        data_file = np.loadtxt(filename)
        counter += 1     

    data_file = np.loadtxt(filename)

    #check if a new element was added and if it was, compare last 2 elements and control the camera
    if counter < len(data_file):            
        print(data_file[counter])          
        counter += 1                        
        print(len(data_file))               #test print for length of data_file array

        #Calculate the difference between the last element with the second to last element -->if the last element is bigger --> will be positive, smaller --> will be negative
        #If the camera has already found a focal point but the difference breaks a threshold, reset the focus key variable and resume auto focusing
        difference = data_file[counter-1] - data_file[counter -2]       
        if (difference < -.05) and stop_zooming==1:                    
            z_out = 0
            z_in = 0
            z_out_ctr = 0
            stop_zooming = 0
            print("\nOut of focus, re-focusing\n")

        if stop_zooming==0:
            #Initially zoom out the camera to test the focus
            if z_out == 0 and z_in==0:                     
                if (camera_position =='h' or camera_position=='H'):                
                    pyautogui.press('up')
                elif(camera_position =='v' or camera_position=='V'):
                    pyautogui.press('pageup')
                z_out = 1
                print('Zooming out--Case 1\n')
            #if the new number keeps getting better, keep zooming out
            elif difference > 0 and z_out==1 and z_in==0:                                  
                if (camera_position =='h' or camera_position=='H'):                
                    pyautogui.press('up')
                elif(camera_position =='v' or camera_position=='V'):
                    pyautogui.press('pageup')
                z_out_ctr +=1
                print('Zooming out--Case 2\n')
            #if the new number is smaller(focus got worse) but we already tried zooming out--> do these
            elif difference < 0 and z_out==1 and z_in==0:
                #if we have zoomed out more than 2 times, only zoom back in once and stop zooming
                if z_out_ctr > 1 :
                    if (camera_position =='h' or camera_position=='H'):                
                        pyautogui.press('down')
                    elif(camera_position =='v' or camera_position=='V'):
                        pyautogui.press('pagedown')
                    stop_zooming = 1
                    print("Zoomed out more than 2 times and focus got worse, stop zooming")
                #otherwise zoom in twice and check the opposite direction for better focus
                else:
                    if (camera_position =='h' or camera_position=='H'):                
                        pyautogui.press('down')
                    elif(camera_position =='v' or camera_position=='V'):
                        pyautogui.press('pagedown', presses = 2, interval=1)
                    z_in = 1
                    print('Zooming in--Case 3\n')
            #after zooming in twice to check other direction, if the new diff is positive(focus is getting better), keep zooming in for better focus until we go out of focus again
            elif difference > 0 and z_in == 1:                   
                if (camera_position =='h' or camera_position=='H'):                
                    pyautogui.press('down')
                elif(camera_position =='v' or camera_position=='V'):
                    pyautogui.press('pagedown')
                print('Zooming in--Case 4\n')
            #after zooming in twice, if new number is smaller(focus got worse) zoom back out to previous position, and set stop_zooming key to 1 to stop auto focusing
            elif difference < 0 and z_out==1 and z_in ==1:                  
                if (camera_position =='h' or camera_position=='H'):                
                    pyautogui.press('up')
                elif(camera_position =='v' or camera_position=='V'):
                    pyautogui.press('pageup')
                stop_zooming = 1
                print('Number got worse after zooming in, stop zooming\n')