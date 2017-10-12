# -*- coding:utf-8 -*-
import re
import urllib2
import sys
import os

class Fresheye_spider:

    def __init__(self, keyword, save_dir, max_download_num=300):
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
                    'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                req = urllib2.Request(url, headers=self.headers)
                response = urllib2.urlopen(req)
                page = response.read()
                return page
            except:
                return "Page Not found"


    def __get_image_items(self, page):
        # 正则表达式：<h3><a border="0" href="(.*)><img alt="
        pattern = r'<h3><a border="0" href="(.*?)><img alt="'
        re_list = re.findall(pattern, page)
        if len(re_list) == 0:
            print("查找结束！")
            sys.exit(0)
        else:
            return re_list

    def __download_image(self, item_list):
        # 正则表达式：<img alt="(.*)" src="(.*)" name="
        prefix = 'http://kotochu.fresheye.com'
        pattern = r'<img alt="(.*?)" src="(.*?)" name="'
        for item in item_list:
            jump_url = prefix + item
            image_detail_page = self.__download_page(jump_url)
            download_link = re.search(pattern, image_detail_page)
            try:
                req = urllib2.Request(download_link.group(2), headers=self.headers)
                # 设置一个urlopen的超时，如果10秒访问不到，就跳到下一个地址，防止程序卡在一个地方。
                img = urllib2.urlopen(req, timeout=20)
                p = open(os.path.join(self.save_dir, str(self.download_count)+".jpg"), "wb")
                p.write(img.read())
                p.close()
                print("已下载：" + download_link.group(2))
                self.download_count += 1
            except Exception as e:
                print("Exception" + str(e))


            # urllib.urlretrieve(download_link.group(2), os.path.join(self.save_dir, str(self.download_count)+".jpg"))
            # self.download_count += 1
            if self.download_count >= self.max_download_num:
                print("查找结束！")
                sys.exit(0)

    def start_search(self):
        url = 'http://kotochu.fresheye.com/search-img/?kw=****&kuid=299978&thid=6000041&pg=$$$$'
        search_keyword = self.keyword.replace(" ","+")
        key_url = url.replace("****", search_keyword)
        page_num = 0
        search_result_url = key_url.replace("$$$$",str(page_num))
        while True:
            page = self.__download_page(search_result_url)
            item_list = self.__get_image_items(page)
            self.__download_image(item_list)
            page_num += 1   # next page
            search_result_url = key_url.replace("$$$$",str(page_num))

# keyword为搜索关键词，可以带空格，最好是英文搜索
# save_dir为保存目录
# max_download_num为最大下载图片数
spider = Fresheye_spider(keyword="Tridrepana unispina", save_dir='/Volumes/Media/tea_plant_insect/fresheye_temp', max_download_num=100)
spider.start_search()