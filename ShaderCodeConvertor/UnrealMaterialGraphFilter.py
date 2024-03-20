# 导入必要的库
import UnrealMaterialGraphDict as ue_dict
import GlobalSettings as gls


def clean_line(line, key):
    start_index = line.find(key)
    if start_index < 0:
        return line
    start_index += len(key)
    end_index = line.find(",", start_index)
    if end_index < 0:
        end_index = len(line)
    s = key.replace(",", "") + "=" + line[start_index:end_index] + "\n"
    if is_key_in_line(s, "CustomProperties"):
        s = clean_line(s, "CustomProperties ")
        return clean_line(s, key)
    return s


def is_key_in_line(line, key):
    return line.find(key) != -1


def replace_content(content, custom_config):
    for key, value in custom_config.items():
        content = content.replace(key, value)
    return content


# 保留符合匹配的行 删除行首没有匹配到自定义配置项的行和空行
def replace_by_config(content, custom_config, start, end):
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        # 只保留符合行首匹配的行
        if any(line.lstrip().startswith(config) for config in custom_config):
            if is_key_in_line(line, start):
                new_lines.append("\n },")
                line = "{\n" + line

            if is_key_in_line(line, end):
                new_lines.append("},")
                line = "{"
            new_lines.append(line + ";\n")
    content = "".join(new_lines)
    return content


# 保留符合匹配的行 删除行首没有匹配到自定义配置项的行和空行
def match_by_config(content, custom_config):
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


# 如果行首匹配到config中的任何一个键，则去掉该行
def remove_lines(content, custom_config):
    lines = content.split("\n")  # 将字符串按行分割成一个列表
    new_lines = []
    for line in lines:
        line = line.lstrip()  # 去掉行首空格
        for key in custom_config:
            if is_key_in_line(line, key):
                continue
            new_lines.append(line)
    return "\n".join(new_lines)  # 将新的列表转换成字符串，每行以换行符连接起来


def clean_result(c):
    c = c.replace("{;", "{").replace("=", ":").replace("{\n},", "").replace('{' + '},', "")
    return c


def main():
    print("当前运行模块为 : UE Graph Filter 过滤材质节点模块 ")
    if not gls.check_status("需要过滤材质节点吗?", "UE Graph Filter::Main"):
        return False

    path = ""
    # 定义输入和输出文件路径
    input_file = gls.check_input("输入拷贝GraphNode的文件路径", "file")
    output_file = gls.check_input("输入输出文件路径", "file")

    content = gls.read_file(input_file)
    content = content.replace(gls.sign, "\n")

    # Get Parameters Info
    result = "{" + replace_by_config(content, ue_dict.match_param, ue_dict.param_start, ue_dict.param_end) + "}"
    result = clean_result(replace_content(result, ue_dict.filter_dict_param))

    result += "\n" + ue_dict.split_signal + "\n"

    input_hlsl = gls.check_input("输入拷贝的HLSL文件路径", "file")
    hlsl_code = gls.read_file(input_hlsl)
    hlsl_code = hlsl_code.replace(gls.sign, "\n")

    hlsl = match_by_config(hlsl_code.lstrip(), ue_dict.filter_shader)
    hlsl = hlsl.replace("},\n}", "}")

    gls.write_file(output_file, result + hlsl)
    # 将转换后的内容写入输出文件
    return True


