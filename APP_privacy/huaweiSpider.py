import requests
from datetime import datetime
from time import sleep
from urllib.parse import quote

header1 = {
	"Accept": 'application/json, text/plain, */*',
	"Accept-Encoding": 'gzip, deflate, br',
	"Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
	"Cache-Control": 'no-cache',
	"Connection": 'keep-alive',
	"Host": 'web-drcn.hispace.dbankcloud.cn',
	"Origin": 'https://appgallery.huawei.com',
	"Pragma": 'no-cache',
	"Referer": 'https://appgallery.huawei.com/',
	"Sec-Fetch-Dest": 'empty',
	"Sec-Fetch-Mode": 'cors',
	"Sec-Fetch-Site": 'cross-site',
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}


# 从某个 app 中去请求其详细信息时，用于获取隐私政策的 url 链接
header2 = {
	"Accept": 'application/json, text/plain, */*',
	"Accept-Encoding": 'gzip, deflate, br',
	"Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
	"Cache-Control": 'no-cache',
	"Connection": 'keep-alive',
	"Host": 'web-drcn.hispace.dbankcloud.cn',
	"Origin": 'https://appgallery.huawei.com',
	"Pragma": 'no-cache',
	"Referer": 'https://appgallery.huawei.com/',
	"Sec-Fetch-Dest": 'empty',
	"Sec-Fetch-Mode": 'cors',
	"Sec-Fetch-Site": 'cross-site',
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}


def send(url, headers):
	sleep(0.2)
	res = requests.get(url = url, headers = headers)
	return res

# 获取 应用和游戏 的 tabId，即是后续请求其下面的最小子分类的 tabId 时需要的 uri。
def getAppGameTabId():
	"""
	这里我们只爬取应用和游戏就可以了，
	"""
	url = 'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTemplate&serviceType=20&zone=&locale=zh'

	res = send(url = url, headers = header1).json()
	r = res['tabInfo']

	appTabId = r[1]['tabId'] # 应用 大分类中的 uri
	gameTabId = r[2]['tabId'] # 游戏 大分类中的 uri

	return appTabId, gameTabId


# 获取 分类的名字 主要是子分类的 tabId
def getSonCatTabId(uri):
	"""
	有了前面的是 游戏和应用的 id 我们就可以获取当前页面下的，
	分类，
	各个分类的子分类
	及其子分类对应的 tabId，用于获取当前页面下的 app ，作为 url 中的 uri 参数。
	https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&uri=b2b4752f0a524fe5ad900870f88c11ed&maxResults=25&zone=&locale=zh
	"""

	subCategories = [] # 一个列表 元素为字典 包含当前子分类的名字， tabId，父分类

	url = f"https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&uri={uri}&maxResults=100&zone=&locale=zh"

	res = send(url = url, headers = header1).json()
	r = res['tabInfo']

	for i in range(len(r)):
		rr = r[i]['tabInfo']
		for j in range(len(rr)):
			item = {}
			item["category"] = r[i]['tabName']
			item["subCategory"] = rr[j]['tabName']
			item["uri"] = rr[j]['tabId']

			subCategories.append(item)

	return subCategories




# 从 appid 获取 其隐私政策的链接
def getTextUrl(appId):
	"""
	从 appid 获取其隐私政策的链接
	"""
	url = f"https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&maxResults=25&uri=app%7C{appId}&shareTo=&currentUrl=https%253A%252F%252Fappgallery.huawei.com%252F%2523%252Fapp%252F{appId}&accessId=&appid={appId}&zone=&locale=zh"
	print(url)

	res = send(url = url, headers = header2).json()
	r = res['layoutData']

	for x in range(len(r)):
		if "Privacy Policy" in str(r[x]) or "隐私政策" in str(r[x]):
			return r[x]['dataList'][0]['conceal']['text']

	return "NULL"


