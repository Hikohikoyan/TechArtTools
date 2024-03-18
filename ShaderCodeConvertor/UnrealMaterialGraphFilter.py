# 导入必要的库
import UnrealMaterialGraphDict as ue_dict

# 定义输入和输出文件路径
input_file = "input.txt"
output_file = "collection_for_unity_shader.txt"

# 读取输入文件内容
#with open(input_file, "r") as f:
#在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()


def clean_line(line, key):
    start_index = line.find(key)
    if start_index < 0:
        return line
    start_index += len(key)
    end_index = line.find(",", start_index)
    if end_index < 0:
        end_index = len(line)
    s = key.replace(",","") +"=" + line[start_index:end_index] + "\n"
    if is_key_in_line(s,"CustomProperties"):
        s = clean_line(s,"CustomProperties ")
        return clean_line(s,key)
    return s

def is_key_in_line(line, key):
    return key in line

def replace_content(content, custom_config):
    for key, value in custom_config.items():
        content = content.replace(key, value)
    return content

# 保留符合匹配的行 删除行首没有匹配到自定义配置项的行和空行
def replace_by_config(content,custom_config,start,end):
    
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        # 只保留符合行首匹配的行
        if any(line.lstrip().startswith(config) for config in custom_config):
            if is_key_in_line(line,start):
                new_lines.append("\n },")
                line = "{\n" + line 
            
            if is_key_in_line(line,end):
                new_lines.append("},")
                line = "{"
            new_lines.append(line+";\n")
    content = "".join(new_lines)
    return content

# 保留符合匹配的行 删除行首没有匹配到自定义配置项的行和空行
def match_by_config(content,custom_config):
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        line = line.lstrip()  # 去掉行首空格
        # 只保留符合行首匹配的行
        if any(line.startswith(config) for config in custom_config):
            line = "\n" + line 
            new_lines.append(line)
    content = "".join(new_lines)
    return content

# 如果行首匹配到onfig中的任何一个键，则去掉该行
def remove_lines(content, custom_config,start):
    lines = content.split("\n")  # 将字符串按行分割成一个列表
    new_lines = []
    for line in lines:
        line = line.lstrip()  # 去掉行首空格
        if line.startswith(tuple(custom_config.keys())):
            continue  
        if line.startswith(start):
            line = line.replace("(","").replace(")","")
            #line = clean_line(line,",Pin") +  clean_line(line,"LinkedTo")
            new_lines.append(line)  # 否则将该行加入新的列表中
        else:
            new_lines.append(line)  # 否则将该行加入新的列表中
    return "\n".join(new_lines)  # 将新的列表转换成字符串，每行以换行符连接起来

def clean_result(c):
    c = c.replace("{;","{").replace("=",":").replace("{\n},","").replace('{'+'},',"")
    return c


# Get Parameters Info
result = "{" + replace_by_config(content,ue_dict.match_param,ue_dict.param_start,ue_dict.param_end)+"}"
result = clean_result(replace_content(result,ue_dict.filter_dict_param))

result += "\n" + ue_dict.split_signal + "\n"

input_hlsl = "input.hlsl"
with open(input_hlsl, "r", encoding="utf-8") as f:
    hlsl_code = f.read()
hlsl = match_by_config(hlsl_code.lstrip(),ue_dict.filter_shader)
hlsl = hlsl.replace("},\n}","}")

# 将转换后的内容写入输出文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result + hlsl)