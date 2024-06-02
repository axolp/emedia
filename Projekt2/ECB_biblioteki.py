from Crypto.PublicKey import RSA
from PIL import Image
import numpy as np
from Crypto.Cipher import PKCS1_OAEP


def generate_rsa_keys():
    key = RSA.generate(1024)  
    private_key = key.export_key()
    public_key = key.publickey().export_key()
   
    return private_key, public_key



def read_image(image_path):
    image = Image.open(image_path)
    image_data = np.array(image)
    return image_data.tobytes(), image.size, image.mode

def encrypt_blocks(blocks, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_blocks = [cipher.encrypt(block.ljust(block_size, b'\0')) for block in blocks]
    return encrypted_blocks

def write_encrypted_image(encrypted_blocks, image_size, image_mode, output_path):
    encrypted_data = b''.join(encrypted_blocks)
    image = Image.frombytes(image_mode, image_size, encrypted_data[:image_size[0] * image_size[1] * len(image_mode)])
    image.save(output_path)

def decrypt_blocks(encrypted_blocks, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_blocks = [cipher.decrypt(block).rstrip(b'\0') for block in encrypted_blocks]
    return decrypted_blocks



private_key, public_key = generate_rsa_keys()
print("Public Key:", public_key)
print("Private Key:", private_key)

image_path = 'lena.png'
image_data, image_size, image_mode = read_image(image_path)

# Rozbijanie danych na bloki o długości 6 bajtów
block_size = 6
blocks = [image_data[i:i+block_size] for i in range(0, len(image_data), block_size)]

encrypted_blocks = encrypt_blocks(blocks, public_key)

output_path = 'bib_ecb_encrypted_image.png'
write_encrypted_image(encrypted_blocks, image_size, image_mode, output_path)

decrypted_blocks = decrypt_blocks(encrypted_blocks, private_key)
write_encrypted_image(decrypted_blocks, image_size, image_mode, 'bib_ECB_decrypted_image.png')
