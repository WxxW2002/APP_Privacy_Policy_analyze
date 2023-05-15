import json
import jsonpath

obj = json.load(open('index.json', 'r', encoding='utf-8')) 
texturl = jsonpath.jsonpath(obj, '$..texturl')
print(texturl)
