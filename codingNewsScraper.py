import requests

response = requests.get('https://news.mit.edu/topic/machine-learning')

print(response.text)
