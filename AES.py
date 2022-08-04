from Crypto.Cipher import AES

class AESCipher():
    def __init__(self, key: bytes):
        self.cipher = AES.new(key, AES.MODE_ECB)

    def msg_encrypt(self, msg): # 填充
        if (len(msg) % 16 != 0):
            msg = msg + ' '*(16 - len(msg) % 16)
        return self.cipher.encrypt(msg.encode())

    def msg_decrypt(self, enc_msg):
        return self.cipher.decrypt(enc_msg).decode()
