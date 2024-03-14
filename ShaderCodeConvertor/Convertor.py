# 导入必要的库
import re
import json
# 定义输入和输出文件路径
input_file = "input.txt"
output_file = "output.txt"


# 定义hlsl shader code和cgsl的对应关系
shader_dict = {
    "float": "float",
    "int": "int",
    "bool": "bool",
    "float2": "vec2",
    "float3": "vec3",
    "float4": "vec4",
    "MaterialFloat":"float",
    "MaterialFloat2":"vec2",
    "MaterialFloat3":"vec3",
    "MaterialFloat4":"vec4",
    "float3x3": "mat3",
    "float4x4": "mat4",
    "MaterialFloat3x3": "mat3",
    "MaterialFloat4x4": "mat4",
    "Texture2D": "sampler2D",
    "SamplerState": "samplerState",
    "cbuffer": "uniform",
    "struct": "struct",
    "return": "return",
    "LinearInterpolate":"lerp",
    "Class=/Script/Engine." :"",
    "Begin Object":"",
    "Class=/Script/UnrealEd.MaterialGraphNode":"",
    '"':"",
    "Name=":" ",
    "MaterialExpression":"",
    "End Object":"\n"
}

# 定义自定义配置
custom_config = {
    # "#define",
    # "#include"
    #"#",
    #"    #",
    # "      MaterialExpressionEditorX",
    # "      MaterialExpressionEditorY",
    # "End Object",
    # "Begin Object",
    # "   End Object",
    # "   Begin Object",
    "   NodePosX":" ",
    "   NodePosY":" ",
    # "   CustomProperties",
    # "   NodeGuid=",
    # "      Material=",
    # "   bCanRenameNode",
    # "      MaterialExpressionGuid"
    # "NodeComment",
    # "Text",
    "Begin Object Class":" ",
    "MaterialExpressionEditorX":" ",
    "MaterialExpressionEditorY":" ",
    "EditorX":"",
    "EditorY":"",
    "NodePosY":"",
    "NodePosX":"",
    "CustomProperties":""
}

# 读取输入文件内容
#with open(input_file, "r") as f:
#在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
with open(input_file, "r", encoding="gbk") as f:
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

def replace_by_config(content,custom_config):
    # 删除行首没有匹配到自定义配置项的行和空行
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        # 只保留符合行首匹配的行
        if any(line.lstrip().startswith(config) for config in custom_config):
            # 替换hlsl shader code为cgsl
            for key, value in shader_dict.items():
                line = re.sub(r"\b{}\b".format(key), value, line)
            if is_key_in_line(line,"ParameterName"):
                new_lines.append("\n },")
                line = "{" + line
            new_lines.append(line)
    content = "".join(new_lines)
    return content

def remove_lines(content, custom_config):
    lines = content.split("\n")  # 将字符串按行分割成一个列表
    new_lines = []
    for line in lines:
        line = line.lstrip()  # 去掉行首空格
        if line.startswith(tuple(custom_config.keys())):
            continue  # 如果行首匹配到custom_config中的任何一个键，则跳过该行
        if line.startswith("CustomProperties"):
            line = line.replace("(","").replace(")","")
            line = clean_line(line,",Pin") +  clean_line(line,"LinkedTo")

            new_lines.append(line)  # 否则将该行加入新的列表中
        else:
            new_lines.append(line)  # 否则将该行加入新的列表中
    return "\n".join(new_lines)  # 将新的列表转换成字符串，每行以换行符连接起来

match_param = {
    "ParameterName",
    "Group",
    "Desc",
    "Texture=Texture2D"
}
content = "{" + replace_by_config(content,match_param)

# 将转换后的内容写入输出文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)