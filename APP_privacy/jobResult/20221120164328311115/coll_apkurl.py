import json
import jsonpath

obj = json.load(open('index.json', 'r', encoding='utf-8')) 
apkurl = jsonpath.jsonpath(obj, '$..apkurl')
print(apkurl)
