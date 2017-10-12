# -*- coding:utf-8 -*-
import re
import urllib
import urllib2
import sys
import os

class Picssr_spider:

    def __init__(self, keyword, save_dir, max_download_num=100):
        self.download_count = 0
        self.keyword = keyword
        if os.path.isdir(save_dir):
            self.save_dir = save_dir
        else:
            print("保存目录不存在！")
            sys.exit(0)
        self.max_download_num = max_download_num


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
                    'User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
                req = urllib2.Request(url, headers=self.headers)
                response = urllib2.urlopen(req)
                page = response.read()
                return page
            except:
                return "Page Not found"

    def __get_image_download_link(self, page):
        # 正则表达式：<a title="(.*?)" href="(.*?)" data-url="
        # 第二个为图片链接
        pattern = r'<a title="(.*?)" href="(.*?)" data-url="'
        link_list = re.findall(pattern, page)
        if len(link_list) == 0:
            print("查找结束！")
            sys.exit(0)
        else:
            return link_list

    def __download_image(self, link_list):
        for res in link_list:
            link = res[1]
            #link = link.replace("https","http")
            try:
                # print(link)

                # urllib.urlretrieve(link[1], os.path.join(self.save_dir, str(self.download_count) + ".jpg"))
                req = urllib2.Request(link, headers=self.headers)
                img = urllib2.urlopen(req, timeout=10)
                p = open(os.path.join(self.save_dir, str(self.download_count) + ".jpg"), "wb")
                p.write(img.read())
                p.close()
                print("已下载：" + link)
                self.download_count += 1
            except Exception as e:
                print("Exception" + str(e))


            if self.download_count >= self.max_download_num:
                print("查找结束！")
                sys.exit(0)

    def start_search(self):
        url = 'http://picssr.com/search/****/page$$$$'
        search_keyword = self.keyword.replace(" ","+")
        key_url = url.replace("****", search_keyword)
        page_num = 1
        search_result_url = key_url.replace("$$$$",str(page_num))
        while True:
            page = self.__download_page(search_result_url)
            download_link_list = self.__get_image_download_link(page)
            self.__download_image(download_link_list)
            page_num += 1   # next page
            search_result_url = key_url.replace("$$$$",str(page_num))

# keyword为搜索关键词，可以带空格，最好是英文搜索
# save_dir为保存目录
# max_download_num为最大下载图片数
spider = Picssr_spider(keyword='atractomorpha sinensis', save_dir='/Volumes/Media/tea_plant_insect/fresheye_temp',
                       max_download_num=100)
spider.start_search()
