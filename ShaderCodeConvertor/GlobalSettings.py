# 导入必要的库
import re

log_file = "Log.txt"
log = ""

def write_log(func,s):
    global log 
    log += func  + " " + "\n    " + s + ""
    return log

def make_comment(desc):
    return "// "+desc


#判断所表达的浮点数数据类型是float|float3|float4|未知
def identify_float_type(s):
    # 去掉字符串中的字母
    s = re.sub('[^0-9,.]', '', s)
    # 统计字符串中“,”的个数
    num_commas = s.count(',')
    isInt = s.count('.')<1
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

#制作缩进数量 同’tab'键
def make_indentation(num):
    res = []
    space = "    "
    for i in range(0,num): 
        res.append(space)
    return "".join(res)

def clean_value(v):
    val_type = identify_float_type(v)
    s = ""
    if val_type == "int":
        s = v.replace(".","")  # 匹配小数点前面的数字，如果是整数，则去掉小数点
    else:
        s = v.replace("(","").replace(")","")
        if val_type == "float":
            s = re.sub('[^0-9,.]', '', v)
            s = re.sub(r"(\.\d*?)0+$", r"\1",s)+"0"
        else :
            s = re.sub('[^0-9,.]', '', v)
            t = []
            num = 0
            for i in s.split(","):
                num += 1
                i = re.sub(r"(\.\d*?)0+$", r"\1",i)+"0"
                if num < len(s.split(",")):
                    t.append(i + ",")
                else:
                    t.append(i)
            s = "".join(t)
    #debug
    write_log("\nclean_value","val_type " + val_type + "  return " + s)
    return s

#根据起始和结束的行号读取文件
def get_line_from_rowindex(file_path, start_line, end_line):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        string = ''
        for i in range(start_line - 1, end_line):
            string += lines[i]
        return string