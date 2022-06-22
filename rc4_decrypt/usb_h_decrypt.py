#!/usr/bin/env python3.9

import sys

# Notice that the key is hardcoded. 
# If you have the `usb.h` file chances are this is the correct encryption key, as it's an early version.

def decryptRC4(data:str, key:str) -> str:
    S = list(range(256))
    j = 0
    out = ""

    #KSA Phase
    for i in range(256):
        j = (j + S[i] + ord( key[i % len(key)] )) % 256
        S[i] , S[j] = S[j] , S[i]  

    #PRGA Phase
    i = j = 0
    for char in data:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        out += (chr(ord(chr(char)) ^ S[(S[i] + S[j]) % 256]))

    return out
       

key = "caixasuporte4232" 

# Each line is encrypted individually and delimited by '0x00000000'
EOF = b'\x00\x00\x00\x00'

encrypted_file = open(sys.argv[0], "rb")
decrypted_file = open(sys.argv[1], 'w')

line = b''
while True:
    char = encrypted_file.read(1)

    if char:
        line += char
    else:
        # end of file
        break
    
    # check for delimiter
    if line[-4:] == EOF:
        line = line[:-4]
        decrypted_file.write(decryptRC4(line, key))
        line = b''
