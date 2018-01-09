from Crypto.Cipher import AES


class Encryption:
    def __init__(self):
        self.key = b'\xa8\xb7Rh\xcc\x98\xa8+l\xfbD\xbbK\x1e:\r'
        self.iv = b'\n=\x80\xe9[oe\xc1V\xd5\n`,\x83\xb5)'

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        return cipher.encrypt(data)

    def decrypt(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        return cipher.decrypt(ciphertext)