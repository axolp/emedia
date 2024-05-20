class RSA:
    
    def mod_inverse(self, e, phi):
        for d in range(3, phi):
            if (d*e)%phi == 1:
                return d
            
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q # moze tylko prawidlwoo kodawc liczby mniejsze od n
        self.phi = (p - 1) * (q - 1)
        self.e = 7 
        self.d = self.mod_inverse(self.e, self.phi)  # Adjusted private key calculation
        
        self.public_key = [self.e, self.n]
        self.private_key= [self.d, self.n]

    def encrypt(self, m, public_key):
        e= public_key[0]
        n= public_key[1]
        return pow(m, e)%n
    
    def decrypt(self, encrypted_message):
        return pow(encrypted_message, self.d, self.n)
    

    
Alice= RSA(5,11)    
Bob = RSA(17, 11)

#Alice wysyla do Boba
cipher_text= Alice.encrypt(10, Bob.public_key)
print(Bob.decrypt(cipher_text))

#Bob wysyla do Alice
cipher_text= Bob.encrypt(25, Alice.public_key)
print(Alice.decrypt(cipher_text))