import requests, re
from multiprocessing import Pool
class spider(object):
    def __init__(self):
        print('开始爬取内容...')

    # 获取网页源代码
    def getHtml(self, url):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        return response.text

    # 产生url
    def changePage(self, url, total_page):
        now_page = int(re.search('pageNum=(\d+)', url).group(1))
        page_group = []
        for page in range(now_page, total_page + 1):
            link = re.sub('pageNum=\d+', 'pageNum=%d' % page, url)
            page_group.append(link)
        return page_group

    # 获取每个页面上的课程列表
    def getEveryClass(self, html):
        every_class = re.findall('(<li id="\d+".*</li>)', html, re.S)
        return every_class

    # 每个课程列表的课程具体信息
    def getInfo(self, every_class):
        info = {}
        info['title'] = re.search('class="lessonimg" title="(.*?)"', every_class, re.S).group(1)
        info['content'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>', every_class, re.S).group(1)
        info['classtime'] = re.search('<i class="time-icon"></i><em>(.*?)</em>', every_class, re.S).group(1)
        info['classlevel'] = re.search('<i class="xinhao-icon"></i><em>(.*?)</em>', every_class, re.S).group(1)
        info['learnum'] = re.search('<em class="learn-number">(.*?)</em>', every_class, re.S).group(1)
        return info

    # 将课程具体信息写入本地
    def saveInfo(self, classInfo):
        file = open('info.txt', 'a+', encoding='utf-8')
        for info in classInfo:
            file.write('title:' + info['title'].strip() + '\n')
            file.write('content:' + info['content'].strip() + '\n')
            file.write('classtime:' + info['classtime'].strip().replace('\r', '').replace('\n', '').replace('\t', '') + '\n')
            file.write('classlevel:' + info['classlevel'].strip() + '\n')
            file.write('learnum:' + info['learnum'].strip() + '\n')
            file.write('===================================================\n\n\n')
        file.close()


if __name__ == '__main__':
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    pool = Pool()
    jikespider = spider()
    all_links = jikespider.changePage(url, 20)
    class_infos = []
    result = []
    for link in all_links:
        source_html = jikespider.getHtml(link)
        source_class = jikespider.getEveryClass(source_html)
        for source in source_class:
            r = pool.apply_async(jikespider.getInfo, (source,))
            print(r)
            result.append(r)
    pool.close()
    pool.join()
    for res in result:
        class_infos.append(res.get())
    jikespider.saveInfo(class_infos)







