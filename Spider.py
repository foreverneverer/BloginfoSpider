#!usr/bin/python
# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup

account = "u011552404"

baseUrl = 'http://blog.csdn.net'

'''
使用urllib获取html页面
'''
def getPage(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}  # 伪装成浏览器访问
    req = request.Request(url, headers=headers)
    Response = request.urlopen(req)
    Page = Response.read()
    return Page


'''
获取文章分页数：
1、目的是在接下来的页面抓取中能够抓取每一页的数据
2、分页数在CSDN下有规律，即页码显示区域的最后一个数字就是总页数
'''


def getPageCount(url):
    Page = getPage(url)
    soup = BeautifulSoup(Page, 'html.parser', from_encoding='utf-8')  # 利用BeautifulSoup解析XML，形成特殊的Tag对象
    papeList = soup(class_="page-link")#页码显示区域
    numberList = papeList[-2]#提取页码显示区域数据
    res = str(numberList).split('<')[-2].split('>')[-1]#提取页码数
    return res


'''
提取所有文章数和阅读数
1、请参看BeautifulSoup的教程理解
2、核心原理就是获取+分割+得到关键字，具体如何提取请在CSDN页面上调出“开发者模式调试控制台”（F12）,
   总结所有抓取的信息在页面上的位置、元素特点，建议有一定的前端HTML经验
3、提取后存入txt文档
'''

def getArticleDetails():
    myUrl = baseUrl + '/' + account
    page_sum_number = getPageCount(myUrl)
    print("pageNumber", page_sum_number)
    cur_page_num = 1
    linkList = []
    titleList = []
    dateList = []
    readList = []
    while cur_page_num <= int(page_sum_number):
        url = myUrl + '/article/list/' + str(cur_page_num)  # CSDN的每页博客的URL地址格式
        myPage = getPage(url)
        soup = BeautifulSoup(myPage, 'html.parser', from_encoding='utf-8')#解析当前XML页面的为soup对象
        print(soup)
        for blog_list in soup.find_all(class_="blog-unit"):#CSDN博客中目录页每篇博客所在的元素class统一为"blog-unit"，所以通过此关键字定位到博客信息列表
            print("blog_list", blog_list.contents)
            link_elment = blog_list.contents[1]#第一个元素即为链接地址所在
            link = link_elment['href'].strip()  # 提取链接地址
            print("link", link)
            name_elment = link_elment.contents[1]#链接地址所在元素的第一个元素又是名称元素
            name = str(name_elment).split('\n')[-1].split('\t')[-3]  # 提取博客文章名称
            print("name", name)
            linkList.append(link)
            titleList.append(name)
        '''
        日期和阅读数提取这里出现了意外的情况：明明日期和阅读数所在元素区域是和上一个博客标题区域分离的，
        结果解析出来竟然把日期和博客阅读数作为blog_list的子节点（子区域），这里重新提取关键字class_=
        " floatL left-dis-24"，但是由于这个关键字所在区域同时检索出了三个信息：日期、阅读数、评论数
        所以，一次循环同时提取三个信息，所以for in 语句不能用了，采用list的索引指针移动的形式，每次提
        取三个信息（实际代码作演示只提取了两个）
        '''
        list = soup.find_all(class_=" floatL left-dis-24")
        i = 0
        while i < len(list):
            date_info = list[i]
            print("date_info", type(date_info), date_info)
            date = str(date_info).split('<')[1].split('>')[-1]
            print("date", date)
            dateList.append(date);
            i = i + 1
            read_info = list[i]
            print("read_info", read_info)
            read_span = read_info.find('span')
            read = str(read_span).split('>')[1].split('<')[0]
            print("read", read)
            readList.append(read)
            i = i + 2 # 跳过下一个信息提取
        cur_page_num = cur_page_num + 1
    f = open("./read_count.txt", "a+")
    for i in range(0, len(titleList)):
        #string = titleList[i] + '\t' + linkList[i] + '\t' + dateList[i] + '\t' + readList[i] + '\t' + '\n'
        string = readList[i] + '\n'
        f.write(str(string))
    f.write('\n')
    f.close()


if __name__ == "__main__":
    getArticleDetails()
