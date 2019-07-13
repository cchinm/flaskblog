import requests
url = 'http://bjx.iimedia.cn/app_rank'

req = requests.get(url=url, proxies={"http":"http://222.240.184.126:8086"})
print(req.text)