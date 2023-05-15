import json
import random

# 读取jsonl文件
with open('final_data.jsonl', 'r') as f:
    lines = f.readlines()

# 将所有行随机打乱
random.shuffle(lines)

# 去除每行开头的空格
lines = [line.lstrip() for line in lines]

# 写入新的jsonl文件
with open('shuffled_data.jsonl', 'w') as f:
    for line in lines:
        f.write(line)
