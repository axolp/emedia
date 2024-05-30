import numpy as np
from PIL import Image
from sympy import nextprime



class RSA:
    def mod_inverse(self, e, phi):
        x0, x1, y0, y1 = 0, 1, 1, 0
        phi0 = phi
        while e != 0:
            q = phi // e
            phi, e = e, phi % e
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        if phi != 1:
            return None  
        else:
            return x0 % phi0  

    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = 65537
        self.d = self.mod_inverse(self.e, self.phi)
        
        if self.d is None:
            raise ValueError("Nie można znaleźć odwrotności modularnej. Sprawdź wartości p, q, e.")
        
        self.public_key = [self.e, self.n]
        self.private_key = [self.d, self.n]

    def encrypt(self, m, public_key):
        e, n = public_key
        return pow(m, e, n)
    
    def decrypt(self, encrypted_message):
        return pow(encrypted_message, self.d, self.n)
def generate_large_primes():
    p = nextprime(10**56)
    q = nextprime(p + 10000)  # Dla różnorodności, wybieramy kolejną liczbę pierwszą po p+10000
    return p, q


def read_image(image_path):
    image = Image.open(image_path)
    image_data = np.array(image)
    return image_data.tobytes(), image.size, image.mode

def pad_block(block, block_size):
    return block.ljust(block_size, b'\0')

def encrypt_blocks(blocks, rsa, block_size):
    encrypted_blocks = []
    for block in blocks:
        padded_block = pad_block(block, block_size)
        block_int = int.from_bytes(padded_block, byteorder='big')
        encrypted_block_int = rsa.encrypt(block_int, rsa.public_key)
        encrypted_block = encrypted_block_int.to_bytes((encrypted_block_int.bit_length() + 7) // 8, byteorder='big')
        
        decrypted_block_int = rsa.decrypt(encrypted_block_int)
        decrypted_block = decrypted_block_int.to_bytes(block_size, byteorder='big')

        
    
        #'''
        if block != decrypted_block:
            print(f"Original block: {block}")
            print(f"Padded block (int): {block_int}")
            print(f"Encrypted block (int): {encrypted_block_int}")
            print(f"Encrypted block (bytes): {encrypted_block}")
            print(f"Decrypted block (int): {decrypted_block_int}")
            print(f"Decrypted block (bytes): {decrypted_block}")
    
            print("-" * 40)
        #'''
        
        encrypted_blocks.append(encrypted_block)
    return encrypted_blocks

def write_encrypted_image(encrypted_blocks, image_size, image_mode, output_path):
    encrypted_data = b''.join(encrypted_blocks)
    image = Image.frombytes(image_mode, image_size, encrypted_data[:image_size[0] * image_size[1] * len(image_mode)])
    image.save(output_path)

def decrypt_blocks(encrypted_blocks, rsa, block_size):
    decrypted_blocks = []
    for block in encrypted_blocks:
        block_int = int.from_bytes(block, byteorder='big')
        decrypted_block_int = rsa.decrypt(block_int)
        decrypted_block = decrypted_block_int.to_bytes(block_size, byteorder='big')
        decrypted_blocks.append(decrypted_block)

    return decrypted_blocks

# Generowanie kluczy RSA
#p = 4999999  # przykładowa liczba pierwsza
#q = 4999963  # przykładowa liczba pierwsza
p, q = generate_large_primes()
rsa = RSA(p, q)

# Wczytanie danych obrazu
image_path = 'image.png'
image_data, image_size, image_mode = read_image(image_path)
print(image_size)
print(len(image_data))

# Rozbicie danych na bloki
block_size = 20
blocks = [image_data[i:i+block_size] for i in range(0, len(image_data), block_size)]

# Szyfrowanie bloków
encrypted_blocks = encrypt_blocks(blocks, rsa, block_size)

# Zapisanie zaszyfrowanego obrazu
output_path = 'encrypted_image.png'
write_encrypted_image(encrypted_blocks, image_size, image_mode, output_path)

# Odszyfrowanie bloków
decrypted_blocks = decrypt_blocks(encrypted_blocks, rsa, block_size)
write_encrypted_image(decrypted_blocks, image_size, image_mode, 'decrypted_image.png')
