# 导入必要的库
import re
import json
from typing import Dict
import os

log_file = "Log.txt"
log = ""
sign = "////"

def convertRGB():
    n = input("请输入RGB值")
    n = n.replace("(","")
    n = n.replace(")","")
    new_str = n.split(",")
    res =""
    i = 0
    for s in new_str:
        i +=1
        res += str('{:.2f}'.format(int(s)/255))
        if i != len(new_str):
            res += ","
    print("("+res +")")

#convertRGB()


def read_file(input):
    res = ""
    with open(input, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        res += line + "  " + sign
    res = res.replace(sign, "")
    return res


def get_lines_from_file(input):
    with open(input, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        return lines


def write_file(input, content):
    if os.path.isfile(input):
        with open(input, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    else:
        print("输入文件路径非法")
        return False


def write_log(func, s):
    global log
    log += func + " " + "\n    " + s
    # 输出Debug Log
    log_file = "Log.txt"
    write_file(log_file, log)
    return log


def make_comment(desc):
    return "// " + desc


# 判断所表达的浮点数数据类型是float|float3|float4|未知
def identify_float_type(s):
    # 去掉字符串中的字母
    s = re.sub('[^0-9,.]', '', s)
    # 统计字符串中“,”的个数
    num_commas = s.count(',')
    isInt = s.count('.') < 1
    # 如果字符串中没有“,”，则为float类型
    if isInt:
        return "int"
    elif num_commas == 0:
        return "float"
    elif num_commas == 2:
        return "float3"
    elif num_commas == 3:
        return "float4"
    else:
        return "未知类型"


# 制作缩进数量 同’tab'键
def make_indentation(num):
    res = []
    space = "    "
    for i in range(0, num):
        res.append(space)
    return "".join(res)


def check_status(str, func):
    status = input(str + " 回答Y/N :")
    if status.count("n") > 0 or status.count("N") > 0:
        print("跳过执行 " + func)
        return False
    if status.count("Y") > 0 or status.count("y") > 0:
        return True
    print("输入不包含Yes 跳过执行 " + func + " 只使用函数定义")
    return False


def is_file(str):
    return os.path.isfile(str)


def check_input(str, type):
    a = input(str)
    check_state = False
    if type == "num":
        pattern = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
        check_state = pattern.match(a) is not None
    if type == "file":
        check_state = is_file(a)
    if type == "path":
        check_state = os.path.exists(a)
    if not check_state:
        print("输入有误 需要重新输入 ")
        print("\n输入类型应为" + type)
        a = check_input(str, type)
    return a


def clean_str(v):
    pattern = re.compile(r'[^\w=]|[\s]+|[{}|<>()+~`^]')
    return pattern.sub("", v)


# print(clean_str(' _BaseColorTex("颜色贴图BaseColo;;rTex", 2D) = "white" {}'))

def clean_value(v):
    val_type = identify_float_type(v)
    s = ""
    if val_type == "int":
        s = v.replace(".", "")  # 匹配小数点前面的数字，如果是整数，则去掉小数点
    else:
        s = v.replace("(", "").replace(")", "")
        if val_type == "float":
            s = re.sub('[^0-9,.]', '', v)
            s = re.sub(r"(\.\d*?)0+$", r"\1", s) + "0"
        else:
            s = re.sub('[^0-9,.]', '', v)
            t = []
            num = 0
            for i in s.split(","):
                num += 1
                i = re.sub(r"(\.\d*?)0+$", r"\1", i) + "0"
                if num < len(s.split(",")):
                    t.append(i + ",")
                else:
                    t.append(i)
            s = "".join(t)
    # debug
    # write_log("\nclean_value","val_type " + val_type + "  return " + s)
    return s


# 根据起始和结束的行号读取文件
def get_line_from_index(file_path, start_line, end_line):
    if not os.path.isfile(file_path):
        print("输入文件路径非法")
        return ""
    lines = get_lines_from_file(file_path)
    print("输入文件总行数为 " + str(len(lines)))
    start_line = int(start_line)
    end_line = int(end_line)
    string = ''
    for i in range(start_line - 1, end_line):
        string += lines[i]
    #write_log("\nget_line_from_index\n",string)
    return string


# 键值对反转
def reverse_dict(input):
    return {value: key for key, value in input.items()}


# 映射参数表
def match_keys(mapping_a: Dict[str, str], mapping_b: Dict[str, str]) -> Dict[str, str]:
    write_log("\nmatch_keys  \n A = ", json.dumps(mapping_a))
    write_log("\nmatch_keys  \n B = ", json.dumps(mapping_b))
    # 将mapping_a和mapping_b中的键值对反转，方便后续的匹配操作
    reverse_mapping_a = reverse_dict(mapping_a)
    reverse_mapping_b = reverse_dict(mapping_b)

    # 遍历reverse_mapping_a中的每个键，查找是否存在于reverse_mapping_b中
    result = {}
    for key in reverse_mapping_a:
        if key in reverse_mapping_b:
            result[reverse_mapping_a[key]] = reverse_mapping_b[key]
        else:
            result[reverse_mapping_a[key]] = ""
    write_log("\nmatch_keys  \n result = ", json.dumps(result))
    return result


def remove_inner_string(s, start_str, end_str):
    pattern = re.compile(re.escape(start_str) + ".*?" + re.escape(end_str))
    return pattern.sub("", s)


def merge_single_to_pack():
    text = read_file("input.txt")#input("输入文件"))
    txts = text.split(";")
    single = []
    ref = []
    log = ""
    for line in txts:
        line = line.lstrip()
        isHalf = line.startswith("half ")
        isFloat = line.startswith("float ")
        if isHalf | isFloat:
            val = line.split("=")
            attr = val[0].split(" ")
            if len(attr)<=0:
                print("no attr")
                continue
            single.append({"name":attr[1].replace(" ",""),"val":val[1].replace(";","")})
            log += "\n" + attr[1].replace(" ","") + " : " + val[1].replace(";","")
            text = text.replace(line+";","")
    temp_item = {"name":"none","val":"0"}
    temp = [temp_item,temp_item,temp_item,temp_item]
    count = 0
    str_comment = ""

    for item in single:
        # log += "\n"+str(count) +  item["name"] + item["val"]
        if count == 4 :
            ref.append({"pack":temp,"comment":str_comment})
            print("append")
            count = 0
            str_comment = ""
            temp_item = {"name": "none", "val": "0"}
            temp = [temp_item,temp_item,temp_item,temp_item]
        temp[count] = item
        str_comment += item["name"] +"|"
        count += 1

        if count == len(single):
            ref.append({"pack": temp, "comment": str_comment})
            count = 0
            str_comment = ""
            temp_item = {"name": "none", "val": "0"}
            temp = [temp_item, temp_item, temp_item, temp_item]

    pack_prefix = input("合并为Half4的prefix  :")
    pack_count = 0

    for item in ref:
        attr_x_name = item["pack"][0]["name"]
        attr_x_val = item["pack"][0]["val"]
        attr_y_name = item["pack"][1]["name"]
        attr_y_val = item["pack"][1]["val"]
        attr_z_name = "none"
        attr_z_val = "0"
        attr_w_name = "none"
        attr_w_val = "0"
        if len(single)>2:
            attr_z_name = item["pack"][2]["name"]
            attr_z_val = item["pack"][2]["val"]
        if len(single)>3:
            attr_w_name = item["pack"][3]["name"]
            attr_w_val = item["pack"][3]["val"]
        new_name = pack_prefix +"_" + str(pack_count)
        new_attr = "half4 " + new_name +" ="
        new_attr += "half4( " +attr_x_val +" , "
        new_attr += attr_y_val +" , "
        new_attr += attr_z_val +" , "
        new_attr += attr_w_val +" ); "
        pack_count += 1
        text = "//Output Pack \n" + new_attr +"//@special replace" + text
        print(new_attr)
        text = text.replace(attr_x_name,new_name +".x");
        text = text.replace(attr_y_name,new_name +".y");
        text = text.replace(attr_z_name,new_name +".z");
        text = text.replace(attr_w_name,new_name +".w");
        text = text.replace("//@special replace"," // " + item["comment"]);
    print(log)
    print(text)


#convertRGB()