def getAllApp4Hua(crawldb, workId4HuaCrawl):

	# 华为只爬应用和游戏
	appTabId, gameTabId = getAppGameTabId()
	TableIds = [appTabId, gameTabId]

	for tableId in TableIds:
		subCategories = getSonCatTabId(tableId)
		# print(subCategories)

		for item in subCategories:
			uri, category, subCategory = item['uri'], item['category'], item['subCategory']
			reqPageNum = 0

			while True:
				# 查询是否需要退出
				sql = f"""select state from {crawldb.workStateTable} where jobid = '{workId4HuaCrawl}';"""
				state = crawldb.doSQL(sql)
				if state[0] == 0 and state[0] == False:
					return

				reqPageNum += 1
				url = f"https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum={reqPageNum}&uri={uri}&maxResults=25&zone=&locale=zh" 
				res = send(url = url, headers = header1).json()

				r = res["layoutData"][0] 
				rr = r['dataList'] # 这就是一个 list 包含了请求到的 25 个

				for i in range(len(rr)):
					# 查询是否需要退出
					sql = f"""select state from {crawldb.workStateTable} where jobid = '{workId4HuaCrawl}';"""
					state = crawldb.doSQL(sql)
					if state[0] == 0 or state[0] == False:
						return

					name = rr[i]['name'] # app 名称
					appid = rr[i]['appid'] # app id
					apkurl = rr[i]['downurl'] # apk 地址
					crawtime = str(datetime.now())#time.asctime(time.localtime(time.time())) # 爬取时间
					iconurl = rr[i]['icon'] # 图标 或许前端需要显示呢？
					category = category # 应用分类
					subCategory = subCategory # 应用子分类
					version = rr[i]['appVersionName'] # 版本信息
					store = "huawei"
					texturl = getTextUrl(appid)

					# 查询数据库中是否有这个 app 没有就插入
					sql = f"""select appid from {crawldb.appInfoTable} where appid = '{appid}';"""
					if crawldb.doSQL(sql) == None:
						sql = f"""insert into {crawldb.appInfoTable}(appid, name, category, subCategory, iconurl, crawtime, store, texturl, apkurl, version) 
									values ('{appid}', '{name}', '{category}', '{subCategory}', '{iconurl}', '{crawtime}', '{store}', '{texturl}', '{apkurl}', '{version}');"""
						crawldb.doSQL(sql)
					else:
						sql = f"""select version from {crawldb.appInfoTable} where appid = '{appid}';"""
						# 版本不一样就更新最新的
						# 同时设定文本为空 apk 为空，以便后续可以下载新文件
						if crawldb.doSQL(sql)[0] != version:
							sql = f"""update {crawldb.appInfoTable} set name = '{name}',
									category = '{category}', iconurl = '{iconurl}', crawtime = '{crawtime}', 
									store = '{store}', texturl = '{texturl}', apkurl = '{apkurl}', 
									subCategory = '{subCategory}', version = '{version}', 
									textpath = {None}, apkpath = {None} where jobid = '{jobid}';"""
							crawldb.doSQL(sql)					

				if res['hasNextPage'] != 1:
					break


"""
download apk headers
"""

header3 = {
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	'Accept-Encoding': "gzip, deflate",
	'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
	'Cache-Control': "no-cache",
	'Connection': "keep-alive",
	'Host': "appdlc-drcn.hispace.hicloud.com",
	'Pragma': "no-cache",
	'Upgrade-Insecure-Requests': "1",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

def getApkByUrl4Hua(url, name):

	try:
		res = send(url = url, headers = header3)
		with open(name, "wb") as f:
			f.write(res.content)
		return "成功保存到 {name}"
	except:
		return "从 url = {url} 保存 apk 文件到 {name} 失败"

def getTextByUrl4Hua(url, name):
	pass


header4 = {
	"Accept": 'application/json, text/plain, */*',
	"Accept-Encoding": 'gzip, deflate, br',
	"Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
	"Cache-Control": 'no-cache',
	"Connection": 'keep-alive',
	"Host": 'web-drcn.hispace.dbankcloud.cn',
	"Origin": 'https://appgallery.huawei.com',
	"Pragma": 'no-cache',
	"Referer": 'https://appgallery.huawei.com/',
	"Sec-Fetch-Dest": 'empty',
	"Sec-Fetch-Mode": 'cors',
	"Sec-Fetch-Site": 'cross-site',
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

def search4Hua(name, crawldb):
	url = f"https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.completeSearchWord&serviceType=20&keyword={quote(name, encoding='utf-8')}&zone=&locale=zh"

	res = send(url = url, headers = header4)
	s = res.json()['appList'][0]

	appid = s['id']
	name = s['name']
	apkurl = s['downurl']
	version = s['version']
	iconurl = s['icon']
	category = s['kindName']
	crawtime = str(datetime.now())
	store = "huawei"
	texturl = getTextUrl(appid)

	# 查询数据库中是否有这个 app 没有就插入
	sql = f"""select appid from {crawldb.appInfoTable} where appid = '{appid}';"""
	if crawldb.doSQL(sql) == None:
		sql = f"""insert into {crawldb.appInfoTable}(appid, name, category, iconurl, crawtime, store, texturl, apkurl, version) 
					values ('{appid}', '{name}', '{category}', '{iconurl}', '{crawtime}', '{store}', '{texturl}', '{apkurl}', '{version}');"""
		crawldb.doSQL(sql)
	else:
		sql = f"""select version from {crawldb.appInfoTable} where appid = '{appid}';"""
		# 版本不一样就更新最新的
		# 同时设定文本为空 apk 为空，以便后续可以下载新文件
		if crawldb.doSQL(sql)[0] != version:
			sql = f"""update {crawldb.appInfoTable} set name = '{name}',
					category = '{category}', iconurl = '{iconurl}', crawtime = '{crawtime}', 
					store = '{store}', texturl = '{texturl}', apkurl = '{apkurl}', version = '{version}', 
					textpath = {None}, apkpath = {None} where jobid = '{jobid}';"""
			crawldb.doSQL(sql)	

if __name__ == '__main__':
	
	getAllApp()

	# subCategories = getSonCatTabId(gameTabId)

	# for item in subCategories[:2]:
	# 	sleep(0.2)
	# 	apps = getAllAppId(item['uri'], item['category'], item['subCategory'])

	# print(apps)
	# print("="*30)
	# print(len(apps))

	# appids = ["C100797671", "C101810811", "C101081295", "C103411281"]

	# for appidddd in appids:
	# 	print(getPrivicyUrl(appidddd))
