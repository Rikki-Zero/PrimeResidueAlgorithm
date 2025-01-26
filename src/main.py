import secrets
import math

class Base:
    def __init__(self):
        pass

    def __is_composite(self, n, a, d, s):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    def __miller_rabin(self, n, k=20):
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(k):
            a = secrets.randbelow(n - 1) + 1
            if self.__is_composite(n, a, d, s):
                return False
        return True

    def generate_large_prime(self, bits):
        while True:
            # 生成指定位数的随机奇数
            n = secrets.randbits(bits)
            n |= (1 << bits - 1) | 1  # 确保是奇数，并且位数符合要求

            if self.__miller_rabin(n):
                return n
            
    def __extended_gcd(self, a, b):
        # 扩展欧几里得算法
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.__extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def modular_inverse(self, a, m):
        # 计算模逆元
        gcd, x, _ = self.__extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("模逆元不存在，因为 a 和 m 不是互质的")
        return (x % m + m) % m # 保证返回的是正数

    def generate_keys(self, p):
        # 生成加密和解密密钥
        while True:
            key = secrets.randbelow(p - 3) + 2 # 确保 1 < key < p - 1
            if math.gcd(key, p - 1) == 1: # 确保 key 和 p-1 互质
                break
        key_inverse = self.modular_inverse(key, p - 1) # 这里是 p - 1 不是 p
        return key, key_inverse

    def encrypt(self, message, key, p):
        # 加密消息
        return pow(message, key, p)

    def decrypt(self, ciphertext, key_inverse, p):
        # 解密消息
        return pow(ciphertext, key_inverse, p)


if __name__ == '__main__':
    base = Base()
    bits = 24
    p = base.generate_large_prime(bits)
    print(f"生成的大素数 p: {p}")

    key, key_inverse = base.generate_keys(p)
    print(f"加密密钥 key: {key}")
    print(f"解密密钥 key_inverse: {key_inverse}")

    message = 23324
    print(f"原始消息: {message}")

    ciphertext = base.encrypt(message, key, p)
    print(f"加密后的密文: {ciphertext}")

    decrypted_message = base.decrypt(ciphertext, key_inverse, p)
    print(f"解密后的消息: {decrypted_message}")
    
    assert message == decrypted_message
    print("加解密测试通过!")