import requests
url ="http://108.29.41.133/api/v1/chargecontroller.php?file=4"

response = requests.get(url)
data = response.json()
print(data[0])