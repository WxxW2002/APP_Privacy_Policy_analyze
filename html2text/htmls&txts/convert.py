import os
import re
import html2text
import subprocess

root_dir = r"/home/wangxin/Desktop/html2text/htmls&txts/htmls"

for file in os.listdir(root_dir):
    result = subprocess.getoutput('html2text ./htmls/'+file)
    # 利用正则式去除特殊符号
    result = re.sub(r'\|', '', result)
    result = re.sub(r'\*\*', '', result)
    result = re.sub(r'\*', '', result)
    result = re.sub(r' *$', '', result)
    result = re.sub(r'\n\n+', r'\n\n', result)
    result = re.sub(r'^\n+', '', result)
    result = re.sub(r'\#', '', result)
    result = re.sub(r'\#\#', '', result)
    result = re.sub(r'\#\#\#', '', result)
    result = re.sub(r'\#\#\#\#', '', result)
    result = re.sub(r'\#\#\#\#\#', '', result)
    result = re.sub(r'\※', '', result)
    result = re.sub(r'\>', '', result)
    result = re.sub(r'\-\-\-', '', result)
    result = re.sub(r'\s*\n', '\n', result)
    result = re.sub('http://\S+|https://\S+', '', result)
    result = re.sub('http[s]?://\S+', '', result)
    result = re.sub(r'http\S+', '', result)
    
    with open("/home/wangxin/Desktop/html2text/htmls&txts/txts/{0}.txt".format(file),"a",encoding="utf-8") as file_handle: 
        file_handle.write(result)     #将txt文本依次写入文件夹中
    

