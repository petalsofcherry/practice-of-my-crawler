# -*- coding:utf-8 -*-
import urllib.request
import re

class QSBK(object):
    def __init__(self):
        self.url = 'http://www.qiushibaike.com/hot/page/'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
    
    #传入页码
    def getContent(self,page):
        try:
            url = self.url + str(page)
            request = urllib.request.Request(url=url, headers=self.headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')
            #正则提取
            patter = re.compile('<div class="content">.*?<span>(.*?)</span>(.*?)<div class="stats">', re.S)
            items = re.findall(patter, content)
            for i in items:
                #有图片的笑话咱都不要了
                havimg = re.search("img", i[1])
                if not havimg:
                    replaceBR = re.compile("<br/>")
                    text = re.sub(replaceBR, "\n", i[0])
                    print(text)
        #要是有错误，就报错。
        except urllib.request.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

    def start(self):
        #每按一下回车，就给你翻页，唔，其实是我为了自己在IDE里面看的爽……
        for page in range(1,50):
            self.getContent(page)
            input()
        print("you should relax.")


crawler = QSBK()
crawler.start()
