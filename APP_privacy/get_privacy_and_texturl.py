import json
from selenium import webdriver
import requests

def get_proxy():
	return requests.get(url = "http://192.168.23.1:5010/get/").json()

def delete_proxy(proxy):
	requests.get("http://192.168.23.1:5010/delete/?proxy={}".format(proxy))

def get_texturl_by_webid(webid):
	while True:
		proxy = get_proxy().get("proxy")
		if not proxy:
			input("没代理了，快快运行 schedule...")
		try:
			for i in range(3):
				# 运行三次 都不行才确定无效
				try:
					chromeOptions = webdriver.ChromeOptions()
					chromeOptions.add_argument("--proxy-server=http://{}".format(proxy))
					browser = webdriver.Chrome(options = chromeOptions)
					url = "https://www.wandoujia.com/top/app" + webid
					browser.get(url)
					browser.implicitly_wait(5) # 设置隐式等待时间
					
					print(browser.find_element_by_xpath("//a[@class='privacy-link']").get_attribute('href'))
					input("I'm waiting!!!")
					# /html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[4]/a			   
					
					browser.quit()
					# 使用代理访问
					return texturl, version
				except Exception as e:
					browser.quit()
					print("ERROR!")
					print(e)

		except Exception:
			# 删除代理池中代理
			delete_proxy(proxy)


with open("oldappid.json", "r") as f:
	oldappid = json.load(f)["oldappid"]

with open("wandoujia.json", "r") as f:
	content = json.load(f)
appids = list(content.keys())

for i in range(oldappid, len(appids)):
	oldappid = i
	appid = appids[i]
	item = content[appid]

	texturl, version = get_texturl_by_webid(item['webid'])
	item["texturl"] = texturl
	item["version"] = version

	break

	with open("wandoujia.json", "w") as f:
		json.dump(content, f)

	with open("oldappid.json", "w") as f:
		json.dump({"oldappid":oldappid}, f)

	break

