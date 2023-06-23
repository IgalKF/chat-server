import random as rnd

class rsa:
    def surely_composite(self, n, d, s, a):
        'n-1 == 2**s * d'
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s):
            x = pow(x, 2, n)
            if x == 1: return True
            if x == n - 1: return False
        return True

    def detect_if_prime(self, n, number_of_rounds):    
        (d, s) = n - 1, 0
        while d % 2 == 0:
            (d, s) = (d//2, s+1)

        for round in range(number_of_rounds):
            if self.surely_composite(n, d, s, rnd.randint(2, n - 1)):
                return False
        return True

    def get_gcd_mod(self, e, phi):
        if phi == 0:
            return e, 1, 0

        gcd, e1, y1 = self.get_gcd_mod(phi, e % phi)
        e_new = y1
        y_new = e1 - (e // phi) * y1

        return gcd, e_new, y_new

    def find_inverse(self, e, phi):
        gcd, e_inv, _ = self.get_gcd_mod(e, phi)
        if gcd == 1:
            return e_inv % phi
        else:
            return None
        
    def pick_random_prime_number(self, second_prime_number = -1, max_random_number = 1024):
        first_prime_number = rnd.getrandbits(1024) if max_random_number == 1024 else rnd.randint(3, max_random_number)

        if (second_prime_number != -1 and first_prime_number == second_prime_number):
            first_prime_number = self.pick_random_prime_number(second_prime_number, max_random_number)

        if first_prime_number % 2 == 0:
            first_prime_number += 1

        if not self.detect_if_prime(first_prime_number, 4):
            first_prime_number = self.pick_random_prime_number(first_prime_number, max_random_number)
        
        return first_prime_number

    def define_prime_multiplication(self, first_prime_number, scond_prime_number):
        N = first_prime_number * scond_prime_number
        phi = (first_prime_number-1) * (scond_prime_number-1)

        e = 65537

        return N, phi, e
    
    def generate_keys(self):
        N , phi, e = self.define_prime_multiplication(self.pick_random_prime_number(), self.pick_random_prime_number())
        private_key = self.find_inverse(e, phi)
        public_key = f'{N}:{e}'
        return private_key, public_key

    def encrypt(self, m, n):
        message_num = int.from_bytes(m.encode(), 'big')
        encrypted_message = pow(message_num, 65537, n)

        return encrypted_message

    def decrypt(self, c, d, n):
        decrypted_message = pow(c, d, n)
        result = decrypted_message.to_bytes((decrypted_message.bit_length() + 7) // 8, 'big').decode('utf-8')
        return result