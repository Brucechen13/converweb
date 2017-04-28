import requests
from lxml import etree

url = 'http://www.smzdm.com/jingxuan/'

def getGoods():
    return get_html(url)

def get_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host':'www.smzdm.com',
        'Connection':'keep-alive',
        'Referer':'http://www.smzdm.com/?utm_source=baidu&utm_medium=cpc&utm_term=&utm_campaign=Ppmeitao',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    data = []
    res = requests.get(url, headers= headers)
    doc = etree.HTML(res.text) 
    goodsItems = doc.xpath('//li[@class="feed-row-wide"]')
    #print(len(goodsItems))
    for item in goodsItems:
        goods = {}
        price = item.xpath('./h5/a/span/text()')
        if len(price) >= 1:
            goods['title'] = item.xpath('./h5/a/text()')[0]   
            goods['price'] = price[0]
            goods['pic'] = item.xpath('./div//img/@src')[0]
            intros = item.xpath('.//div[@class="feed-block-descripe"]')[0]
            goods['url'] = intros.xpath('./a/@href')[0]
            texts = intros.xpath('.//text()')
            goods['intro'] = (''.join(texts[1:-2]))
            goods['store'] = item.xpath('//span[@class="feed-block-extras"]/a/text()')[0]
            data.append(goods)
    return data
            
            

#print(get_html(url))