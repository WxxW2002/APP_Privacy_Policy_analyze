from xiaomiSpider import getAllAppidNameIconCategoty4Mi, search4Mi
from huaweiSpider import getAllApp4Hua, search4Hua, getApkByUrl4Hua
from crawlDb import Crawldb

from threading import Lock
from time import sleep

# 循环重新爬取全部的时间间隔
# 但是由于有个 while 如果sleep太久了就会没有响应 会阻塞flask
loopCrawlAllTimeInterval = 3600 # 一个小时 

class MyThread:
    def __init__(self, database, workStateTable, appInfoTable, jobStateTable, host = 'localhost', port = 3306, user = 'root', password = '12345678', workId4MiCrawl = "workId4MiCrawl", workId4HuaCrawl = "workId4HuaCrawl"):
        """
        job: 是启动自动任务还是停止 start/stop
        store: 是小米还是华为 xiaomi/huawei
        content: 是隐私正常还是 apk Text/apk
        """
        
        # # lock the dist, and the tail head
        self.lock_db = Lock() 
        # self.lock_index = Lock()

        # 直接初始化为 False
        # 小米自动爬取隐私政策的标记
        self.autoCrawlMiFlag = False
        # 华为自动爬取隐私政策的标记
        self.autoCrawlHuaFlag = False

                
        # 操作数据库
        self.crawldb = Crawldb(database = database,
                workStateTable = workStateTable,
                appInfoTable = appInfoTable,
                jobStateTable = jobStateTable,
                host = host,
                port = port,
                user = user,
                password = password, 
                workId4MiCrawl = workId4MiCrawl, 
                workId4HuaCrawl = workId4HuaCrawl,
                lock = self.lock_db)
        self.crawldb.rebuild() # debugger

        self.workId4MiCrawl = workId4MiCrawl
        self.workId4HuaCrawl = workId4HuaCrawl


    # ============================= 自动隐私政策 & apk ====================================
    # 开始自动爬取小米商城隐私政策 & apk
    def startAutoCrawlMi(self):
        # 已经在跑了就不用了
        if self.autoCrawlMiFlag:
            return "已经在自动爬取小米!"

        # 标记为正在爬取了
        self.autoCrawlMiFlag = True

        # 更新爬虫自己的状态
        self.crawldb.updateWorkStateTable(self.workId4MiCrawl, self.workId4MiCrawl, 1)
        
        # 死循环一直爬
        while self.autoCrawlMiFlag:  
            getAllAppidNameIconCategoty4Mi(self.crawldb, workId4MiCrawl)
            # sleep(loopCrawlAllTimeInterval)

        # 更新爬虫自己的状态
        self.crawldb.updateWorkStateTable(self.workId4MiCrawl, self.workId4MiCrawl, 0)

        return "开始自动爬取 xiaomi 成功!"


    # 开始自动爬取华为商城隐私政策 & apk
    def startAutoCrawlHua(self):
        
        # 已经在跑了就不用了
        if self.autoCrawlHuaFlag:
            return "已经在自动爬取华为!"

        # 标记为正在爬取了
        self.autoCrawlHuaFlag = True

        # 更新爬虫自己的状态
        self.crawldb.updateWorkStateTable(self.workId4HuaCrawl, self.workId4HuaCrawl, 1)

        # 死循环一直爬
        while self.autoCrawlHuaFlag:
            getAllApp4Hua(self.crawldb, workId4HuaCrawl)
            # sleep(loopCrawlAllTimeInterval)
       
        # 更新爬虫自己的状态
        self.crawldb.updateWorkStateTable(self.workId4HuaCrawl, self.workId4HuaCrawl, 0)
        
        return "退出自动爬取 huawei 成功!"


    # 停止自动爬取小米商城隐私政策 & apk
    def stopAutoCrawlMi(self):

        # 将标记设置为 False 就可以停止了
        self.autoCrawlMiFlag = False
        
        # 更新爬虫自己的状态
        self.crawldb.updateWorkStateTable(self.workId4MiCrawl, self.workId4MiCrawl, 0)
        return "成功停止自动爬取小米!"


    # 停止自动爬取华为商城隐私政策 & apk
    def stopAutoCrawlHua(self):

        # 将标记设置为 False 就可以停止了 当前页面对函数的调用了
        self.autoCrawlHuaFlag = False

        # 更新爬虫自己的状态
        self.crawldb.updateWorkStateTable(self.workId4HuaCrawl, self.workId4HuaCrawl, 0)
        return "成功停止自动爬取华为!"

    '''
    # ============================= 自动隐私 apk ====================================
    # 开始自动爬取小米商城 apk 
    def startAutoCrawlApkMi(self):

        # 已经在跑了就不用了
        if self.autoCrawlApkMiFlag:
            return "已经在自动爬取小米商城 apk 了!"

        # 标记为正在爬取了
        self.autoCrawlApkMiFlag = True

        # 死循环一直爬
        while self.autoCrawlApkMiFlag:
            with open("startAutoCrawlApkMi", "w+") as f:
                f.write("crawling at xiaomi ...")    
            print("crawling at xiaomi ...")
            sleep(1)

        return "退出自动爬取 xiaomi  apk 成功!"

    # 开始自动爬取华为商城 apk 
    def startAutoCrawlApkHuawei(self):

        # 已经在跑了就不用了
        if self.autoCrawlApkHuaweiFlag:
            return "已经在自动爬取华为商城 apk 了!"

        # 标记为正在爬取了
        self.autoCrawlApkHuaweiFlag = True

        # 死循环一直爬
        while self.autoCrawlApkHuaweiFlag:
            with open("startAutoCrawlApkHuawei", "w+") as f:
                f.write("crawling at huawei ...")
            print("crawling at huawei ...")
            sleep(1)

        return "退出自动爬取 huawei  apk 成功!"


    # 停止自动爬取小米商城 apk 
    def stopAutoCrawlApkMi(self):
        
        # 将标记设置为 False 就可以停止了
        self.autoCrawlApkMiFlag = False

        return "成功停止自动爬取小米商城 apk "


    # 停止自动爬取华为商城 apk 
    def stopAutoCrawlApkHuawei(self):
        
        # 将标记设置为 False 就可以停止了
        self.autoCrawlApkHuaweiFlag = False

        return "成功停止自动爬取华为商城 apk "
    '''

    # ============================= name 隐私 text ====================================
    def crawlByNameMi(self, name, jobid):
        # 更新此 jobid 的状态  --爬取中
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 1, type1 = 'both'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)

        search4Mi(name, self.crawldb)

        # 更新此 jobid 的状态  --爬取完毕
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 2, type1 = 'both'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)

        return f"调用按名字查询小米成功 name = {name}"

    def crawlByNameHua(self, name, jobid):
        # 更新此 jobid 的状态  --爬取中
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 1, type1 = 'both'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)

        search4Hua(name, self.crawldb)

        # 更新此 jobid 的状态  --爬取完毕
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 2, type1 = 'both'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)
        
        return f"调用按名字查询华为成功 name = {name}"

    '''
    # ============================= name 隐私 apk ====================================
    def crawlApkByNameMi(self):
        pass

    def crawlApkByNameHuawei(self):
        pass
    '''
    
    # ============================= 按 url 下载隐私政策 ====================================
    # 按 url 下载隐私政策
    def downloadTextByUrl(self, url, filename, jobid):
        # 更新此 jobid 的状态  --爬取中
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 1, type1 = 'text'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)

        info = getTextByUrl4Hua(url, filename)

        # 更新此 jobid 的状态  --爬取完毕
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 2, type1 = 'text'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)        
        
        return info


    # ============================= 按 url 下载 apk ====================================
    # 按 url 下载 apk
    def downloadApkByUrl(self, url, filename, jobid):
        # 更新此 jobid 的状态  --爬取中
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 1, type1 = 'apk'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)

        info = getApkByUrl4Hua(url, filename)
        
        # 更新此 jobid 的状态  --爬取完毕
        sql = f"""update {myThread.crawldb.jobStateTable} set state = 2, type1 = 'apk'
                    where jobid = '{jobid}';"""
        self.crawldb.doSQL(sql)
        
        return info


