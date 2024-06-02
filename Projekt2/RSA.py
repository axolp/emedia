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
        self.e = 65537  # typowa
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


Alice = RSA(1299821, 1299827)  
Bob = RSA(1299811, 1299817) # n to 1 689 516 434 587 pozwala na blok o dlugosci 6

# Alice wysyła do Boba
cipher_text = Alice.encrypt(70, Bob.public_key)
#print("zaszyfrowane: ", cipher_text)
#print("odszyfrowane: ", Bob.decrypt(cipher_text))

# Bob wysyła do Alice
cipher_text2 = Bob.encrypt(707070707070, Alice.public_key)
#print("zaszyfrowane: ", cipher_text2)
#print("odszyfrowane: ", Alice.decrypt(cipher_text2))
