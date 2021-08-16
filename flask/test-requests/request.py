import requests

res = requests.get('http://localhost:82/migrations')
print(res.text)
