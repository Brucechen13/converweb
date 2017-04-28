import requests
from lxml import etree

moviesUrl=['https://movie.douban.com/chart','https://movie.douban.com/top250']

def getMovie():
    return get_html(moviesUrl[0])

def get_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host':'movie.douban.com',
        'Referer':'https://movie.douban.com/chart',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    response = requests.get(url, headers=headers)#
    if response.status_code == 200:
        data = []
        doc = etree.HTML(response.text)
        all_div = doc.xpath('//tr[@class="item"]')
        for row in all_div:
            value = {}
            # 获取影评的标题部分
            title = row.xpath('.//td')
            value['url'] = title[0].xpath('./a/@href')[0]
            value['title'] = title[0].xpath('./a/@title')[0]
            value['pic'] = title[0].xpath('./a/img/@src')[0]
            value['intro'] = title[1].xpath('./div/p/text()')[0]
            value['star'] = title[1].xpath('./div/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
            value['comments'] = []
            detail = requests.get(value['url'])
            if detail.status_code == 200:
                doc_deatil = etree.HTML(detail.text)
                value['pic'] = doc_deatil.xpath('//div[@id="mainpic"]/a/img/@src')[0]
                value['type'] = '|'.join(doc_deatil.xpath('//span[@property="v:genre"]/text()'))
                value['intro'] = doc_deatil.xpath('//span[@property="v:summary"]/text()')[0]
                detail_comms = doc_deatil.xpath('//div[@id="hot-comments"]/div[@class="comment-item"]/div[@class="comment"]')
                for comm in detail_comms:
                    comment = {}
                    comment['auth'] = comm.xpath('./h3/span[@class="comment-info"]/a/text()')[0]
                    comment['msg'] = comm.xpath('./p/text()')[0]
                    value['comments'].append(comment)
            data.append(value)
            #print(value)
        return data
    else:
        pass
#getMusic()