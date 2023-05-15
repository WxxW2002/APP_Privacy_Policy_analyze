from xiaomiSpider import getAllAppidNameIconCategoty4Mi
# from huaweiSpider import getAllAppidNameIconCategoty4Hua


import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


jobResultRoot = "./jobResult/"


def getAppid():
	s = str(datetime.now())
	appid = s[:4]+s[5:7]+s[8:10]+s[11:13]+s[14:16]+s[17:19]+s[20:]
	return appid

def makedir(s):
	if not os.path.exists(s):
		os.mkdir(s)


if __name__ == '__main__':
	# each time run this crawl will create a index json file to store the detail infomation.
	browser = webdriver.Chrome() 
	thisJobid = getAppid()

	thisJobDir = jobResultRoot + thisJobid + "/"
	textFileDir = thisJobDir + "privacies/"
	apkFileDir = thisJobDir + "apks/"

	makedir(thisJobDir)
	makedir(textFileDir)
	makedir(apkFileDir)

	crawlRecordFile = thisJobDir + "index.json"
	with open(crawlRecordFile, "w") as f:
		json.dump([], f)


	getAllAppidNameIconCategoty4Mi(crawlRecordFile, 0)
	# getAllAppidNameIconCategoty4Hua(crawlRecordFile, textFileDir, apkFileDir, browser)
	
	browser.quit()
