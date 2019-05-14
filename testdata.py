from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data1 = "ax1920y1080"
data2 = "s"
data3 = "l"
data = bytes(data1,'utf-8')
key = get_random_bytes(16)
key_out = open("key.bin", "wb")
key_out.write(key)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)


tag_out = open("tag.bin", "wb")
tag_out.write(tag)

print("key", key)
print("tag", tag)
print("data", data)

file_out = open("encrypted.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
print("cipher.nonce", cipher.nonce)
print("ciphertext", ciphertext)

