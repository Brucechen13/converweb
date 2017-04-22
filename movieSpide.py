import requests
from lxml import etree

moviesUrl=['https://movie.douban.com/chart','https://movie.douban.com/top250']

def get_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'www.douban.com',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    response = requests.get(url)#, headers=headers
    print(url+str(response.status_code))
    if response.status_code == 200:
        data = []
        doc = etree.HTML(response.text)
        all_div = doc.xpath('//tr[@class="item"]')
        value = {}
        #print(all_div)
        for row in all_div:
            # 获取影评的标题部分
            title = row.xpath('.//td')
            value['url'] = title[0].xpath('./a/@href')[0]
            value['title'] = title[0].xpath('./a/@title')[0]
            value['pic'] = title[0].xpath('./a/img/@src')[0]
            value['intro'] = title[1].xpath('./div/p/text()')[0]
            value['star'] = title[1].xpath('./div/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
            data.append(value)
            print(value)
        return value
    else:
        pass

get_html(moviesUrl[0])
