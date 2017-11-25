import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        response = requests.get(url, timeout = 30)
        response.raise_for_status()
        response.encoding = 'gbk'
        return response.text
    except:
        return ' ERROR '
def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    movies = soup.select('ul.picList.clearfix li')
    for movie in movies:
        img_url = 'http:' + movie.find('img')['src']
        name = movie.find('span', class_='sTit').a.text
        # 这里错了一个异常捕获，防止没有上映时间而报错
        try:
            time = movie.find('span', class_='sIntro').text
        except:
            time = '暂无上映时间'
        # 将获取到的子孙节点组成字符串
        actors = ' '.join(list(movie.find('p', class_='pActor').stripped_strings))
        intro = movie.find('p', class_='pTxt pIntroShow').text
        print('片名：{}\t{}\n{}\n{} \n\n'.format(name, time, actors, intro))

        # 下载图片
        with open('images/{}.png'.format(name), 'wb+') as file:
            file.write(requests.get(img_url, stream=True).content)
def main():
    get_content('http://dianying.2345.com/top/')

if __name__ == '__main__':
    main()