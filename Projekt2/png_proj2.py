from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import RSA
import binascii


def readMetaData(file_name):
    with open(file_name, 'rb') as file:
        return file.read()

def writeMetaData(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)  

def find_all(haystack, needle):
    start = 0
    while True:
        start = haystack.find(needle, start)
        if start == -1:  
            break
        yield start
        start += len(needle) 

#def into_block_into_ascii(n, data):



def change_length_insert_ciphered_data(ciphered_data):
    n= len(ciphered_data) #//2
    idat= ""
    if n!= 0:
        data_len= str(hex(n//2)[2:]).zfill(8)#dziele przez dwa bo ma byc liczba 
        print("data len in hex: ",data_len)
        idat= data_len + "49444154" + ciphered_data + "00000000"   #na koncu crc
       
    return idat
def from_ascii_to_hex(data):
    hex_codes= {
    '65': 'A',
    '66': 'B',
    '67': 'C',
    '68': 'D',
    '69': 'E',
    '70': 'F',
    '48': '0',
    '49': '1',
    '50': '2',
    '51': '3',
    '52': '4',
    '53': '5',
    '54': '6',
    '55': '7',
    '56': '8',
    '57': '9',
    '99': 'break'
    }
    data= str(data)
    #print(data)
    decyphered_data= ""
    for i in range(0, len(data)-1, 2):
        pair= data[i]+data[i+1]
        #print(pair)
        hex= hex_codes[pair]
        if hex == "break":
            break
        decyphered_data+=hex

    return decyphered_data

def turn_to_ASCII(data):
    
    ascii_data= ""
    ascii_codes = {
    'A': 65,
    'B': 66,
    'C': 67,
    'D': 68,
    'E': 69,
    'F': 70,
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57
    #dodaje dodatkowy znak 99 dla paddingu
    }
    for b in data:
        #print(b)
        ascii_data+= str(ascii_codes[b.upper()])
    #print("ascii data: ", ascii_data)
    
    return int(ascii_data)
    

def encrypt_png_data(data, block_n):
    global encoder, decoder
    encrypted_data= ""
    padding_idx= len(data) - (len(data)%block_n) 
    leftovers= len(data)%block_n
    for i in range(1, len(data)):
        if i == padding_idx:
            #zastosuj padiing
            break

        if i % block_n == 0:
            block_data= data[i-block_n:i]
            #print("block data", block_data)
            ascii_data= turn_to_ASCII(block_data)
            encrypted_block= encoder.encrypt(ascii_data, decoder.public_key)
            str_encrypted_block= str(encrypted_block)
            decrypted_block= decoder.decrypt(int(encrypted_block))
            print("ascii data:", ascii_data, "encrypted: ", encrypted_block, "decrypted_ascii: ", decrypted_block, "decrypoted_hex: ", from_ascii_to_hex(decrypted_block))
            encrypted_data+= str(encrypted_block)

    print("padding idx:", padding_idx,"leftovers: ", leftovers)
    if leftovers != 0:
        padding_data= data[padding_idx:padding_idx+leftovers]
        print("padding data:", padding_data)
        ascii_padding= str(turn_to_ASCII(padding_data))
        for j in range(block_n - leftovers):
            ascii_padding+="99"
        
        encrypted_padding= encoder.encrypt(int(ascii_padding), decoder.public_key)
        encrypted_data+= str(encrypted_padding)

    return encrypted_data

def rsa_image():
  
    binary_file = readMetaData("image.png")
    hex_data = binary_file.hex()

    indexes = list(find_all(hex_data, '49444154'))
    middle= ""

    left_idx= indexes[0]
    left= hex_data[:left_idx-8]

    right_idx= hex_data.find('49454e44')
    right= hex_data[right_idx-8:]

    

    for i, idx in enumerate(indexes):
        #zamien dane z idat na zaszyfrowane dane
        data_len= int(hex_data[idx-8:idx], 16)*2 #ilosc znakow 16 do oczytania 
        #print("next idat:", hex_data[idx+8+data_len+8:idx+8+data_len+8+8+8])
        idat_data= hex_data[idx+8:idx+8+data_len]
        encrypted_data= encrypt_png_data(idat_data, 3)
        middle+= change_length_insert_ciphered_data(encrypted_data)
    new_hex_data= left + middle + right
   
          
    #print("position 8032007", new_hex_data[8032007])
    new_binary_data = bytes.fromhex(new_hex_data)
    #new_binary_data = binascii.unhexlify(new_hex_data)
    writeMetaData("ciphered_img.png", new_binary_data)

def read_rsa_iamge(path):
    binary_file = readMetaData(path)
    hex_data = binary_file.hex()
    #print(hex_data)

    indexes = list(find_all(hex_data, '49444154'))
    middle= ""

    indexes = list(find_all(hex_data, '49444154'))
    middle= ""

    left_idx= indexes[0]
    left= hex_data[:left_idx-8]

    right_idx= hex_data.find('49454e44')
    right= hex_data[right_idx-8:]
    print(left)
    print(right)

    for idx in indexes:
        print(hex_data[idx-8:idx+8])
        data_len= int(hex_data[idx-8:idx], 16)*2
        print("data len:", data_len)
        print("data: ", hex_data[idx+8:idx+8+data_len])




#encoder = RSA.RSA(1299821, 1299827)  
#decoder = RSA.RSA(1299811, 1299817) # n to 1 689 516 434 587 pozwala na blok o dlugosci 6

encoder = RSA.RSA(101, 7001)  
decoder = RSA.RSA(101, 7001) # n to 1 689 516 434 587 pozwala na blok o dlugosci 6

#encoder = RSA.RSA(4999999, 4999963)  
#decoder = RSA.RSA(4999991, 4999957) # n to 1 689 516 434 587 pozwala na blok o dlugosci 6
rsa_image()
#read_rsa_iamge("ciphered_img.png")
