from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import sys

data=sys.argv[1]
key = b"ahdgebsg63ye8ubv"
cipher = AES.new(key, AES.MODE_CBC,iv=b'aaaaaaaaaaaaaaaa')
ct_bytes = cipher.encrypt(pad(bytes(data, 'utf-8'), AES.block_size))
print(ct_bytes.hex())
