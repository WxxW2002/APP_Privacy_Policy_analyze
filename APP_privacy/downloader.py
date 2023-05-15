# 本 py 提供一个统一下载功能
# 自动爬取能爬取到相应的 url 然后通过此 py 对其相应的内容包括 隐私政策和 apk 进行下载, 而且还可以进行切割
# 而同时用户提交的 url 和 名字 也是可以通过此玩意进行下载 
#	名字的本质还是需要整成 url


# 如何在 centos 服务器中整 selenium ： https://segmentfault.com/a/1190000022589195


import requests
from selenium import webdriver
import re
from time import sleep
from parsel import Selector

def checkUrlValid(url):
	if "javascript:void(0)" in url:
		return False
	return True


	if re.match(r'^https?:/{2}\w.+$', url):
		return True

	return False


# name 应包含路径和后缀名
def downloadText(url, name, browser):
	# browser = webdriver.Chrome() #启动一个Chrome浏览器

	"""
	从这个链接获取其中的隐私政策文本信息
	"""

	if not checkUrlValid(url):
		print(f"Invalid url = {url}, check {checkUrlValid(url)}")
		return False

	try:
		browser.get(url) #对url发起一个get请求，获取相应数据
		browser.implicitly_wait(10) # 暗中等待 1s
		sleep(1)
		# browser.encoding = 'utf-8' # 这是另一种据说的可以解决编码的乱码的
		text = browser.page_source.encode("utf8") # 据说能解决乱码问题

		res = Selector(text=text.decode("utf-8"))
		body = res.xpath("//body")[0]

		# remove 没有返回值 是直接操作其中的对象
		# 移除 js
		body.xpath("//script").remove()

		with open(name, 'w', encoding='utf-8') as f:
			f.write(str(body.xpath('string(.)').get()))

		sleep(0.5) # 太快了 selenium 会出问题

		return True

	except:
		print(f"this app({name}) doesn't have a valid url = {url}")
		return False




def downloadApk(url, name):
	
	if not checkUrlValid(url):
		print(f"Invalid url = {url} of name = {name}")
		return False
	
	try:
		res = requests.get(url)
		with open(name, "wb") as f:
			f.write(res.content)

		return True
	except:
		print(f"requests = {url} failed!")
		return False



