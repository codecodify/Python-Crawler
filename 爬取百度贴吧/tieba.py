import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # 请求错误时抛出错误
        response.encoding = 'utf-8'
        return response.text
    except:
        return 'ERROR'

def get_content(url):
    comments = []
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('li', attrs={'class' : ' j_thread_list clearfix'})
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find('a', attrs={'class':'j_th_tit '}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + li.find('a', attrs = {'class' : 'j_th_tit '})['href']
            comment['name'] = li.find('span', attrs = {'class' : 'tb_icon_author '}).text.strip()
            comment['time'] = li.find('span', attrs = {'class' : 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find('span', attrs = {'class' : 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            print('出了点小问题')
    return comments

def put_file(comments):
    with open('bieba.txt', 'a+', encoding='utf-8') as file:
        for comment in comments:
            file.write('标题：{}\t  链接：{}\t  发帖人：{}\t  发帖时间：{}\t  回复数量：{}\r'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
    print('当前页面爬取完成')


def main(base_url, page):
    url_list = [base_url + '&pn={}'.format(str(i * 50)) for i in range(0, page)]
    print('所有的网页已经下载到本地！开始筛选信息...')

    for url in url_list:
        content = get_content(url)
        put_file(content)
    print('所有信息保存完毕!')


if __name__ == '__main__':
    # base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'   # ie参数代表为编码格式
    # page = 500

    base_url = input('请输入您要抓取贴吧的主页面（不包括分页参数）：')
    page = int(input('请输入您要抓取的码数：'))
    main(base_url, page)