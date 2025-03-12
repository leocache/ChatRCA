import csv

# 读取CSV文件
def read_csv(file_name):
    with open(file_name, mode='r', encoding='utf-8') as f:
        return list(csv.reader(f))

# 将CSV数据转换为Markdown表格
def csv_to_markdown(csv_path):
    csv_data = read_csv(csv_path)
    markdown_lines = ["| " + " | ".join(row) + " |" for row in csv_data]
    header_line = markdown_lines[0]
    # 修正这里，确定列数以生成分隔行
    separators = ["|" + " --- |" * len(csv_data[0])] if csv_data else []
    
    return "\n".join([header_line] + separators + markdown_lines[1:])


