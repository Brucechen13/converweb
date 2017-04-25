import requests
import json,os
import base64
from Crypto.Cipher import AES
import codecs
import binascii
from lxml import etree

musicUrl = ['http://music.163.com/discover/toplist?id=3779629']
basicUrl = 'http://music.163.com'


def getMusic():
    return get_html(musicUrl[0])

def get_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host':'music.163.com',
        'Referer':'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = []        
        doc = etree.HTML(res.text)
        all_songs = doc.xpath('//ul[@class="f-hide"]/li')
        for i in range(0, min(10, len(all_songs))):
            music = {}
            music['url'] = all_songs[i].xpath('./a/@href')[0];
            music['comments'] = get_comments(music['url'][9:])
            music['title']  = all_songs[i].xpath('./a/text()')[0]
            res_detail = requests.get(basicUrl+music['url'] )
            if res_detail.status_code == 200:
                doc_detail = etree.HTML(res_detail.text)
                music['picUrl'] = doc_detail.xpath('//div[@class="u-cover u-cover-6 f-fl"]/img/@src')[0]
                infos = doc_detail.xpath('//div[@class="cnt"]/p[@class="des s-fc4"]')
                music['auth'] = infos[0].xpath('./span/@title')[0]
                music['album'] = infos[1].xpath('./a/text()')[0]
            else:
                pass
            music['url'] = basicUrl+music['url']
            data.append(music)
            #print(music)
        return data
    else:
        pass
    
# 由于网易云音乐歌曲评论采取AJAX填充的方式所以在HTML上爬不到，需要调用评论API，而API进行了加密处理，下面是相关解决的方法
def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    if (type(text)) is  str:
        text = text.encode('utf-8')
    text = text + (pad * chr(pad)).encode('utf-8')
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(binascii.b2a_hex(text.encode('utf-8')), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(xx)[2:]), os.urandom(size))))[0:16]

def get_comments(songId):
    comments = []
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(songId) + '/?csrf_token='
    headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/'}
    text = {'username': '', 'password': '', 'rememberLogin': 'true'}
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    req = requests.post(url, headers=headers, data=data)#
    total = req.json()['hotComments']
    for i in range(0, min(2, len(total))):
        comm = {}
        comment  = total[i]
        comm['content'] = comment['content']
        comm['userName'] = comment['user']['nickname']
        comm['userPic'] = comment['user']['avatarUrl']
        comments.append(comm)
    return comments
    
#print(getMusic())