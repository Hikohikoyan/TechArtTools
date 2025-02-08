import re
# 定义正则表达式
define_pattern = r'^\s*(float|int|bool|half|uint|struct|sampler|texture)\s+\w+\s*;'
function_pattern = r'^\s*(float|int|bool|half|uint|struct|sampler|texture)\s+\w+\s*\(.*\)\s*\{'
#calculation_pattern = r'^\s*[\w\s\*]+\s*=\s*[\w\s\*]+\(.*\);'

cbuffer_pattern = r'cbuffer\s+\w+\s*:\s*register\(\w+\)\s*\{[^}]*\}'
sampler_pattern = r'SamplerState\s+\w+\s*:\s*register\(\w+\);'
struct_pattern = r'struct\s+\w+\s*\{[^}]*\};'
calculation_pattern = r'^\s*[\w\s\*]+\s*=\s*[^;]+;'

branch_start_block = r'if\s*\)\s*\{[^}]*\}'
branch_sub_block = r'else\s*\{[^}]*\}'

import re

import re

def match_param(params,c):


    # 假设 c 是一个条件表达式，替换参数
    # 使用正则表达式查找所有的 slot1, slot2, ...
    def replace_slots(match):
        slot_name = match.group(0)
        idx = int(slot_name.replace(" ", "").replace("slot", ""))
        idx -= 1
        if len(params) > idx:
            # print(params[idx])
            return params[idx]
        return slot_name  # 否则返回原始 slot 名称

    # 使用正则表达式替换 c 中的 slot
    slot_pattern = r'\b(slot\d+)\b'  # 匹配 slot1, slot2, ...
    result = re.sub(slot_pattern, replace_slots, c)
    return result
def replace_function_call(a, b, c,comment):
    origin = b
    # 定义正则表达式来匹配函数调用
    bHasValueDefine = b.count('((') > 1
    bHasValueDefine |= b.count('))') > 1
    if bHasValueDefine:
        return origin
    else:
        pattern = r'\b' + re.escape(a) + r'\s*\(([^)]+)\)'

        # 提取函数调用中的参数
        match = re.search(pattern, b)
        if match:
            # 获取函数调用的参数
            params_str = match.group(1).strip()

            # 使用正则表达式根据运算符分割参数
            # 这里我们假设参数之间可能有空格
            params = re.split(r'\s*[\,\+\-\*/>=<]+\s*', params_str)
            # 去掉参数的空白字符
            params = [param.strip() for param in params]
            result = match_param(params,c)
            # 替换 b 中的函数调用为结果
            return b.replace(match.group(0), result) +"\n //Original Codes : "  + origin + comment +  " \n"

        # 如果没有匹配到函数调用，返回原始文本
        return origin
#
# # 示例用法
# a = "pow"
# b = "r4.x = pow(r1.y,2);"
# c = "slot1 * slot1"
#
# result = replace_function_call(a, b, c)
# print(result)