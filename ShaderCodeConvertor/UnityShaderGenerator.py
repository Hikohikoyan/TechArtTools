# 导入必要的库
import GlobalSettings as gls
import UnrealMaterialGraphDict as ue_dict
import UnityShaderConfig as unity_config
import UnrealMaterialGraphFilter as ue_filter


log_file = "Log.txt"
log = ""

# 定义hlsl shader code和cgsl的对应关系
cginc_dict = unity_config.cginc_dict
shader_dict = unity_config.shader_dict
#texture_type
texture_type =unity_config.texture_type


def make_param(t,n,config):
    #input type name
    res = ""
    res = ue_filter.replace_content(t,config) + " " + n
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
        if (ue_filter.is_key_in_line(info_type,"ParameterName")):
            pack["param_name"] = info_val
            if ue_filter.is_key_in_line(info_val,"Tex"):
                pack["isNotTexture"] = True

        # get ParameterGroup
        if (ue_filter.is_key_in_line(info_type,"Group")):
            pack["param_group"] = info_val
            if ue_filter.is_key_in_line(info_val,"贴图"):
                pack["isNotTexture"] = True

        # get ParameterDesc
        if (ue_filter.is_key_in_line(info_type,"Desc")):
            pack["param_desc"] = info_val

        # get ParameterValue
        if (ue_filter.is_key_in_line(info_type,"DefaultValue")):
            pack["param_val"] = gls.clean_value(info_val)

        # get TextureValue
        if (ue_filter.is_key_in_line(info_type,"SamplerType")):
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

def decode_hlsl(input):
    input.replace("\n","")
    lines = ue_filter.match_by_config(input,{"PixelMaterialInputs"})
    lines = lines.replace("PixelMaterialInputs.","")

    out = {
        'constant':[],
        'custom':[],
        'comment':[]
        }
    # vector = []
    # texture = []
    # scalar = []
    for line in lines.split(";"):
        l = line.split("=")
        if len(l) >1:
            if not ue_filter.is_key_in_line(l[1],"Local"):
                #存在自定义参数
                t = "fragmentContext." + l[0] +" = " + l[1]
                t = t.replace("\n","")
                out['constant'].append(t)

    for i in input.split(";"):
        i = i.lstrip()
        if i.startswith("PixelMaterialInputs"):
            t = "//" + i.replace("\n","")
            out['comment'].append(t)
        else:
            out['custom'].append(i.replace("\n",""))
    return out



#制作cginc参数 同步ue材质内设置
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
        t = make_param(item["param_type"],"_"+item["param_name"],cginc_dict).replace(";","") +";"
        desc = item["param_group"] + item["param_desc"]
        d = " "+ gls.make_comment(desc)
        res.append(t + d)
    #print(type(json_str))
    return res # 将新的列表转换成字符串，每行以换行符连接起来


#制作shader 参数 同步ue材质内设置
def write_shader_params(content,num):

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
        if gls.identify_float_type(val) != "float" and ue_filter.is_key_in_line(name,"Color") and isNotTex:
            type_str = "Color"
            val = "("+val+")"
        line = "_" + name + '("' + desc + "" + name + '"'+ make_param(type_str,"",shader_dict).replace(";","")
        if type_str == "Texture":
            gls.write_log("\nwrite_shader","texture_val " + item["texture_val"])
            line += '"' 
            if( item["texture_val"] != ""):
                line += ue_filter.replace_content(item["texture_val"],texture_type)
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
    return  res # 将新的列表转换成字符串，每行以换行符连接起来




def gen_shader_file(input,output):
    with open(input, "r", encoding="utf-8") as f:
        content = f.read()

    #写UnityShader Cginc
    subshader_num = 2 #int(input("Shader文件包含几个subshader:"))
    res = write_shader_params(content.split(ue_dict.split_signal)[0],subshader_num)

    maincontainer = "Shader 'Sample/YourShaderName'\n{\n"
    prop_str = gls.make_indentation(1) + "Properties\n" + gls.make_indentation(1) +"{\n"
    prop_str += "\n".join(res) +"\n" + gls.make_indentation(1) +  "}\n"

    sub_str = "\n" +  gls.make_indentation(1) + "SubShader\n" +  gls.make_indentation(1) +"{"

    #subshader tags
    tag_str = unity_config.make_shader_tags(1,{"Queue":"Geometry","RenderType":"Opaque"},"")
    pass1_str = unity_config.make_subshader_pass(2,{"LightMode":"ForwardBase"},"/gen.cginc",True,True,True)

    sub = []
    for i in range(0,subshader_num):
        if(i == 0):
            pass2_str = unity_config.make_subshader_pass(2,{"LightMode":"ForwardBase"},"",False,False,False)
            s = sub_str + tag_str + pass1_str + pass2_str + gls.make_indentation(1) +  "}\n" 
        else:
            pass2_str = unity_config.make_subshader_pass(2,{"LightMode":"ForwardBase"},"",False,False,False)
            s = sub_str + tag_str + pass2_str  + gls.make_indentation(1) +  "}\n" 
        sub.append(s)
    maincontainer += prop_str + "".join(sub) +"\n}"

    #将转换后的内容写入输出文件output_shader
    with open(output, "w", encoding="utf-8") as f:
        f.write(maincontainer)
    return 

def gen_cginc_file(input,output):
    with open(input, "r", encoding="utf-8") as f:
        content = f.read()
    res = write_cginc(content.split(ue_dict.split_signal)[0])
    res = "\n".join(res) +"\n"
    out = decode_hlsl(content.split(ue_dict.split_signal)[1])
    func_contents = ""
    indent = "\n"+gls.make_indentation(0)
    for item in out['constant']:
        func_contents +=  item + ";"
    for item in out['custom']: 
        func_contents += item + ";"
               
    for item in out['comment']: 
        func_contents += item + ";"
    func_contents = ue_filter.replace_content(func_contents,unity_config.material_to_shaderlab)
    res += unity_config.make_func(indent,"void","SetupFragmentAndShadingContext",
                           "inout FragmentContext fragmentContext, inout ShadingContext shadingContext, in VertexOutput input",
                           func_contents)
    #将转换后的内容写入输出文件output_cginc
    with open(output, "w", encoding="utf-8") as f:
        f.write(res)


#Shader文件包含几个subshader

# 定义输入和输出文件路径
input_file = "collection_for_unity_shader.txt" 
#input("请输入For Unity的TXT 路径：")
output_cginc = unity_config.cginc
output_shader = unity_config.shader

# 读取输入文件内容
#在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
# with open(input_file, "r", encoding="utf-8") as f:
#     content = f.read()

#main
result_cginc = gen_cginc_file(input_file,output_cginc)
result_shader = gen_shader_file(input_file,output_shader)


#输出Debug Log
with open(log_file, "w", encoding="utf-8") as f:
    f.write(log)