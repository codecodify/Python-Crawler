import requests, os
from bs4 import BeautifulSoup
from multiprocessing import Pool

class JDSpider:
    def __init__(self, url):
        self.url = url  # 采集的目标地址，如 https://list.jd.com/list.html?cat=9987,653,655
        self.start_page = 1  # 采集起始页数
        self.end_page = None


    # 获取HTML
    def getHtml(self, url):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        return response.text


    # 下载图片
    def downImage(self, fileName, imageUrl):
        image_path = 'image'
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        with open(os.path.join(image_path, fileName), 'wb') as file:
            image = requests.get(imageUrl)
            file.write(image.content)
            return fileName + '图片已下载'

    def work(self):
        html = self.getHtml(self.url)
        pool = Pool()
        # 获取结束页码
        bsObj = BeautifulSoup(html, 'lxml')
        self.end_page = int(bsObj.find('span', {'class' : 'p-skip'}).em.b.text)
        # self.end_page = 10  结束页面，测试的时候可以去掉注释
        result = []
        for page in range(self.start_page, self.end_page + 1):
            url = self.url + '&page=' + str(page)
            html = self.getHtml(url)
            bsObj = BeautifulSoup(html, 'lxml')
            images = bsObj.select('li.gl-item div.p-img img')
            try:
                for img in images:
                    imageUrl = 'https:' + img.get('src')
                    name = imageUrl.split('/')[-1]
                    r = pool.apply_async(self.downImage, args=(name, imageUrl))
                    result.append(r)
            except:
                continue
        pool.close()
        pool.join()
        for item in result:
            print(item.get())
        print('done..')

if __name__ == '__main__':
    jd = JDSpider('https://list.jd.com/list.html?cat=9987,653,655')
    jd.work()