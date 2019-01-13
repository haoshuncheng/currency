import requests


def run():
	url = "https://mifengcha.com/exchange/binance"
	rs = requests.get(url)
	text =rs.text

	content = re.findall(r"<script>window.__NUXT__=(.*)</script>",text)
	print(content)

if __name__ == '__main__':
	run()