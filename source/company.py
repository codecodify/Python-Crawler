import requests, re

url = 'https://www.kuaidi100.com/company.do?method=js'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
response = requests.get(url, headers = headers)
html = response.text
company_list = re.findall('"number" : "(.*?)".*?"shortName" : "(.*?)"', html, re.S)
company_list = dict(company_list)
company = dict()
for key, value in company_list.items():
    company[value] = key