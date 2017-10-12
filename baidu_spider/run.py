#coding=utf-8
from BaiduImageSearch import BaiduImage
import sys
import os

'''
python run.py 参数1 参数2 参数3 ...
参数1：抓取图片存放路径，如：/home/admin/爬虫数据/鹿
参数2及以后：都是抓取图片的关键词
'''
keyword = "_".join(sys.argv[2:])
save_path = sys.argv[1]
if not(os.path.exists(save_path)):
    os.makedirs(save_path)

print(keyword)
if not keyword:
    print("1111")
    print("1111")
else:
    search = BaiduImage(keyword, save_path=save_path)
    search.search()
