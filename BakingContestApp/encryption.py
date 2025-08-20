from Crypto.Cipher import AES
import base64

class AESCipher:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciphertext = cipher.encrypt(raw.encode('utf-8'))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decoded = base64.b64decode(enc)
        return cipher.decrypt(decoded).decode('utf-8')

# Define key and IV
key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'  # 32 bytes
iv = b'OWFJATh1Zowac2xr'  # 16 bytes

# Initialize cipher
cipher = AESCipher(key, iv)

# Expose encrypt and decrypt functions
def encrypt(data):
    return cipher.encrypt(data)

def decrypt(data):
    return cipher.decrypt(data)
