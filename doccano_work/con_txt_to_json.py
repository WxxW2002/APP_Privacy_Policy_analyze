import os
import json
from tqdm import tqdm

#获取path路径下的所有文件的名字(eg:123.txt)
files = os.listdir("/home/wangxin/Desktop/doccano_work/TXTS")   

for fn in tqdm(files):
    p=os.path.join("/home/wangxin/Desktop/doccano_work/TXTS",fn)

    # 大多数文件都是utf-8格式的，少数文件是gbk格式，默认使用utf-8格式读取，为了防止gbk文件使程序中断,使用try catch处理特殊情况
    f=open(p,mode="r",encoding="utf-8")
    content = f.read()
    lines = content.split("\n")
    objects = []
    for line in lines:
        obj = {}
        obj["text"] = line
        objects.append(obj)

    output_file = fn.replace(".txt", ".json")
    output_path = os.path.join("/home/wangxin/Desktop/doccano_work/JSONS", output_file)
    with open(output_path, "w", encoding="utf-8") as f:
            json.dump(objects, f, ensure_ascii=False)
