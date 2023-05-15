import json
import os

input_folder = "/home/wangxin/Desktop/doccano_work/Results"
safe_output_folder = "/home/wangxin/Desktop/doccano_work/Information_Results"
dangerous_output_folder = "/home/wangxin/Desktop/doccano_work/Permission_Results"

# 创建输出文件夹
os.makedirs(safe_output_folder, exist_ok=True)
os.makedirs(dangerous_output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    input_file = os.path.join(input_folder, filename)
    safe_output_file = os.path.join(safe_output_folder, filename)
    dangerous_output_file = os.path.join(dangerous_output_folder, filename)
    with open(input_file, "r", encoding="utf-8") as f, open(safe_output_file, "w", encoding="utf-8") as f_safe, open(dangerous_output_file, "w", encoding="utf-8") as f_dangerous:
        for line in f:
            obj = json.loads(line.strip())
            obj_id = obj["id"]
            obj_text = obj["text"]
            obj_label = obj["label"]
            has_dangerous = False
            for label in obj_label:
                if label[2] == "危险权限":
                    has_dangerous = True
                    break
            if has_dangerous:
                # 输出到dangerous_output_folder
                f_dangerous.write(json.dumps({"id": obj_id, "text": obj_text, "label": [label for label in obj_label if label[2] == "危险权限"]}, ensure_ascii=False) + "\n")
            else:
                # 输出到safe_output_folder
                f_safe.write(json.dumps({"id": obj_id, "text": obj_text, "label": [label for label in obj_label if label[2] != "危险权限"]}, ensure_ascii=False) + "\n")