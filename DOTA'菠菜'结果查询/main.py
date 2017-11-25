import requests
import bs4

def get_html(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return ' ERROR '


def print_result(url):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    match_list = soup.find_all('div', class_='matchmain bisai_qukuai')
    for match in match_list:
        time = match.find('div', class_='whenm').text.strip()
        team_name = match.find_all('span', class_='team_name')  # 两个队名
        # 如果没有队名，则显示php的注释，这里使用了类型判断，如果是注释的内容，则为bs4.element.ProcessingInstruction类型，否则就是bs4.element.NavigableString类型，具体可以打印type(team_name[0].string)
        if type(team_name[0].string) == bs4.element.ProcessingInstruction:
            team1_name = '暂无队名'
        else:
            team1_name = team_name[0].string

        team1_support_level = soup.find('span', class_='team_number_green').string
        team2_name = team_name[1].string
        team2_support_level = soup.find('span', class_='team_number_red').string
        print(' 比赛时间：{}\n 队伍一：{}     胜率：{}\n 队伍二：{}     胜率：{}\n'.format(time, team1_name, team1_support_level, team2_name, team2_support_level))

def main():
    url = 'http://dota2bocai.com/match'
    print_result(url)

if __name__ == '__main__':
    main()