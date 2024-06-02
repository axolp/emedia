import numpy as np
from PIL import Image
from sympy import nextprime
import os

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
        
        
        
        self.public_key = [self.e, self.n]
        self.private_key = [self.d, self.n]

    def encrypt(self, m, public_key):
        e, n = public_key
        return pow(m, e, n)
    
    def decrypt(self, encrypted_message):
        return pow(encrypted_message, self.d, self.n)

def read_image(image_path):
    image = Image.open(image_path)
    image_data = np.array(image)
    return image_data.tobytes(), image.size, image.mode

def pad_block(block, block_size):
    return block.ljust(block_size, b'\0')

def generate_iv(block_size):
    return os.urandom(block_size)

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt_blocks_cbc(blocks, rsa, block_size, iv):
    encrypted_blocks = []
    previous_block = iv
    for block in blocks:
        padded_block = pad_block(block, block_size)
        xored_block = xor_bytes(padded_block, previous_block)
        block_int = int.from_bytes(xored_block, byteorder='big')
        encrypted_block_int = rsa.encrypt(block_int, rsa.public_key)
        encrypted_block = encrypted_block_int.to_bytes((encrypted_block_int.bit_length() + 7) // 8, byteorder='big')
        encrypted_blocks.append(encrypted_block)
        previous_block = encrypted_block
    return encrypted_blocks

def decrypt_blocks_cbc(encrypted_blocks, rsa, block_size, iv):
    decrypted_blocks = []
    previous_block = iv
    for block in encrypted_blocks:
        block_int = int.from_bytes(block, byteorder='big')
        decrypted_block_int = rsa.decrypt(block_int)
        decrypted_block = decrypted_block_int.to_bytes(block_size, byteorder='big')
        xored_block = xor_bytes(decrypted_block, previous_block)
      
        decrypted_blocks.append(xored_block)
        previous_block = block
    return decrypted_blocks

def write_encrypted_image(encrypted_blocks, image_size, image_mode, output_path):
    encrypted_data = b''.join(encrypted_blocks)
    image = Image.frombytes(image_mode, image_size, encrypted_data[:image_size[0] * image_size[1] * len(image_mode)])
    image.save(output_path)


def generate_large_primes():
    p = nextprime(10**5)
    q = nextprime(p + 10000)
    return p, q

p, q = generate_large_primes()
rsa = RSA(p, q)

image_path = 'lena.png'
image_data, image_size, image_mode = read_image(image_path)
print(image_size)
print(len(image_data))


block_size = 4
blocks = [image_data[i:i+block_size] for i in range(0, len(image_data), block_size)]


iv = generate_iv(block_size)


encrypted_blocks = encrypt_blocks_cbc(blocks, rsa, block_size, iv)


output_path = 'cbc_encrypted_image.png'
write_encrypted_image(encrypted_blocks, image_size, image_mode, output_path)

decrypted_blocks = decrypt_blocks_cbc(encrypted_blocks, rsa, block_size, iv)
write_encrypted_image(decrypted_blocks, (100, 100), image_mode, 'cbc_decrypted_image.png')