#设置数据库
database = "privacy"
workStateTable = "workStateTable" # 一些存储计算函数的状态的表
appInfoTable = "appInfoTable" # 存储 app 信息的表
jobStateTable = "jobStateTable" # 存储 job 的
host = "localhost"
port = 3306
user = "root"
password = "12345678"    
workId4MiCrawl = "workId4MiCrawl"
workId4HuaCrawl = "workId4HuaCrawl"

# 实例化一个线程
myThread = MyThread(database = database,
                    appInfoTable = appInfoTable,
                    workStateTable = workStateTable,
                    jobStateTable = jobStateTable,
                    host = host,
                    port = port,
                    user = user,
                    password = password,
                    workId4MiCrawl = workId4MiCrawl, 
                    workId4HuaCrawl = workId4HuaCrawl)
                  

# def dij_concurrent(para):
#     """
#     function: 
#         use dijkstra algorithm in CPU (with concurrent) to solve the SSSP. 
    
#     parameters:  
#         class, Parameter object. (see the 'SPoon/classes/parameter.py/Parameter') 
    
#     return: 
#         class, Result object. (see the 'SPoon/classes/result.py/Result')     
#     """

#     logger.debug("turning to func dij_concurrent-sssp")

#     t1 = time()

#     CSR, n, s, pathRecordBool = para.CSR, para.n, para.srclist, para.pathRecordBool

#     V, E, W = CSR[0], CSR[1], CSR[2]

#     # vis 数组
#     vis = np.full((n, ), 0).astype(np.int32)

#     # 距离数组
#     dist = np.full((n,), INF).astype(np.int32)
#     dist[s] = 0    

#     # 实例化线程类
#     myThread = MyThread(V, E, W, dist, vis, s)

#     # 线程数量
#     threadNum = 8
#     ts = [Thread(target = myThread.getSSSP) for i in range(threadNum)]

#     # 启动线程
#     for ti in ts:
#         ti.start()

#     # 等待线程执行完毕
#     for ti in ts:
#         ti.join()    

#     timeCost = time() - t1

#     # 结果
#     result = Result(dist = myThread.dist, timeCost = timeCost, msg = para.msg, graph = para.CSR, graphType = 'CSR')

#     if pathRecordBool:
#         result.calcPath()

#     return result