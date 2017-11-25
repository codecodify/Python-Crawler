import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        response = requests.get(url, timeout = 30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except:
        return ' ERROR '

# 获取排行版小说及其链接，按顺序写入文件，格式为：小说名字+小说链接
def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    url_list = []
    category_list = soup.find_all('div', class_='index_toplist')

    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a+', encoding='utf-8') as file:
            file.write("\n小说种类：{} \n".format(name))
        general_list = cate.find('div', style='display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a', encoding='utf-8') as file:
                file.write('小说名：{} \t  小说地址：{} \n'.format(title, link))
    return url_list

# 获取单本小说的所有章节链接
def get_txt_rul(url):
    html = get_html(url)
    url_list = []
    soup = BeautifulSoup(html, 'lxml')
    list_all = soup.find_all('dd')
    txt_name = soup.find('div', id='info').h1.text
    with open('小说/{}.txt'.format(txt_name), 'a+', encoding='utf-8') as file:
        file.write('小说标题：{} \n'.format(txt_name))
    for list in list_all:
        url_list.append('http://www.qu.la/' + list.a['href'])
    return txt_name, url_list

# 获取单页文章内容并保存本地
def get_one_txt(txt_name, url):
    html = get_html(url).replace('<br>', '\n')
    soup = BeautifulSoup(html, 'lxml')
    try:
        title = soup.title.text
        txt = soup.find('div', id='content').text.replace('chaptererror();', '')
        with open('小说/{}.txt'.format(txt_name), 'a', encoding='utf-8') as file:
            file.write(title + '\n\n')
            file.write(txt)
            print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')

def main():
    all_novel_url = get_content('http://www.qu.la/paihangbang/')
    for novel_url in all_novel_url:
        novel_info = get_txt_rul(novel_url)
        for content_url in novel_info[1]:
            get_one_txt(novel_info[0], content_url)


if __name__ == '__main__':
    main()