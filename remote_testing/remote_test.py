import requests

r = requests.post('http://robo:5000/setcurrentplan', data = {'plan':[[100,100], [100,100], [100,100], [100,100], [100,100], [100,100]]})

