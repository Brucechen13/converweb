import requests
import threading
from lxml import etree

basicUrl = ['http://www.23us.com/html/51/51514/','http://www.23us.com/html/24/24665/','http://www.23us.com/html/49/49940/']

def saveTxt(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host':'www.23us.com',
        'Referer':'http://www.23us.com/book/51514',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    res = requests.get(url, headers= headers)
    res.encoding = 'gbk'
    doc = etree.HTML(res.text)
    bodyText = doc.xpath('//div[@class = "bdsub"]/dl')[0]
    title = bodyText.xpath('./dd/h1/text()')[0].split(' ')[0]
    #print(title)
    book = open(title+'.txt', 'w', encoding='utf-8')
    book.write(title+"\n")
    chapters = doc.xpath('//td[@class="L"]/a')
    for i in range(0, min(100, len(chapters))):
        chapter = chapters[i]
        chapterTxt = chapter.xpath('./text()')[0]
        if (chapterTxt.find('章') != -1) and (chapterTxt.find("月票") == -1):
            #print(chapterTxt)
            book.write(chapterTxt+"\n")
            chapterUrl = chapter.xpath('./@href')[0]
            res_detail = requests.get(url+chapterUrl, headers= headers)
            res_detail.encoding = 'gbk'
            doc_detail = etree.HTML(res_detail.text)
            doc_detail = doc_detail.xpath('//dd[@id="contents"]')[0]
            contents = doc_detail.xpath('./text()')
            chapterTxt = ""
            for content in contents:
                chapterTxt += content
                chapterTxt += '\n'
            chapterTxt += '\n'            
            book.write(chapterTxt)
    book.close()
    
for i in range(len(basicUrl)):
    threading.Thread(target = saveTxt, args = (basicUrl[i], )).start()
    
    