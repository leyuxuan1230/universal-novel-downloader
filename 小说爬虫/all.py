import requests,time,os
from tqdm import *
from bs4 import *

def get_content(target,class_or_id,mmm):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    req = requests.get(url = target,headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    if int(class_or_id) == 0:
        texts = bf.find('div', class_=mmm)
    else:
        texts = bf.find('id', id=mmm)
    content = texts.text.strip().split('\xa0'*4)
    return content

def main(web_url,book_url,class_or_id,class_id,title_tag_h1,book_tag,text_div_class_or_id,class_id2):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    server = web_url
    target = book_url
    req = requests.get(url = target,headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    chapter_bs = BeautifulSoup(html, 'lxml')
    if int(class_or_id) == 0:
        chapters = chapter_bs.find('div', class_=class_id)
    else:
        chapters = chapter_bs.find('div', id=class_id)
    chapters = chapters.find_all('a')
    if title_tag_h1 == "y":
        x = chapter_bs.find('h1')
        x = x.text
        book_name = x + '.txt'
    else:
        x = chapter_bs.find(book_tag)
        x = x.text
        book_name = x + '.txt'
    print('正在下载',book_name)
    for chapter in tqdm(chapters,ncols = 72):
        chapter_name = chapter.string
        if jue_dui == 1:
            url = chapter.get('href')
        else:
            url = server + chapter.get('href')
        content = get_content(url,int(text_div_class_or_id),class_id2)
        with open(book_name, 'a', encoding='utf-8') as f:
            f.write(chapter_name)
            f.write('\n')
            f.write('\n'.join(content))
            f.write('\n')

web_url=input('这个小说站的url是什么？（如：http://www.kehuan.net.cn/）\n')

book_url=input('这本书的目录页的url是什么？（如：http://www.kehuan.net.cn/book/leiren.html）\n')

class_or_id=int(input('含有整个目录的div标签是class属性(0)还是id属性(1)？\n'))
if class_or_id == 0:
    class_id=input('那么这个div的class属性是什么呢？\n')
else:
    class_id=input('那么这个div的id属性是什么呢？\n')

title_tag_h1=input('如果我没有弄错的话，标题应该是在h1标签里吧（y，n）：')
if title_tag_h1=='n':
    book_tag=input('请输入书名所在的标签:')
else:
    book_tag='h1'
print('现在让我们打开其中的一章')
text_div_class_or_id=input('其中包含所有文字的div标签是class属性(0)还是id属性(1)？\n')
if int(text_div_class_or_id) == 0:
    class_id2=input('那么这个div的class属性是什么呢？\n')
else:
    class_id2=input('那么这个div的id属性是什么呢？\n')

jue_dui=int(input('目录页中章节的url是绝对路径(1)还是相对的(2)？\n'))

main(web_url,book_url,class_or_id,class_id,title_tag_h1,book_tag,text_div_class_or_id,class_id2)

