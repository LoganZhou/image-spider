# -*- coding:utf-8 -*-
import re
import urllib2
import sys
import os
import socks
import socket

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 8080)
socket.socket = socks.socksocket

class Twmoth_tesri_spider:
    def __init__(self, url, save_dir, page_file=None):
        self.download_count = 0
        self.url = url
        if os.path.isdir(save_dir):
            self.save_dir = save_dir
        else:
            print("保存目录不存在！")
            sys.exit(0)
        if page_file != None:
            self.page_file = page_file

        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version:
            self.headers = {}
            self.headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        else:
            self.headers = {}
            self.headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    def __download_page(self, url):
        '''
        Downloading entire Web Document (Raw Page Content)
        :param url:
        :return:
        '''
        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version:  # If the Current Version of Python is 3.0 or above
            import urllib.request  # urllib library for Extracting web pages
            try:
                self.headers = {}
                self.headers[
                    'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                req = urllib.request.Request(url, headers=self.headers)
                resp = urllib.request.urlopen(req)
                respData = str(resp.read())
                return respData
            except Exception as e:
                print(str(e))
        else:  # If the Current Version of Python is 2.x
            import urllib2
            try:
                self.headers = {}
                self.headers[
                    'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                req = urllib2.Request(url, headers=self.headers)
                response = urllib2.urlopen(req)
                page = response.read()
                return page
            except:
                return "Page Not found"

    def __read_page(self):
        with open(self.page_file,'r') as f:
            page = f.read()
        return page

    def __get_image_items(self, page):
        # 正则表达式：<h3><a border="0" href="(.*)><img alt="
        pattern = r'src="(.*?)" style="'
        re_list = re.findall(pattern, page)
        if len(re_list) == 0:
            print("查找结束！")
            sys.exit(0)
        else:
            return re_list

    def __download_image(self, item_list):
        for image_link in item_list:
            try:
                download_link = 'http://twmoth.tesri.gov.tw/' + image_link.lstrip('.')
                req = urllib2.Request(download_link, headers=self.headers)
                # 设置一个urlopen的超时，如果10秒访问不到，就跳到下一个地址，防止程序卡在一个地方。
                img = urllib2.urlopen(req, timeout=20)
                p = open(os.path.join(self.save_dir, str(self.download_count)+".jpg"), "wb")
                p.write(img.read())
                p.close()
                print("已下载：" + download_link)
                self.download_count += 1
            except Exception as e:
                print("Exception" + str(e))

        print("查找结束！总共下载 %d 张图片。" % self.download_count)

    def start_search(self):
        page = self.__read_page()
        image_list = self.__get_image_items(page)
        self.__download_image(image_list)

spider = Twmoth_tesri_spider(url='http://twmoth.tesri.gov.tw/peo/FBMothQuery.aspx?F=Limacodidae&G=Setora&S=Setora%20postornata',
                             save_dir='/Volumes/Media/tea_plant_insect/fresheye_temp',
                             page_file='/Users/zhouheng/Downloads/Setora_postornata.htm')
spider.start_search()
