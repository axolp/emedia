from Crypto.PublicKey import RSA
from PIL import Image
import numpy as np
from Crypto.Cipher import PKCS1_OAEP


def decrypt_blocks(encrypted_blocks, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_blocks = [cipher.decrypt(block).rstrip(b'\0') for block in encrypted_blocks]
    return decrypted_blocks

decrypted_blocks = decrypt_blocks(encrypted_blocks, private_key)
write_encrypted_image(decrypted_blocks, image_size, image_mode, 'decrypted_image.png')
