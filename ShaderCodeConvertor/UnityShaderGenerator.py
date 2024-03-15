# 导入必要的库
import re
import json
import Convertor
# 定义输入和输出文件路径
input_file = "output.txt"
output_cginc = "gen.cginc"
output_shader = "gen.shader"

log_file = "Log.txt"
log = ""


# 定义hlsl shader code和cgsl的对应关系
cginc_dict = {
    "Texture":"sampler2D",
    "float":"half",
    "int" :"half",
    "float3":"half3",
    "float4":"half4",
}

shader_dict = {
    "Texture" : ', 2D) =',
    "int" : ", Range(0,1)) = ",
    "float" : ", Range(0,1)) = ",
    "float3" : ", Vector) =",
    "float4":", Vector) =",
    "Color":", Color) = (1,1,1)"
}

#texture_type
texture_type ={
    "SAMPLERTYPE_Normal":"bump",
    "SAMPLERTYPE_LinearColor":"black",
}

# 读取输入文件内容
#with open(input_file, "r") as f:
#在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

def write_log(func,s):
    global log 
    log += func  + " " + "\n    " + s + ""
    return log
def make_param(t,n,config):
    #input type name
    res = ""
    res = Convertor.replace_content(t,config) + " " + n
    return res

def make_comment(desc):
    return "// "+desc


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

def decode_input(item):

    pack = {
        "param_name" : "",
        "param_type" :"",
        "param_group" : "",
        "param_desc" :"",
        "param_val" : "",
        "isNotTexture":False,
        "isColor":False,
        "isBoolean":False,
        "texture_val":""
    }
    item = item.replace(",{","").replace("\n","").replace("{","")
    for info in item.split(";"):
        
        if len(info.split(":"))<2:
            continue
        info_type = "".join(info.split(":")[0]).replace("}","").replace("{","")
        info_val = info.replace(info_type,"").replace(":","").replace('"',"")
        # #debug
        # write_log("" ,"info_type:  " + info_type)
        # write_log("" ,"info_val:  " + info_val)

        # get ParameterName
        if (Convertor.is_key_in_line(info_type,"ParameterName")):
            pack["param_name"] = info_val
            if Convertor.is_key_in_line(info_val,"Tex"):
                pack["isNotTexture"] = True

        # get ParameterGroup
        if (Convertor.is_key_in_line(info_type,"Group")):
            pack["param_group"] = info_val
            if Convertor.is_key_in_line(info_val,"贴图"):
                pack["isNotTexture"] = True

        # get ParameterDesc
        if (Convertor.is_key_in_line(info_type,"Desc")):
            pack["param_desc"] = info_val

        # get ParameterValue
        if (Convertor.is_key_in_line(info_type,"DefaultValue")):
            pack["param_val"] = clean_value(info_val)

        # get TextureValue
        if (Convertor.is_key_in_line(info_type,"SamplerType")):
            pack["isNotTexture"] = True
            pack["texture_val"] = info_val

    #debug
    # write_log("" ,"param_val:" +pack["param_val"])
    # write_log("" ,"param_name:" +pack["param_name"])
    # write_log("decode_input" ,"param_desc:" +pack["param_desc"])
    if pack["isNotTexture"] :
        #贴图参数
        pack["param_type"] = "Texture"
    else:
        pack["param_type"] = identify_float_type(pack["param_val"])
    return pack
    
def write_cginc(content):
    params = content.replace("\n","").replace(" ","").split("}")
    res = []
    for info in params:
        item = decode_input(info)
        isNotTex = not item["isNotTexture"]
        checkstatus = isNotTex and item["param_val"]==""
        checkstatus = checkstatus or item["param_name"] == ""
        if item == None or checkstatus:
            continue
        t = make_param(item["param_type"],item["param_name"],cginc_dict).replace(";","") +";"
        res.append(t)
        d = make_comment( item["param_desc"])+"\n"
        res.append(d)

    #print(type(json_str))
    return "\n".join(res)  # 将新的列表转换成字符串，每行以换行符连接起来

def write_shader(content):

    params = content.replace("\n","").replace(" ","").split("}")
    res = []
    for info in params:
        item = decode_input(info)
        isNotTex = not item["isNotTexture"]
        checkstatus = isNotTex and item["param_val"]==""
        checkstatus = checkstatus or item["param_name"] == ""
        if item == None or checkstatus:
            continue
        name = item["param_name"]
        val = clean_value(item["param_val"])
        desc = item["param_desc"]
        type_str = item["param_type"]

        write_log("\nwrite_shader","name " + name + " val " + val +" type_str " + type_str)
        if identify_float_type(val) != "float" and Convertor.is_key_in_line(name,"Color") and isNotTex:
            type_str = "Color"
            val = "("+val+")"
        line = "_" + name + '("' + desc + " " + name + '"'+ make_param(type_str,"",shader_dict).replace(";","")
        if type_str == "Texture":
            write_log("\nwrite_shader","texture_val " + item["texture_val"])
            line += '"' 
            if( item["texture_val"] != ""):
                line += Convertor.replace_content(item["texture_val"],texture_type)
            else:
                line += "white"
            line += '" {' + '}'
        elif type_str != "Color":
            range_str = "Range(0," + val +")"
            line.replace(" Range(0,1)",range_str)
            line += " " + val
        res.append( line )
        write_log("\nwrite_shader",line)
        res.append(make_comment( desc)+"\n")
        
    #print(type(json_str))
    return "\n".join(res)  # 将新的列表转换成字符串，每行以换行符连接起来


result_cginc = write_cginc(content)
result_shader = write_shader(content)

#将转换后的内容写入输出文件
with open(output_cginc, "w", encoding="utf-8") as f:
    f.write(result_cginc)

#将转换后的内容写入输出文件
with open(output_shader, "w", encoding="utf-8") as f:
    f.write(result_shader)

with open(log_file, "w", encoding="utf-8") as f:
    f.write(log)