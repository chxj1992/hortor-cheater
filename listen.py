import re
import json
from mitmproxy import ctx
from urllib.parse import quote
import string
import requests

def response(flow):
    path = flow.request.path
    if path == '/question/bat/findQuiz':
        content = flow.response.content
        data = json.loads(content)
        question = data['data']['quiz']
        options = data['data']['options']
        ctx.log.info('question : %s, options : %s'%(question, options))
        options = ask(question, options)
        data['data']['options'] = options
        flow.response.text = json.dumps(data)



def ask(question, options):
    # url = quote('http://www.baidu.com/s?wd=' + question, safe = string.printable)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}

    baidu_url = ['119.75.213.50','119.75.213.61','61.135.169.125','220.181.112.244','61.135.169.125']

    content = ""
    count = [0 for i in range(4)]
    for page_num in range(4):
        url= 'http://'+baidu_url[page_num]+'/s?wd=%s&tn=tn=baidulocal&ie=utf-8&pn=' %quote(question)
        url += str(page_num*10)
        # req=urlopen(search_url, headers=headers)
        # html=req.text
        content = requests.get(url,headers=headers).text
        for i, option in enumerate(options):
            count[i] += content.count(option)
    for i,option in enumerate(options):
        ctx.log.info('option : %s, count : %s'%(option, count[i]))
        options[i] = options[i] + ':' + str(count[i])
        # print("option: %s, count: %s"%(option, count))
    return options
