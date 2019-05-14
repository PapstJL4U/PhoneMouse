from Crypto.Cipher import AES

with open("key.bin", "rb") as i:
    key = i.read()

file_in = open("encrypted.bin", "rb")
nonce2, tag2, ciphertext2 = [ file_in.read(x) for x in (16, 16, -1) ]

# let's assume that the key is somehow available again
cipher2 = AES.new(key, AES.MODE_EAX, nonce2)
data666 = cipher2.decrypt_and_verify(ciphertext2, tag2)


print(ciphertext2)
print(data666)