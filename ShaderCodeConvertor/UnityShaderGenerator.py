# 导入必要的库
import GlobalSettings as gls
import UnrealMaterialGraphDict as ue_dict
import UnityShaderConfig as unity_config
import UnrealMaterialGraphFilter as graph_nodes
# 定义输入和输出文件路径
input_file = "collection_for_unity_shader.txt" 
#input("请输入For Unity的TXT 路径：")
output_cginc = unity_config.cginc
output_shader = unity_config.shader

log_file = "Log.txt"
log = ""


# 定义hlsl shader code和cgsl的对应关系
cginc_dict = unity_config.cginc_dict

shader_dict = unity_config.shader_dict

#texture_type
texture_type =unity_config.texture_type

# 读取输入文件内容
#with open(input_file, "r") as f:
#在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()


def make_param(t,n,config):
    #input type name
    res = ""
    res = graph_nodes.replace_content(t,config) + " " + n
    return res


#解析数据包
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
        # gls.write_log("" ,"info_type:  " + info_type)
        # gls.write_log("" ,"info_val:  " + info_val)

        # get ParameterName
        if (graph_nodes.is_key_in_line(info_type,"ParameterName")):
            pack["param_name"] = info_val
            if graph_nodes.is_key_in_line(info_val,"Tex"):
                pack["isNotTexture"] = True

        # get ParameterGroup
        if (graph_nodes.is_key_in_line(info_type,"Group")):
            pack["param_group"] = info_val
            if graph_nodes.is_key_in_line(info_val,"贴图"):
                pack["isNotTexture"] = True

        # get ParameterDesc
        if (graph_nodes.is_key_in_line(info_type,"Desc")):
            pack["param_desc"] = info_val

        # get ParameterValue
        if (graph_nodes.is_key_in_line(info_type,"DefaultValue")):
            pack["param_val"] = gls.clean_value(info_val)

        # get TextureValue
        if (graph_nodes.is_key_in_line(info_type,"SamplerType")):
            pack["isNotTexture"] = True
            pack["texture_val"] = info_val

    #debug
    # gls.write_log("" ,"param_val:" +pack["param_val"])
    # gls.write_log("" ,"param_name:" +pack["param_name"])
    # gls.write_log("decode_input" ,"param_desc:" +pack["param_desc"])
    if pack["isNotTexture"] :
        #贴图参数
        pack["param_type"] = "Texture"
    else:
        pack["param_type"] = gls.identify_float_type(pack["param_val"])
    return pack

#制作cginc文件
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
        desc = item["param_desc"]
        if desc == "":
            desc = item["param_group"]
        d = gls.make_comment(desc )+"\n"
        res.append(d)

    #print(type(json_str))
    return "\n".join(res)  # 将新的列表转换成字符串，每行以换行符连接起来



#制作shader文件
def write_shader(content,num):

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
        val = gls.clean_value(item["param_val"])
        desc = item["param_desc"]
        type_str = item["param_type"]

        gls.write_log("\nwrite_shader","name " + name + " val " + val +" type_str " + type_str)
        if gls.identify_float_type(val) != "float" and graph_nodes.is_key_in_line(name,"Color") and isNotTex:
            type_str = "Color"
            val = "("+val+")"
        line = "_" + name + '("' + desc + " " + name + '"'+ make_param(type_str,"",shader_dict).replace(";","")
        if type_str == "Texture":
            gls.write_log("\nwrite_shader","texture_val " + item["texture_val"])
            line += '"' 
            if( item["texture_val"] != ""):
                line += graph_nodes.replace_content(item["texture_val"],texture_type)
            else:
                line += "white"
            line += '" {' + '}'
        elif type_str != "Color":
            range_str = "Range(0," + val +")"
            line.replace(" Range(0,1)",range_str)
            line += " " + val
        res.append( gls.make_indentation(2)  + line )
        gls.write_log("\nwrite_shader",line)
        if desc == "":
            desc = item["param_group"]
        res.append( gls.make_indentation(2)  + gls.make_comment( desc)+"\n")
        
    #print(type(json_str))
    maincontainer = "Shader 'Sample/YourShaderName'\n{\n"
    prop_str = gls.make_indentation(1) + "Properties\n" + gls.make_indentation(1) +"{\n"
    prop_str += "\n".join(res) +"\n" + gls.make_indentation(1) +  "}\n"

    sub_str = "\n" +  gls.make_indentation(1) + "SubShader\n" +  gls.make_indentation(1) +"{"

    #subshader tags
    tag_str = unity_config.make_shader_tags(1,{"Queue":"Geometry","RenderType":"Opaque"},"")

    pass1_str = unity_config.make_subshader_pass(2,{"LightMode":"ForwardBase"},"/gen.cginc",True,True,True)

    sub = []
    for i in range(0,num):
        if(i == 0):
            pass2_str = unity_config.make_subshader_pass(2,{"LightMode":"ForwardBase"},"",False,False,False)
            s = sub_str + tag_str + pass1_str + pass2_str + gls.make_indentation(1) +  "}\n" 
        else:
            pass2_str = unity_config.make_subshader_pass(2,{"LightMode":"ForwardBase"},"",False,False,False)
            s = sub_str + tag_str + pass2_str  + gls.make_indentation(1) +  "}\n" 
        sub.append(s)
    maincontainer += prop_str + "".join(sub) +"\n}"
    return  maincontainer # 将新的列表转换成字符串，每行以换行符连接起来

#写UnityShader Cginc
subshader_num = 2 #int(input("Shader文件包含几个subshader:"))
#Shader文件包含几个subshader

result_cginc = write_cginc(content.split(ue_dict.split_signal)[0])
result_shader = write_shader(content.split(ue_dict.split_signal)[0],subshader_num)

#将转换后的内容写入输出文件output_cginc
with open(output_cginc, "w", encoding="utf-8") as f:
    f.write(result_cginc)

#将转换后的内容写入输出文件output_shader
with open(output_shader, "w", encoding="utf-8") as f:
    f.write(result_shader)

#输出Debug Log
with open(log_file, "w", encoding="utf-8") as f:
    f.write(log)