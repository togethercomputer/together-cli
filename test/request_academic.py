import requests

endpoint = 'https://staging.together.xyz/api/inference'

res = requests.post(endpoint, json={
    "model": "opt-1.3b-tp1",
    "prompt": "test",
    "tags": "academic",
}, headers={
    "User-Agent": "YOUR_NAME_HERE"
})

print(res.text)