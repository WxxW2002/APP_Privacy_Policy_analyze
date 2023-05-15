import os
import re

f=open("temp.txt",encoding="utf-8")
result = f.read()
# 利用正则式去除特殊符号
result = re.sub(r'\[', '', result)
result = re.sub(r'\]', '', result)
result = re.sub(r'\'', '', result)
result = re.sub(r', ', '\n', result)

print(result)
    

