import requests
import io

with open("encrypted.bin", "rb") as f:
   data = f.read()

res = requests.get(url='http://192.168.2.100:8080/hello')
print(res.content)
print("data", data)
#print("data utf", data.decode(encoding='utf-8'))
res = requests.post(url='http://192.168.2.100:8080/secure',
                   data=data,
                   headers={'Content-Type': 'application/octet-stream'})
print(res)