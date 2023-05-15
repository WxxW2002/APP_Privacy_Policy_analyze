# 导入 json 模块
import os
import json
from tqdm import tqdm
# 打开 JSON 文件并读取数据
files = os.listdir("/home/wangxin/Desktop/doccano_work/JSONS")

for fn in tqdm(files):
    p=os.path.join("/home/wangxin/Desktop/doccano_work/JSONS",fn)

    with open(p,mode="r",encoding="utf-8") as read_file:
        data = json.load(read_file)

        # 将数组中的对象转换为 JSON 字符串，并用空格分隔
        result = " ".join([json.dumps(record, ensure_ascii=False) + "\n" for record in data]).replace(" ", "")

        output_path = os.path.join("/home/wangxin/Desktop/doccano_work/JSONLS", fn)
        # 保存结果到一个新的 JSON 文件
        with open(output_path, "w", encoding="utf-8") as write_file:
            write_file.write(result)