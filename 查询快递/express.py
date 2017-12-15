"""
命令行查询快递

Usage:
    express <type> <postid>

Example:
    express 圆通 812378663386
    express 顺丰 0581875298433
"""

from docopt import docopt
from source.company import company
from source.ExpressCollection import ExpressCollection

def cli():
    arguments = docopt(__doc__)
    try:
        type = company.get(arguments['<type>'])
        postid = arguments['<postid>']
        print(type, postid)
        url = 'http://www.kuaidi100.com/query?type=%s&postid=%s' % (type, postid)
        ExpressCollection(url)
    except:
        print('运行错误，请检查格式是否正确')

if __name__ == '__main__':
    cli()