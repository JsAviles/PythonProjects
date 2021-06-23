###########################################################
# File: RSA_Encryption.py (Source code)                   #
# Author: Jesus Sebastian Aviles                          #
###########################################################

#Prime Check function
def prime_Check(num):
    if num < 1 :
        print("Invalid entry: Please try again.")
        return False
    elif num == 1 :
        print("Invalid entry: 1 is not a Prime Number, please try again.")
        return False
    else :
        for i in range (2, (num//2)): #only check up to num//2 because anything higher will never equal a whole number
            if ((num % i) == 0) :
                print("Invalid entry: Not a Prime Number, please try again.")
                return False
    return True

#Check to see if values in argument are relatively prime --> GCD = 1
def rprime_Check(div, r):
    gcd = div % r
    #keep checking for gcd until the remainder becomes 0
    while(gcd != 0):
        div = r
        r = gcd
        gcd = div % r
    return r
        
#Calculate phi(n) = (p-1)(q-1) for prime numbers
def calc_phi(P, Q):
    return ((P-1)*(Q-1))

#Calculate e, e must be relatively prime to phi(n)
def calc_e(PHI):
    euler = 2
    flag = True
    while((euler < PHI) & flag):
        if (rprime_Check(euler, PHI)==1):
            flag = False
        else :
            euler += 1
    return euler

#Calculate private key d
def calc_d(PHI, E):
    flag = True
    k = 1
    while (flag):
        #if e divides (i*phi + 1) evenly then 
        if (((k*PHI)+1) % E) == 0 :
            privateKey = ((k*PHI)+1)//E
            flag = False
            return privateKey
        else :
            k+=1

#Encryption functions
def encryptMessage(plainText, N,E):
    string = []
    size = 0

    #add all the characters of the plainText into a string array for manipulation into M blocks
    for elem in plainText:
        string.append(ord(elem))
        size += 1

    numBlocks = size//3
    #check to see if you need 1 more block for last 1-2 characters if there is not enough to make full blocks of length 3
    if(size % 3 > 0):
        numBlocks += 1

    #create an array/list that will house each block cipher of length 3
    mBlocks = []

    ctr = 0

    #traverse the string array and slice it into equal blocks of length 3 with the encoded value of each character. a-z + space = 1-27
    for i in range(numBlocks):
        block = []
        for j in range(3):
            if ctr==size : #need to pad with zeroes
                block.append(0)
            elif string[ctr] == 32:  #check if char is a space
                block.append(string[ctr]-5)
                ctr += 1
            #if character is not a space, add the ascii value - 96 ( for purpose of mapping 1-26)
            else : 
                block.append(string[ctr]-96)
                ctr += 1
        mBlocks.append(block)

    m = []

    for i in range(numBlocks):
        m.append(((mBlocks[i][0]*(28**2)) + (mBlocks[i][1]*28) + (mBlocks[i][2])))
    #end message slicing into blocks

    #Simple print message--> no calculations are done here
    print("\nEncrypting plaintext: ", end = '')
    for elem in string:
        if elem == 32 :
            print(chr(elem), end = '')
        elif elem > 96 & elem < 123 : 
            print(chr(elem), end = '')
    
    #encrypt
    c=[]
    for elem in m:
        c.append(((elem**E) % N))

    #print statements for public key, private key and cipher text
    print("\n\nPublic key (e, n) is: (",end = '')
    print(E, end = '')
    print(",", N, end = '')
    print(")")  

    print("\nCipher text: ", end = '')
    for i in range(numBlocks):
        print(c[i], end = ' ')
    print("\nMessage block cipher length = 3 --> m-block values are separated by a space\n")
    return c

#decryption function takes in ciphertext, public key n and private key d for decoding
def decryptMessage(cText,N,D):
    print("Private key d:",D)

    #decrypt Cipher text blocks into Message block m
    mDecrypt = []
    for elem in cText:
        mDecrypt.append(((elem**D) % N))

    #Decode plaintext from message blocks m into readable print
    temp = 0
    rem = 0
    pText = []
    for elem in mDecrypt:
        temp = elem
        rem = (temp//(28**2))
        pText.append(rem)
        temp = temp - ((28**2)*rem)
        rem = temp//28
        pText.append(rem)
        temp = temp - (28*rem)
        rem = temp
        pText.append(rem)   

    #print to readable ascii values
    print("Decrypted Ciphertext: ", end= '')
    for elem in pText:
        if elem == 27:
            print(chr(elem+5), end = '')
        elif elem != 0:
            print(chr(elem+96), end = '')
    print("\n")

'''
Main
'''
#begin user input of p and q
#boolean flags for conduction a prime check and n,p,q initialization
pCheck = False
qCheck = False
pqCheck = True
nCheck = False
n=0
p=0
q=0

#major loop for allowing user to input values of p and q, as well as prime checks for p/q, and an n check to ensure that n is larger than the maximum value of a block
while(nCheck != True):
    #p initialization loop
    while (pCheck != True):
        p = int(input("Enter a prime number for p: "))
        pCheck = prime_Check(int(p))

    #q initializtion loop
    while (qCheck != True & pqCheck):
        q = int(input("Enter a prime number for q: "))            
        #check if p and q are the same prime numbers                                     
        if (p == q) :
            print("Invalid entry: p cannot be equal to q, please try again.")
        #if p and q are not equal then check if the entry for q is a prime number
        else :
            qCheck = prime_Check(int(q))
    #check if n is less than the maximum value of a block (28^3-1)
    #and if it is, ask user to re enter larger values for p and q
    n = (p*q)
    if ((n)<= ((28**3)-1)): 
        print("Invalid entry: inputs are not compatible with block length, re-enter larger values for p and q.")
        pCheck = False
        qCheck = False
        #Reset flags to choose new p and q
    elif ((n) > ((28**3)-1)):
        nCheck = True
#end p and q user input

#begin plaintext slicing into m blocks of length 3
Plaintext = input("\nPlease enter the desired plaintext to encrypt with the following Properties:\n1) only lower-case letters 'a-->z'\n2) no special characters allowed except for 'SPACE'\n\n")

#Calculate required variables
phi = calc_phi(p,q)
e = calc_e(phi)
d = calc_d(phi, e)

Ciphertext = encryptMessage(Plaintext, n, e)
decryptMessage(Ciphertext, n, d)
'''
End Main
'''