import re
import json
from mitmproxy import ctx
from urllib.parse import quote
import string
import requests
import webbrowser

def response(flow):
    path = flow.request.path
    if path == '/question/bat/findQuiz':
        data = json.loads(flow.response.text)
        question = data['data']['quiz']
        options = data['data']['options']
        ctx.log.info('question : %s, options : %s'%(question, options))
        options = ask(question, options)
        data['data']['options'] = options
        flow.response.text = json.dumps(data)


def ask(question, options):
    url = quote('https://www.baidu.com/s?wd=' + question, safe = string.printable)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    content = requests.get(url, headers=headers).text
    answer = []
    for option in options:
        count = content.count(option)
        ctx.log.info('option : %s, count : %s'%(option, count))
        answer.append(option + ' [' + str(count) + ']')
    return answer

