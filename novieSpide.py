import requests
import threading
from lxml import etree

basicUrl = "https://www.amazon.cn"
url = ['https://www.amazon.cn/gp/new-releases/books/ref=sv_b_2']

def getBooks():
    return get_html(url[0])

def get_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host':'www.amazon.cn',
        'Connection':'keep-alive',
        'Referer':'https://www.amazon.cn/gp/new-releases/books/ref=sv_b_2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    data = []
    res = requests.get(url, headers= headers)
    doc = etree.HTML(res.text)
    books = doc.xpath('//div[@class = "a-fixed-left-grid-col a-col-right"]')
    #print(len(books))
    for i in range(0, min(10, len(books))):
        content = books[i]
        book = {}
        book['url'] = basicUrl+content.xpath('./a/@href')[0]
        book['title'] = content.xpath('./a/div/text()')[0].strip()
        #print(book['title'])
        book['auther'] = content.xpath('./div[@class="a-row a-size-small"]/span/text()')[0]
        book_detail = etree.HTML(requests.get(book['url'], headers=headers).text)
        book['picUrl'] = book_detail.xpath('//div[@id="img-canvas"]/img/@data-a-dynamic-image')[0].split('":')[0][2:]
        book['intro'] = book_detail.xpath('//noscript/div/text()')[0]
        book_comments = book_detail.xpath('//div[@id="revMHRL"]/div[@class="a-section celwidget"]/div[@class="a-row a-spacing-micro"]')
        book['comments'] = []
        for comment in book_comments:
            commentDict = {}
            commentDict['msg'] = comment.xpath('./div/a')[1].xpath('./span/text()')[0]
            commentDict['auth'] = comment.xpath('./span/span[@class="a-size-normal"]/a/text()')[0]
            book['comments'].append(commentDict)
        data.append(book)
    return data

#print(get_html(url[0]))
    
    
    