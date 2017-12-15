"""
解析数据
"""
import requests
from prettytable import PrettyTable


class ExpressCollection:
    header = '时间 地点和跟踪进度'.split()
    express_data = None

    def __init__(self, express_url):
        self.express_url = express_url
        self.handleData(self.getJson())

    def getJson(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        response = requests.get(self.express_url, headers=headers)
        return response.json()

    def property(self):
        for express in self.express_data:
            data = []
            data.append(express['time'])
            data.append(express['context'])
            yield data

    def handleData(self, json):
        if not int(json['status']) == 200:
            print(json['message'])
            pass

        self.express_data = json['data']
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for data in self.property():
            pt.add_row(data)
        print(pt)

