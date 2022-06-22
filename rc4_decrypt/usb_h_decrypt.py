import sys

# Notice the key is hardcoded

def decryptRC4(data:str, key:str) -> str:
    S = list(range(256))
    j = 0
    out = b''

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
        out += (char ^ S[(S[i] + S[j]) % 256]).to_bytes(1, 'big')

    return out
       

key = "caixasuporte4232" 
EOF = b'\x00\x00\x00\x00'

encrypted_file = open(sys.argv[1], "rb")
decrypted_file = open(sys.argv[2], 'wb')

line = b''
while True:
    char = encrypted_file.read(1)

    if char:
        line += char
    else:
        break
    
    if line[-4:] == EOF:
        line = line[:-4]
        decrypted_file.write(decryptRC4(line, key))
        line = b''
