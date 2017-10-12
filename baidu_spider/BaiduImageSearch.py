#coding=utf-8
from urllib import quote
import urllib2 as urllib
import re
import os


class BaiduImage():

    def __init__(self, keyword, count=2000, save_path="img", rn=60):
        self.keyword = keyword
        self.count = count
        self.save_path = save_path
        self.rn = rn

        self.__imageList = []
        self.__totleCount = 0

        self.__encodeKeyword = quote(self.keyword)
        self.__acJsonCount = self.__get_ac_json_count()

        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
        self.headers = {'User-Agent': self.user_agent, "Upgrade-Insecure-Requests": 1,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch",
                        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                        "Cache-Control": "no-cache"}
        # "Host": Host,

    def search(self):
        for i in range(0, self.__acJsonCount):
            url = self.__get_search_url(i * self.rn)
            response = self.__get_response(url).replace("\\", "")
            image_url_list = self.__pick_image_urls(response)
            self.__save(image_url_list)

    def __save(self, image_url_list, save_path=None):
        if save_path:
            self.save_path = save_path

        print(" " + str(self.__totleCount) + "")
        print(" " + str(len(image_url_list)) + "  ：" + self.save_path)

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        for image in image_url_list:
            host = self.get_url_host(image)
            self.headers["Host"] = host

            with open(self.save_path + "/%s.jpg" % self.__totleCount, "wb") as p:
                try:
                    req = urllib.Request(image, headers=self.headers)
                    # 设置一个urlopen的超时，如果10秒访问不到，就跳到下一个地址，防止程序卡在一个地方。
                    img = urllib.urlopen(req, timeout=20)
                    p.write(img.read())
                    p.close()
                    self.__totleCount += 1
                except Exception as e:
                    print("Exception" + str(e))
                    p.close()
                    if os.path.exists("img/%s.jpg" % self.__totleCount):
                        os.remove("img/%s.jpg" % self.__totleCount)

        print("  " + str(self.__totleCount) + "  ")

    def __pick_image_urls(self, response):
        reg = r'"ObjURL":"(http://img[0-9]\.imgtn.*?)"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, response)
        return imglist

    def __get_response(self, url):
        page = urllib.urlopen(url)
        return page.read()

    def __get_search_url(self, pn):
        return "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=" + self.__encodeKeyword + "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=" + self.__encodeKeyword + "&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=" + str(pn) + "&rn=" + str(self.rn) + "&gsm=1000000001e&1486375820481="

    def get_url_host(self, url):
        print(url)
        reg = r'http://(.*?)/'
        hostre = re.compile(reg)
        host = re.findall(hostre, url)
        if len(host) > 0:
            return host[0]
        return ""

    def __get_ac_json_count(self):
        a = self.count % self.rn
        c = self.count / self.rn
        if a:
            c += 1
        return c
