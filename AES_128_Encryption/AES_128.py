###########################################################
# File: AES_128.py (Source code)                          #
# Author: Jesus Sebastian Aviles                          #
###########################################################

'''
The demofile.txt is where the plaintext resides before encryption and it will be overriden after encryption takes place.

User will be prompted to enter a 16 character key which will be used for encryption.
'''
import codecs, binascii, sys

def encryptFile(file_reference, encrypkey):
    sbox = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76], 
            [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0], 
            [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15], 
            [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
            [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84], 
            [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf], 
            [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8], 
            [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2], 
            [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73], 
            [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb], 
            [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
            [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08], 
            [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a], 
            [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e], 
            [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf], 
            [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]
    ark = []
    rc  =  [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    w0 = []
    w1 = []
    w2 = []
    w3 = []
    gw = [0x00, 0x00, 0x00, 0x00]
    temp = [0x00, 0x00, 0x00, 0x00]
    state = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    tempstate = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    mc = [0x02, 0x03, 0x01, 0x01, 0x01, 0x02, 0x03, 0x01, 0x01, 0x01, 0x02, 0x03,0x03, 0x01, 0x01, 0x2]
    roundctr = 0
    key = []

    for elem in encrypkey:
        key.append(elem.encode().hex())
    
    filename = file_reference
    index = 0
    with open(filename, 'r+') as ptext:
        hasChar = ptext.readline()
        while hasChar:
            for elem in hasChar:                                #check txt file char by char (including spaces)
                hexElem = elem.encode().hex()                   #convert to hex
                state[index]=(hexElem)
                index += 1
            hasChar = ptext.readline()                          #check if there is another line of text
    print('Message to HEX        -', state)
    index = 0

    output = open('Round_Keys.txt', 'w+')
    rewrite = open(filename, 'w+')
    #Add Roundkey, Round 0 Message(State) XOR key 0

    for i in range (16):
        state[i] = (hex(int(bin(int(state[i],16) ^ int(key[i],16)),2)))
    #output text with all the round keys saved
    output.write('Round 0: ')   
    for i in range (16):
        output.write('0x')
        output.write(key[i])
        output.write(', ')
    output.write('\n')

    #begin encryption loop
    while roundctr < 10:
        print(' ****** ROUND ', roundctr+1,' ******')
        #Round 1: Substitute Bytes (S-Box) with current state matrix
        for i in range (16):
            state[i] = hex(sbox[int(state[i],16)//16][int(state[i],16)%16])

        print('After Substitute Byte                      :', state)
        #Round 1: Shift Row 1
        j=0
        for i in range (1,14,4):
            temp[j]=(state[i])
            j+=1
        j=1
        for i in range (1,14,4):
            if i < 13:
                state[i] = temp[j]
                j+=1
            else:
                state[i] = temp[0]
        j=0

        #Shift row 2
        for i in range (2,15,4):
            temp[j]=(state[i])
            j+=1
        j=2
        for i in range (2,15,4):
            if i < 10:
                state[i] = temp[j]
                j+=1
            elif i == 10:
                state[i] = temp[0]
            else:
                state[i] = temp[1]	
        j=0

        #Shift row 3
        for i in range (3,16,4):
            temp[j]= (state[i])
            j+=1
        j=0
        for i in range (3,16,4):
            if i > 5:
                state[i] = temp[j]
                j+=1
            else:
                state[i] = temp[3]	
        j=0

        print('After Shift Rows                           :', state)
        #Round 1: Mix Column Multiples
        
        if roundctr < 9:
            #Column 1 row 1 prime
            check1 = int(state[0],16)
            check2 = int(state[1],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[0]=(hex(int(bin((int(state[0],16) * int(mc[0])) ^ (int(state[1],16)) ^ (int(state[1],16) * int(mc[0]))^(int(state[2],16))^ (int(state[3],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[0]=(hex(int(bin(int(check1,2) ^ (int(state[1],16) * int(mc[0])) ^ (int(state[1],16)) ^ (int(state[2],16)) ^ (int(state[3],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[0]=(hex(int(bin((int(state[0],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[1],16)) ^ (int(state[2],16)) ^ (int(state[3],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[0]=(hex(int(bin(int(check1,2)  ^ int(check2,2) ^ (int(state[1],16)) ^ (int(state[2],16)) ^ (int(state[3],16))),2)))

            #Column 1 row 2 prime
            check1 = int(state[1],16)
            check2 = int(state[2],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[1]=(hex(int(bin((int(state[0],16)) ^ (int(state[1],16) * int(mc[0])) ^ (int(state[2],16)) ^ (int(state[2],16) * int(mc[0])) ^ (int(state[3],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[1]=(hex(int(bin((int(state[0],16)) ^ int(check1,2) ^ (int(state[2],16) * int(mc[0])) ^ (int(state[2],16)) ^ (int(state[3],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[1]=(hex(int(bin((int(state[0],16)) ^ (int(state[1],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[2],16)) ^ (int(state[3],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[1]=(hex(int(bin( int(check1,2)  ^ int(check2,2) ^ (int(state[2],16)) ^ (int(state[0],16)) ^ (int(state[3],16))),2)))

            #Column 1 row 3 prime
            check1 = int(state[2],16)
            check2 = int(state[3],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[2]=(hex(int(bin((int(state[0],16)) ^ (int(state[1],16))  ^ (int(state[2],16) * int(mc[0])) ^ (int(state[3],16) * int(mc[0])) ^ (int(state[3],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[2]=(hex(int(bin((int(state[0],16)) ^ (int(state[1],16)) ^ int(check1,2) ^ (int(state[3],16) * int(mc[10])) ^ (int(state[3],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[2]=(hex(int(bin((int(state[0],16)) ^ (int(state[1],16))  ^ (int(state[2],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[3],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[2]=(hex(int(bin((int(state[0],16)) ^ (int(state[1],16)) ^ int(check1,2) ^ int(check2,2) ^ (int(state[3],16))),2)))

            #Column 1 row 4 prime
            check1 = int(state[0],16)
            check2 = int(state[3],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[3]=(hex(int(bin((int(state[0],16) * int(mc[0])) ^ (int(state[0],16))^ (int(state[1],16)) ^ (int(state[2],16))  ^ (int(state[3],16) * int(mc[0]))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[3]=(hex(int(bin(int(check1,2) ^ (int(state[0],16)) ^ (int(state[1],16)) ^ (int(state[2],16))  ^ (int(state[3],16) * int(mc[0]))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[3]=(hex(int(bin((int(state[0],16) * int(mc[0])) ^ (int(state[0],16))^ (int(state[1],16)) ^ (int(state[2],16))  ^ int(check2,2)),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[3]=(hex(int(bin(int(check1,2) ^ (int(state[0],16)) ^ (int(state[1],16)) ^ (int(state[2],16))  ^ int(check2,2)),2)))

            #Column 2 row 1 prime
            check1 = int(state[4],16)
            check2 = int(state[5],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[4]=(hex(int(bin((int(state[4],16) * int(mc[0])) ^ (int(state[5],16)) ^ (int(state[5],16) * int(mc[0])) ^ (int(state[6],16)) ^ (int(state[7],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[4]=(hex(int(bin(int(check1,2) ^ (int(state[5],16) * int(mc[0])) ^ (int(state[5],16)) ^ (int(state[6],16)) ^ (int(state[7],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[4]=(hex(int(bin((int(state[4],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[5],16)) ^ (int(state[6],16)) ^ (int(state[7],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[4]=(hex(int(bin(int(check1,2)  ^ int(check2,2) ^ (int(state[5],16)) ^ (int(state[6],16)) ^ (int(state[7],16))),2)))

            #Column 2 row 2 prime
            check1 = int(state[5],16)
            check2 = int(state[6],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[5]=(hex(int(bin((int(state[4],16)) ^ (int(state[5],16) * int(mc[0])) ^ (int(state[6],16)) ^ (int(state[6],16) * int(mc[0])) ^ (int(state[7],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[5]=(hex(int(bin((int(state[4],16)) ^ int(check1,2) ^ (int(state[6],16) * int(mc[0])) ^ (int(state[6],16)) ^ (int(state[7],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[5]=(hex(int(bin((int(state[4],16)) ^ (int(state[5],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[6],16)) ^ (int(state[7],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[5]=(hex(int(bin(int(check1,2) ^ int(check2,2) ^ (int(state[6],16)) ^ (int(state[4],16)) ^ (int(state[7],16))),2)))

            #Column 2 row 3 prime
            check1 = int(state[6],16)
            check2 = int(state[7],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[6]=(hex(int(bin((int(state[4],16)) ^ (int(state[5],16))  ^ (int(state[6],16) * int(mc[0])) ^ (int(state[7],16) * int(mc[0])) ^ (int(state[7],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[6]=(hex(int(bin((int(state[4],16)) ^ (int(state[5],16)) ^ int(check1,2) ^ (int(state[7],16) * int(mc[0])) ^ (int(state[7],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[6]=(hex(int(bin((int(state[4],16)) ^ (int(state[5],16))  ^ (int(state[6],16) * int(mc[0])) ^ int(check2,2) ^(int(state[7],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[6]=(hex(int(bin((int(state[4],16)) ^ (int(state[5],16)) ^ int(check1,2) ^ int(check2,2) ^(int(state[7],16))),2)))

            #Column 2 row 4 prime
            check1 = int(state[4],16)
            check2 = int(state[7],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[7]=(hex(int(bin((int(state[4],16) * int(mc[0])) ^ (int(state[4],16))^ (int(state[5],16)) ^ (int(state[6],16))  ^ (int(state[7],16) * int(mc[0]))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[7]=(hex(int(bin(int(check1,2) ^ (int(state[4],16)) ^ (int(state[5],16)) ^ (int(state[6],16))  ^ (int(state[7],16) * int(mc[0]))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[7]=(hex(int(bin((int(state[4],16) * int(mc[0])) ^ (int(state[4],16)) ^ (int(state[5],16)) ^ (int(state[6],16))  ^ int(check2,2)),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[7]=(hex(int(bin(int(check1,2) ^ (int(state[4],16)) ^ (int(state[5],16)) ^ (int(state[6],16))  ^ int(check2,2)),2)))

            #Column 3 row 1 prime
            check1 = int(state[8],16)
            check2 = int(state[9],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[8]=(hex(int(bin((int(state[8],16) * int(mc[0])) ^ (int(state[9],16)) ^ (int(state[9],16) * int(mc[0]))^(int(state[10],16))^ (int(state[11],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[8]=(hex(int(bin(int(check1,2) ^ (int(state[9],16) * int(mc[0])) ^ (int(state[9],16)) ^ (int(state[10],16))^ (int(state[11],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[8]=(hex(int(bin((int(state[8],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[9],16)) ^ (int(state[10],16))^ (int(state[11],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[8]=(hex(int(bin(int(check1,2)  ^ int(check2,2) ^ int(state[9],16) ^ (int(state[10],16)) ^ (int(state[11],16))),2)))

            #Column 3 row 2 prime
            check1 = int(state[9],16)
            check2 = int(state[10],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[9]=(hex(int(bin((int(state[8],16)) ^ (int(state[9],16) * int(mc[0])) ^ (int(state[10],16) ^ (int(state[10],16)) * int(mc[0])) ^ (int(state[11],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[9]=(hex(int(bin((int(state[8],16)) ^ int(check1,2) ^ (int(state[10],16) * int(mc[0])) ^ (int(state[10],16)) ^ (int(state[11],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[9]=(hex(int(bin((int(state[8],16)) ^ (int(state[9],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[10],16)) ^ (int(state[11],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[9]=(hex(int(bin(int(check1,2)  ^ int(check2,2) ^ (int(state[10],16)) ^ (int(state[8],16)) ^ (int(state[11],16))),2)))

            #Column 3 row 3 prime
            check1 = int(state[10],16)
            check2 = int(state[11],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[10]=(hex(int(bin((int(state[8],16)) ^ (int(state[9],16))  ^ (int(state[10],16) * int(mc[0])) ^ (int(state[11],16) * int(mc[0])) ^ (int(state[11],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[10]=(hex(int(bin((int(state[8],16)) ^ (int(state[9],16)) ^ int(check1,2) ^ (int(state[11],16) * int(mc[0])) ^ (int(state[11],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[10]=(hex(int(bin((int(state[8],16)) ^ (int(state[9],16))  ^ (int(state[10],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[11],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[10]=(hex(int(bin((int(state[8],16)) ^ (int(state[9],16)) ^ int(check1,2) ^ int(check2,2) ^ (int(state[11],16))),2)))

            #Column 3 row 4 prime
            check1 = int(state[8],16)
            check2 = int(state[11],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[11]=(hex(int(bin((int(state[8],16) * int(mc[0])) ^ int(state[8],16) ^ int(state[9],16) ^ int(state[10],16)  ^ (int(state[11],16) * int(mc[0]))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[11]=(hex(int(bin(int(check1,2) ^ int(state[8],16) ^ int(state[9],16) ^ int(state[10],16)  ^ (int(state[11],16) * int(mc[0]))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[11]=(hex(int(bin((int(state[8],16) * int(mc[0])) ^ (int(state[8],16))^ (int(state[9],16)) ^ (int(state[10],16))  ^ int(check2,2)),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[11]=(hex(int(bin( int(check1,2) ^ int(state[8],16) ^ int(state[9],16) ^ int(state[10],16)  ^ int(check2,2)),2)))

            #Column 4 row 1 prime
            check1 = int(state[12],16)
            check2 = int(state[13],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[12]=(hex(int(bin((int(state[12],16) * int(mc[0])) ^ (int(state[13],16)) ^ (int(state[13],16) * int(mc[0])) ^ (int(state[14],16)) ^ (int(state[15],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[12]=(hex(int(bin(int(check1,2) ^ (int(state[13],16) * int(mc[0])) ^ (int(state[13],16)) ^ (int(state[14],16)) ^ (int(state[15],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[12]=(hex(int(bin((int(state[12],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[13],16)) ^ (int(state[14],16)) ^ (int(state[15],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[12]=(hex(int(bin(int(check1,2) ^ int(check2,2) ^ (int(state[13],16)) ^ (int(state[14],16)) ^ (int(state[15],16))),2)))

            #Column 4 row 2 prime
            check1 = int(state[13],16)
            check2 = int(state[14],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[13]=(hex(int(bin((int(state[12],16)) ^ (int(state[13],16) * int(mc[5])) ^ (int(state[14],16)) ^ (int(state[14],16) * int(mc[0])) ^ (int(state[15],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[13]=(hex(int(bin((int(state[12],16)) ^ int(check1,2) ^ (int(state[14],16) * int(mc[0])) ^ (int(state[14],16)) ^ (int(state[15],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[13]=(hex(int(bin((int(state[12],16)) ^ (int(state[13],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[14],16)) ^ (int(state[15],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[13]=(hex(int(bin((int(state[12],16)) ^ (int(state[15],16)) ^ int(check1,2) ^ int(check2,2) ^ (int(state[14],16))),2)))

            #Column 4 row 3 prime
            check1 = int(state[14],16)
            check2 = int(state[15],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[14]=(hex(int(bin((int(state[12],16)) ^ (int(state[13],16))  ^ (int(state[14],16) * int(mc[0])) ^ (int(state[15],16) * int(mc[0])) ^ (int(state[15],16))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[14]=(hex(int(bin((int(state[12],16)) ^ (int(state[13],16)) ^ int(check1,2) ^ (int(state[15],16) * int(mc[0])) ^ (int(state[15],16))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[14]=(hex(int(bin((int(state[12],16)) ^ (int(state[13],16)) ^ (int(state[14],16) * int(mc[0])) ^ int(check2,2) ^ (int(state[15],16))),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[14]=(hex(int(bin((int(state[12],16)) ^ (int(state[13],16)) ^ int(check1,2) ^ int(check2,2) ^ (int(state[15],16))),2)))

            #Column 4 row 4 prime
            check1 = int(state[12],16)
            check2 = int(state[15],16)
            if (check1 < 128) & (check2 < 128):
                tempstate[15]=(hex(int(bin((int(state[12],16) * int(mc[0])) ^ (int(state[12],16)) ^ (int(state[13],16)) ^ (int(state[14],16))  ^ (int(state[15],16) * int(mc[0]))),2)))
            elif (check1 >= 128) & (check2 < 128):
                check1 = bin((check1 << 1)^0b100011011)
                tempstate[15]=(hex(int(bin(int(check1,2) ^ (int(state[12],16)) ^ (int(state[13],16)) ^ (int(state[14],16))  ^ (int(state[15],16) * int(mc[0]))),2)))
            elif (check2 >=128) & (check1 < 128):
                check2 = bin((int(check2) << 1)^0b100011011)
                tempstate[15]=(hex(int(bin((int(state[12],16) * int(mc[0])) ^ (int(state[12],16)) ^ (int(state[13],16)) ^ (int(state[14],16)) ^ int(check2,2)),2)))
            else:
                check1 = bin((check1 << 1)^0b100011011)
                check2 = bin((check2 << 1)^0b100011011)
                tempstate[15]=(hex(int(bin(int(check1,2) ^ (int(state[12],16)) ^ (int(state[13],16)) ^ (int(state[14],16)) ^ int(check2,2)),2)))

            #populate the new state after being Mix Column Multiplied
            for i in range (16):
                state[i] = tempstate[i]
        if roundctr < 9:
            print('After Mix Columns                          :', state)

        #begin calculation on roundkey
        j=0
        if roundctr < 1:
            for i in range (4):
                w0.append(key[j%16])
                j+=1
            for i in range (4):
                w1.append(key[j%16])
                j+=1
            for i in range (4):
                w2.append(key[j%16])
                j+=1
            for i in range (4):
                w3.append(key[j%16])
                j+=1
            j=0
        else:
            for i in range (4):
                w0[i]=(key[j%16])
                j+=1
            for i in range (4):
                w1[i]=(key[j%16])
                j+=1
            for i in range (4):
                w2[i]=(key[j%16])
                j+=1
            for i in range (4):
                w3[i]=(key[j%16])
                j+=1
            j=0
        #shift bytes left (g(w3))
        gw[0] = (w3[1])
        gw[1] = (w3[2])
        gw[2] = (w3[3])
        gw[3] = (w3[0])

        #Byte substituion (S-Box) using g(w3)
        for i in range (4):
            gw[i] = hex(sbox[int(gw[i],16)//16][int(gw[i],16)%16]) 		#[row][column] for S-Box Substitution

        gw[0] = hex(int(bin(int(gw[0],16) ^ int(rc[roundctr])),2))		#converts the hex values to binary, computes XOR with round constant then converts to int then back to hex

        w4 = [0x00,0x00,0x00,0x00]
        w5 = [0x00,0x00,0x00,0x00]
        w6 = [0x00,0x00,0x00,0x00]
        w7 = [0x00,0x00,0x00,0x00]

        #round of XORS
        for i in range (4):
            w4[i]=(hex(int(bin(int(w0[i],16) ^ int(gw[i],16)),2)))
        for i in range (4):
            w5[i]=(hex(int(bin(int(w4[i],16) ^ int(w1[i],16)),2)))
        for i in range (4):
            w6[i]=(hex(int(bin(int(w5[i],16) ^ int(w2[i],16)),2)))
        for i in range (4):
            w7[i]=(hex(int(bin(int(w6[i],16) ^ int(w3[i],16)),2)))

        #update key
        for i in range (4):
            key[i] = w4[i]
        for i in range (4,8):
            key[i] = w5[i-4]
        for i in range (8,12):
            key[i] = w6[i-8]
        for i in range (12,16):
            key[i] = w7[i-12]

        for r in range (16):
            state[r] =(hex(int(bin(int(state[r],16) ^ int(key[r],16)),2)))
        output.write('Round ')
        output.write('{}'.format(roundctr+1))
        output.write(': ')
        for i in range (16):
            output.write(key[i])
            output.write(', ')
        output.write('\n')
        
        print('Cipher Text                                :', state)
        print('Updated key                                :', key)

        roundctr += 1
    output.close()

    for i in range (16):
        hs = state[i][2:].encode().hex()
        bs = bytes.fromhex(hs)
        rewrite.write(bs.decode("ASCII"))
        rewrite.write(' ')
#End Encryption Function

#main
encrypkey = input("Enter 16 character Key: \n")
encryptFile('demofile.txt', encrypkey)