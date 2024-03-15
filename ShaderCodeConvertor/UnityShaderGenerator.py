# 导入必要的库
import re
import json
import Convertor
# 定义输入和输出文件路径
input_file = "output.txt"
output_cginc = "gen.cginc"
output_shader = "gen.shader"

# 定义hlsl shader code和cgsl的对应关系
cginc_dict = {
    "Texture":"sampler2D",
    "float":"half",
    "float3":"half3",
    "float4":"half4",
}

shader_dict = {
    "Texture" : ', 2D) ="white" {'+'}',
    "float" : ", Range(0,1)) =  ",
    "float3" : ", Vector) = ",
    "float4":", Vector) = ",
    "Color":", Color) = (1,1,1)"
}

#

# 读取输入文件内容
#with open(input_file, "r") as f:
#在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

def make_param(t,n,config):
    #input type name
    res = ""
    res = Convertor.replace_content(t,config) + " " + n
    return res

def make_comment(desc):
    return "// "+desc

def decode_input(item):
    pack = {
        "param_name" : "",
        "param_type" :"",
        "param_group" : "",
        "param_desc" :"",
        "param_val" : "",
        "isTexture":False,
        "texture_val":""
    }
    for info in item.split(";"):
        info = info.split("=")
        if len(info)<2:
            #print("ERROR: NO VALUE in" + "".join(info))
            continue
        info_type = "".join(info[0]).replace("}","").replace(",","").replace("{","")
        info_val = "".join(info[1])
        
        #debug
        #print(info_type + " = "+ info_val +"\n")
        
        # get ParameterName
        if (Convertor.is_key_in_line(info_type,"ParameterName")):
            pack["param_name"] = info_val


        # get ParameterGroup
        if (Convertor.is_key_in_line(info_type,"Group")):
            pack["param_group"] = info_val


        # get ParameterDesc
        if (Convertor.is_key_in_line(info_type,"Desc")):
            pack["param_desc"] = info_val


        # get ParameterValue
        if (Convertor.is_key_in_line(info_type,"DefaultValue")):
            pack["param_val"] = info_val

        # get TextureValue
        if (Convertor.is_key_in_line(info_type,"Texture")):
            pack["isTexture"] = True
            pack["texture_val"] = info_val

    if pack["isTexture"] :
        #贴图参数
        pack["param_type"] = "Texture"
    else:
        if pack["param_val"] == "" :
            #print("ERROR: NO VALUE in 【" + pack["param_name"] +"】\n")
            return pack
        
        #get value type
        pack["param_val"] = pack["param_val"].replace("(","").replace(")","")
        v = ""
        if len(pack["param_val"].split(",")) > 0:
            v = ""
        else:
            v = str(len(pack["param_val"].split(",")))
        pack["param_type"] = "float" + v
    return pack
    
def write_cginc(content):
    params = content.replace("\n","").replace(" ","").split("}")
    res = []
    for info in params:
        item = decode_input(info)
        if item == None or item["param_val"] == "" :
            continue
        res.append(make_param(item["param_type"],item["param_name"],cginc_dict).replace(";","") +";")
        res.append(make_comment( item["param_desc"])+"\n")
    #print(type(json_str))
    return "\n".join(res)  # 将新的列表转换成字符串，每行以换行符连接起来

def write_shader(content):

    params = content.replace("\n","").replace(" ","").split("}")
    res = []
    for info in params:
        item = decode_input(info)
        if item == None or item["param_val"] == "" :
            continue
        res.append(make_param(item["param_type"],item["param_name"],shader_dict).replace(";","") +";")
        res.append(make_comment( item["param_desc"])+"\n")
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