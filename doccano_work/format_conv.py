import json
import os
from tqdm import tqdm

#获取path路径下的所有文件的名字(eg:123.txt)
files = os.listdir("/home/wangxin/Desktop/doccano_work/Results")  

for fn in tqdm(files):
    p=os.path.join("/home/wangxin/Desktop/doccano_work/Results",fn)
    with open(p,mode="r",encoding="utf-8") as f:
        lines = f.readlines()

        output = []
        for line in lines:
            data = json.loads(line)
            new_data = {
                'text': data['text'],
                'spans': [
                    {
                        'start': span[0],
                        'end': span[1],
                        'label': span[2]
                    } for span in data['label']
                ],
                "answer":"accept"
            }
            output.append(new_data)
    result = " ".join([json.dumps(record, ensure_ascii=False) + "\n" for record in output]).replace(" ", "")
    output_path = os.path.join("/home/wangxin/Desktop/doccano_work/Final_Results", fn)

    with open(output_path, "w", encoding="utf-8") as write_file:
            write_file.write(result)