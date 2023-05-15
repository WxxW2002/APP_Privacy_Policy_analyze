import requests
from parsel import Selector
from time import sleep
import os
from datetime import datetime
import json
from fake_useragent import UserAgent

jobResultRoot = "./jobResult/"

def get_proxy(header):
	return requests.get(url = "http://127.0.0.1:5010/get/", headers = header).json()

def delete_proxy(proxy):
	requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def send(url, header):

	while True:
		proxy = get_proxy(header).get("proxy")
		if not proxy:
			input("没代理了，快快运行 schedule...")
		try:
			for i in range(3):
				# 运行三次 都不行才确定无效
				try:
					html = requests.get(url = url, headers = header, proxies={"http": "http://{}".format(proxy)})
					print({"http": "http://{}".format(proxy)})
				   
					# 使用代理访问
					return html
				except:
					pass

		except Exception:
			# 删除代理池中代理
			delete_proxy(proxy)
			pass
	
	return None


header1 = {
	'Host': "www.wandoujia.com",
	'Connection': "close",
	'Pragma': "no-cache",
	'Cache-Control': "no-cache",
	'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
	'sec-ch-ua-mobile': "?0",
	'Upgrade-Insecure-Requests': "1",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	'Sec-Fetch-Site': "none",
	'Sec-Fetch-Mode': "navigate",
	'Sec-Fetch-User': "?1",
	'Sec-Fetch-Dest': "document",
	'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}

header2 = {
	'Host': "www.wandoujia.com",
	'Connection': "close",
	'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
	'sec-ch-ua-mobile': "?0",
	'Upgrade-Insecure-Requests': "1",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	'Sec-Fetch-Site': "none",
	'Sec-Fetch-Mode': "navigate",
	'Sec-Fetch-User': "?1",
	'Sec-Fetch-Dest': "document",
	'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}
header3 = {
	'Host': "www.wandoujia.com",
	'Connection': "close",
	'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
	'Pragma': "no-cache",
	'Cache-Control': "no-cache",
	'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	'sec-ch-ua-mobile': "?0",
	'Upgrade-Insecure-Requests': "1",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
	'Sec-Fetch-Site': "none",
	'Sec-Fetch-Mode': "navigate",
	'Sec-Fetch-User': "?1",
	'Sec-Fetch-Dest': "document",
	'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
}

"""
	['https://www.wandoujia.com/category/5029',
	 'https://www.wandoujia.com/category/5018',
	 'https://www.wandoujia.com/category/5014',
	 'https://www.wandoujia.com/category/5024',
	 'https://www.wandoujia.com/category/5019',
	 'https://www.wandoujia.com/category/5016',
	 'https://www.wandoujia.com/category/5026',
	 'https://www.wandoujia.com/category/5017',
	 'https://www.wandoujia.com/category/5023',
	 'https://www.wandoujia.com/category/5020',
	 'https://www.wandoujia.com/category/5021',
	 'https://www.wandoujia.com/category/5028',
	 'https://www.wandoujia.com/category/5022',
	 'https://www.wandoujia.com/category/5027',
	 'https://www.wandoujia.com/category/6001',
	 'https://www.wandoujia.com/category/6003',
	 'https://www.wandoujia.com/category/6008',
	 'https://www.wandoujia.com/category/6004',
	 'https://www.wandoujia.com/category/6002',
	 'https://www.wandoujia.com/category/6007',
	 'https://www.wandoujia.com/category/6009',
	 'https://www.wandoujia.com/category/6005',
	 'https://www.wandoujia.com/category/6006',
	 'https://www.wandoujia.com/category/5015']
"""


# 就是豌豆荚里面也是直接按照应用和游戏进行大分类的 这里就可以直接获取比如游戏里面的各个小分类的链接
def getCategoryIds():
	categotuIds = []
	categotuIds += Selector(send('https://www.wandoujia.com/category/app', header1).text).xpath('/html/body/div[2]/ul[1]/li/a/@href').getall()
	categotuIds += Selector(send('https://www.wandoujia.com/category/game', header1).text).xpath('/html/body/div[2]/ul[1]/li/a/@href').getall()

	# 直接这样得到的是各个分类的 url 链接罢了 并不是其 id
	return list(map(lambda categoryUrl: categoryUrl[-4:], categotuIds))


# 从一堆 urls，每个的每个应用的详细信息页面 中获取我们想要 隐私政策链接和版本并汇聚到一个列表中
def getPrivacyUrlsAndVersion(urls, header):
	privacyUrls = []
	versions = []

	for url in urls:
		print(url)
		sleep(0.2)
		text = send(url, header).text
		hhh = Selector(text)
		print(text)
		privacyUrls.append(hhh.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[5]/a/@href').get())
		versions.append(hhh.xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[4]/text()").get()[1:])

	return privacyUrls, versions

def getAppid():
	s = str(datetime.now())
	appid = s[:4]+s[5:7]+s[8:10]+s[11:13]+s[14:16]+s[17:19]+s[20:]
	return appid

def getAll(crawlRecordFile):
	categotuIds = getCategoryIds()

	if not os.path.exists(crawlRecordFile):
		crawlRecordFileContent = {}
		oldcategotuId = 0
		oldpagei = 0
	else:
		with open(crawlRecordFile, "r") as f:
			crawlRecordFileContent = json.load(f)
		oldcategotuId = crawlRecordFileContent["categotuId"]
		oldpagei =  crawlRecordFileContent['pagei']

	for i in range(oldcategotuId, len(categotuIds)):
		sleep(1)

		categotuId = categotuIds[i]
		pagei = oldpagei
		oldpagei = 0

		while True:
			pagei += 1
			url = f"https://www.wandoujia.com/wdjweb/api/category/more?catId={categotuId}&subCatId=0&page={pagei}"
			content = send(url, header2).json()['data']['content']

			if content == "":
				break

			html = Selector(content)

			# 返回了当前分类下 当前这一页的所有二十几个应用的 appid 的 list
			webids = html.xpath("/html/body/li/@data-appid").getall()

			# 每个应用详细信息的页面
			appUrls = list(map(lambda webid: "https://www.wandoujia.com/apps/"+webid, webids))

			# 每个应用的 icon url
			iconUrls = html.xpath("/html/body/li/div/a/img/@data-original").getall()

			names = html.xpath("/html/body/li/div[2]/h2/a/text()").getall()

			category = html.xpath("/html/body/li/a[@class='tag-link']/text()").getall()

			# 然后是在其详细信息的页面获取其隐私政策的链接 和 版本 的列表
			header3['Referer'] = "https://www.wandoujia.com/category/"+categotuId
			# privacyUrls, versions = getPrivacyUrlsAndVersion(appUrls, header3)


			# 然后是 apk 的下载地址
			apkUrls = list(map(lambda x: "https://www.wandoujia.com/apps/"+x+"/download/dot?ch=detail_normal_dl", webids))

			# 以上就整理完了一页中所有的 apk 信息
			for i in range(len(webids)):
				item = {}
				item['webid'] = webids[i]
				item["name"] = names[i]
				item["category"] = category[i]
				item["iconurl"] = iconUrls[i]
				item["crawtime"] = str(datetime.now()) # 时间分离了
				item["store"] = "wandoujia"
				# item["texturl"] = privacyUrls[i]
				# item["version"] = versions[i]
				item["apkurl"] = apkUrls[i]

				appid = getAppid()
				item['appid'] = appid

				print("[+] finish a item")
				print(item)
				print()

				crawlRecordFileContent[appid] = item

			# 这两个用于记忆上一次的位置
			crawlRecordFileContent["categotuId"] = categotuId
			crawlRecordFileContent["pagei"] = pagei

			with open(crawlRecordFile, "w") as f:
				json.dump(crawlRecordFileContent, f)

def get_texturl_by_webid(webid, header):
	url = "https://www.wandoujia.com/apps/" + webid
	text = send(url, header).text
	html = Selector(text)
	print(text)
	privacyUrl = html.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[5]/a/@href').get()
	# company
	company = html.xpath("//span[@class='dev-sites']/text()").get()

	return privacyUrl, company


def makedir(s):
	if not os.path.exists(s):
		os.mkdir(s)

if __name__ == '__main__':

	# # ===================================
	# # each time run this crawl will create a index json file to store the detail infomation.
	# # browser = webdriver.Chrome() 
	# # thisJobid = getAppid()
	# thisJobid = "20210527151736459751"

	# thisJobDir = jobResultRoot + thisJobid + "/"
	# crawlRecordFile = thisJobDir + "index.json"
	# textFileDir = thisJobDir + "privacies/"
	# apkFileDir = thisJobDir + "apks/"

	# makedir(thisJobDir)
	# makedir(textFileDir)
	# makedir(apkFileDir)


	# # getAllAppidNameIconCategoty4Mi(crawlRecordFile, textFileDir, apkFileDir, browser)
	# getAll(crawlRecordFile)
	
	# # browser.quit()
	# # ==================================


	thisJobid = "20210527151736459751"
	thisJobDir = jobResultRoot + thisJobid + "/"
	crawlRecordFile = thisJobDir + "index.json"

	with open(crawlRecordFile, "r") as f:
		content = json.load(f)

	appids = list(content.keys())

	oldappid = content.get("oldappid")
	if not oldappid:
		oldappid = 0
	else:
		oldappid = appids.index(oldappid)

	for i in range(oldappid+1, len(appids)):
		sleep(0.5)
		appid = appids[i]
		item = content[appid]
		header3["User-Agent"] = UserAgent().random
		header3['Referer'] = 'https://www.baidu.com/'
		texturl, company = get_texturl_by_webid(item["webid"], header3)
		item[appid]["texturl"] = texturl
		item[appid]["company"] = company

		content["oldappid"] = appid

		with open(crawlRecordFile, "w") as f:
			json.dump(content, f)