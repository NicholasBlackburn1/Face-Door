import Config 
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
 

# creating private key 
def get_private_key(password):
    salt = Config.SALT
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key        
        
# Encrypts data 
def encrypt(data):
    private_key = get_private_key(Config.ENCRYPITON_PASSWORD)
    raw = Config.PAD(data)
    iv = Random.new().read(Config.BLOCK_SIZE)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = get_private_key(password)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return Config.unpad(cipher.decrypt(enc[16:]))