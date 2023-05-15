import json

input_file = 'anno_data3.jsonl'
output_file = 'final_data3.jsonl'

with open(input_file, 'r', encoding='utf-8') as in_file, open(output_file, 'w', encoding='utf-8') as out_file:
    for line in in_file:
        data = json.loads(line)
        out_file.write(json.dumps(data, ensure_ascii=False))
        out_file.write('\n')