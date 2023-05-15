import requests
from parsel import Selector
from time import sleep
from datetime import datetime
import json
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import os


jobResultRoot = "./jobResult/"

header1 = {
    'Host': "app.mi.com",
    'Connection': "keep-alive",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
    'X-Requested-With': "XMLHttpRequest",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Dest': "empty",
    'Referer': "https://app.mi.com/category/0",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
}


header2 = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    'Cache-Control': "max-age=0",
    'Connection': "keep-alive",
    'Host': "app.mi.com",
    'Sec-Fetch-Dest': "document",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-Site': "none",
    'Sec-Fetch-User': "?1",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
}

def send(url, header):
    # if url[:5] == "https":
    #     url = "http" + url[5:]
    sleep(10)
    print(f"url={url}")
    return requests.get(url = url, params = header) # https , verify=False  , timeout=15, verify=False


def getAllAppidNameIconCategoty4Mi(crawlRecordFile, pagei = -1):

    print(f"[#] file will save to {crawlRecordFile} ...")

    sleep(1)

    # 穷举所有, 应用 0 就是所有的
    # pagei = -1

    if not os.path.exists(crawlRecordFile):
        crawlRecordFileContent = []
    else:
        with open(crawlRecordFile, "r") as f:
            crawlRecordFileContent = json.load(f)

    while True:

        sleep(1)

        pagei += 1

        url1 = f"https://app.mi.com/categotyAllListApi?page={pagei}&categoryId=0&pageSize=30"
        res = send(url1, header1).json()['data']

        # 遍历完了  退出
        if len(res) <= 0:
            break

        for app in res:

            item = {}

            item["webid"] = app['packageName'] # 小米实际上就是通过 packageName 来定位的

            print(f"[*] getting {item['webid']}...")

            item["name"] = app['displayName']
            item["category"] = app['level1CategoryName']
            item["iconurl"] = app['icon']
            item["crawtime"] = str(datetime.now())
            item["store"] = "xiaomi"
            item["xiaomi_appId"] = app["appId"]

            item["texturl"], item["version"] = getTexturlApkurlFromAppid(item["webid"])
            item["apkurl"] = f"https://app.mi.com/download/{item['xiaomi_appId']}?id={item['webid']}&ref=appstore.mobile_download"

            
            # 为此记录生成一个 appid 
            appid = getAppid()
            item['appid'] = appid

            # textFilename  = textFileDir + str(appid) + ".txt"
            # apkFilename = apkFileDir + str(appid) + ".apk"

            # try:
            #     if not downloadApk(item["apkurl"], apkFilename):
            #         apkFilename = "-1"
            # except:
            #     apkFilename = "-1"
            #     print(f"download apk error, apkurl = {item['apkurl']}...")

            
            # try:
            #     if not downloadText(item["texturl"], textFilename, browser):
            #         textFilename = "-1"
            # except:
            #     textFilename = "-1"
            #     print(f"download text error, texturl = {item['texturl']}...")

                
            

            # item["textFilename"] = textFilename
            # item["apkFilename"] = apkFilename

            print("[+] finish a item")
            print(item)
            print()

            crawlRecordFileContent.append(item)


            # save it after each for
            with open(crawlRecordFile, "w") as f:
                json.dump(crawlRecordFileContent, f)



        
    

# 上面的函数无法获取全部数据，这个函数就是用来进行此数据获取的 textpath  
def getTexturlApkurlFromAppid(webid):
    url2 = "https://app.mi.com/details?id=" + webid

    res = Selector(text=send(url2, header2).text)

    texturl = res.xpath("/html/body/div[6]/div[1]/div[5]/div[2]/div[2]/a/@href").get()
    version = res.xpath("/html/body/div[6]/div[1]/div[4]/div[1]/div[2]/text()").get()
    
    return texturl, version

  


def getAppid():
    s = str(datetime.now())
    appid = s[:4]+s[5:7]+s[8:10]+s[11:13]+s[14:16]+s[17:19]+s[20:]
    return appid


def makedir(s):
    if not os.path.exists(s):
        os.mkdir(s)

if __name__ == '__main__':

    # each time run this crawl will create a index json file to store the detail infomation.
    # browser = webdriver.Chrome() 
    thisJobid = getAppid()

    thisJobDir = jobResultRoot + thisJobid + "xiaomi" + "/"
    crawlRecordFile = thisJobDir + "index.json"
    textFileDir = thisJobDir + "privacies/"
    apkFileDir = thisJobDir + "apks/"

    makedir(thisJobDir)
    makedir(textFileDir)
    makedir(apkFileDir)


    # getAllAppidNameIconCategoty4Mi(crawlRecordFile, textFileDir, apkFileDir, browser)
    getAllAppidNameIconCategoty4Mi(crawlRecordFile, 10)
    
    # browser.quit()
