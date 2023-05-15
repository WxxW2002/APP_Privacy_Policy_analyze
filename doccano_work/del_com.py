import os
import json
from tqdm import tqdm

files = os.listdir("/home/wangxin/Desktop/doccano_work/Output")

for fn in tqdm(files):
    p=os.path.join("/home/wangxin/Desktop/doccano_work/Output",fn)
    with open(p,mode="r",encoding="utf-8") as read_file:
        data = read_file.readlines()
        new_data = []
        for line in data:
            obj = json.loads(line)
            obj.pop('Comments', None)
            new_data.append(json.dumps(obj, ensure_ascii=False))

    output_path = os.path.join("/home/wangxin/Desktop/doccano_work/Results", fn)
    with open(output_path, "w", encoding="utf-8") as write_file:
            write_file.write('\n'.join(new_data))
