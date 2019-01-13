import requests


def run():
	url = "https://mifengcha.com/exchange/binance"
	rs = requests.get(url)
	print(rs.text)

if __name__ == '__main__':
	run()