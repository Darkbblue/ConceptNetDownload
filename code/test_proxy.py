import requests
from tools import proxy

def test(url, proxy_ip):
	headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
			'Connection': 'close'
		}
	proxies = {'http': 'http://{}'.format(proxy_ip), 'https': 'https://{}'.format(proxy_ip)}
	try:
		requests.get(url, timeout=5, headers=headers, proxies=proxies)
		return True
	except Exception as e:
		print(url, proxy_ip)
		print(e)
		return False

result = []
for proxy_ip in proxy.get_proxy_list():
	urls = [
		'https://www.google.com/search?q=dog+run&source=lnms&tbm=isch',
		'https://freesound.org/search/?q=dog',
	]
	success_google = test(urls[0], proxy_ip)
	success_sound = test(urls[1], proxy_ip)
	result.append((proxy_ip, success_google, success_sound))

print()
for entry in result:
	print(entry)
