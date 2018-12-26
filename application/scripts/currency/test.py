import requests

url = "https://www.aicoin.net.cn/api/coin-profile/fund"

querystring = {"coin_type":"adcoin","currency":"cny"}

headers = {
    # 'x-xsrf-token': "yJpdiI6IkhFNTFWNWpBR1JMRUFybXBwUHlXVVE9PSIsInZhbHVlIjoiaWtGSUowaDNuNVJnXC9jaW1BcU9Qb0RcL0MzQmNhcHJ6MkdERXhhT3h3TlRZQTk2WDE2NzdGbjdxN1dJc3FVcFpmMnFLc0M2Y3RQd1wvSCsrVUZyam9uR3c9PSIsIm1hYyI6IjA5OGQ2YmY3MTAxZjRhZThjZWU3N2VjNWRmYzY2M2NmNmUwYzU3OGI1N2ZmY2U5MTJmMDNiZjU0NjcyMjJkMGMifQ==",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'referer': "https://www.aicoin.net.cn/",
    # 'cookie': "acw_tc=7819730615456124849948380e626139f91eb699bbcf9bd0979d02b35abcde; _ga=GA1.3.1273134572.1545612487; _gid=GA1.3.1315763248.1545785955; Hm_lvt_3c606e4c5bc6e9ff490f59ae4106beb4=1545612486,1545785955,1545794695; Hm_lpvt_3c606e4c5bc6e9ff490f59ae4106beb4=1545794720; XSRF-TOKEN=eyJpdiI6IkhFNTFWNWpBR1JMRUFybXBwUHlXVVE9PSIsInZhbHVlIjoiaWtGSUowaDNuNVJnXC9jaW1BcU9Qb0RcL0MzQmNhcHJ6MkdERXhhT3h3TlRZQTk2WDE2NzdGbjdxN1dJc3FVcFpmMnFLc0M2Y3RQd1wvSCsrVUZyam9uR3c9PSIsIm1hYyI6IjA5OGQ2YmY3MTAxZjRhZThjZWU3N2VjNWRmYzY2M2NmNmUwYzU3OGI1N2ZmY2U5MTJmMDNiZjU0NjcyMjJkMGMifQ%3D%3D; aicoin_session=eyJpdiI6InBrSldPM2g5NFwvZzZZVEFybnRWYU5BPT0iLCJ2YWx1ZSI6IlBvaTE1UnNRR0Y3a3dyUXJDS09SRXpYeG9JUzVmS3BTVVVzXC96UmVLZTJqUGoySmE1MzBaWjI3WnpUSGVcL3lPZnBXejV1TjBTdlkwOHdkSWZUZDk5NHc9PSIsIm1hYyI6Ijg0NjVlMmY1MTI1YzI2YjU2ZDY4NjQzNmM4NDVmYTYxMGIwZTAzYzZhN2Q3ZGQyNGI1NWRhNDYxNjA0MWQ1YWEifQ%3D%3D",
    # 'path': "/api/coin-profile/fund?coin_type=adcoin&currency=cny",
    'authority': "www.aicoin.net.cn",
    'scheme': "https",
    'accept': "*/*",
    'cache-control': "no-cache",
    # 'postman-token': "fb7926b7-3550-ff0a-9514-044e4e2db8ee"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)