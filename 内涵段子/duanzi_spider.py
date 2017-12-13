import requests, re
class Spider:
    def __init__(self):
        self.enable = True #是否继续加载页面
        self.page = 1  # 当前爬取的页数


    def loadPage(self, page):
        url = "http://www.neihan8.com/article/list_5_" + str(page) + '.html'
        headers = {
            'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT6.1; Trident/5.0'
        }

        response = requests.get(url, headers = headers)
        response.encoding = 'gbk'  #网页是gbk编码
        gbk_html = response.text
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)  #此处要加re.S参数，将字符串作为整体进行匹配，否则只匹配一行
        item_list = pattern.findall(gbk_html)
        return item_list


    def printOnePage(self, item_list, page):
        print('****** 第 %d 页 爬取完毕... ******' % page)
        for item in item_list:
            print('==========')
            item = item.replace('<p>', '').replace('</p>','').replace('<br />', '')
            self.writeToFile(item)
    def writeToFile(self, text):
        with open('MyStory.txt', 'a+', encoding='utf-8') as file:
            file.write(text)
            file.write('---------------------------------------------------------')

    def doWork(self):
        while self.enable:
            try:
                item_list = self.loadPage(self.page)
            except requests.HTTPError as e:
                print(str(e))
                continue
            self.printOnePage(item_list, self.page)
            self.page += 1
            print('按回车继续...')
            print('输入 quit 退出')
            command = input()
            if command == 'quit':
                self.enable = False
                break
            continue

if __name__ == '__main__':
    mySpider = Spider()
    mySpider.doWork()
