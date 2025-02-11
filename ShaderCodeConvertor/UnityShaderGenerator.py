# 导入必要的库
import json

import GlobalSettings as gls
import UnrealMaterialGraphDict as ue_dict
import UnityShaderConfig as unity_config
import UnrealMaterialGraphFilter as ue_filter

path = "ShaderCodeConvertor\\"
log_file = "Log.txt"
log = ""

# 定义hlsl shader code和cgsl的对应关系
cginc_dict = unity_config.cginc_dict
shader_dict = unity_config.shader_dict
# texture_type
texture_type = unity_config.texture_type


def make_param(t, n, config):
    # input type name
    res = ""
    res = ue_filter.replace_content(t, config) + " " + n
    return res


# 解析数据包
def decode_input(item):
    pack = {
        "param_name": "",
        "param_type": "",
        "param_group": "",
        "param_desc": "",
        "param_val": "",
        "isTexture": False,
        "isColor": False,
        "isBoolean": False,
        "texture_val": "",
        "isParam": False
    }
    item = item.replace(",{", "").replace("{;", "")
    for info in item.split(";"):
        if len(info.split(":")) < 2:
            continue
        info_type = "".join(info.split(":")[0]).replace("}", "").replace("{", "")
        info_val = info.replace(info_type, "").replace(":", "").replace('"', "")
        # #debug
        if (info_type.lstrip().startswith("Name")):
            if ue_filter.is_key_in_line(info_val, "Parameter_"):
                pack["isParam"] = True
                info_val = info_val.split("_")[0].replace("Parameter", "")
                info_val = ue_filter.replace_content(info_val, unity_config.match_type)
                pack["param_type"] = info_val
        # get ParameterName
        if (ue_filter.is_key_in_line(info_type, "ParameterName")):
            pack["param_name"] = info_val
            if ue_filter.is_key_in_line(info_val, "Tex"):
                pack["isTexture"] = True
                pack["isParam"] = True
            if ue_filter.is_key_in_line(info_val, "Use"):
                pack["isBoolean"] = True
                pack["isParam"] = True

        # get ParameterGroup
        if (ue_filter.is_key_in_line(info_type, "Group")):
            pack["param_group"] = info_val

        # get ParameterDesc
        if (ue_filter.is_key_in_line(info_type, "Desc")):
            pack["param_desc"] = info_val

        # get ParameterValue
        if (ue_filter.is_key_in_line(info_type, "DefaultValue")):
            pack["param_val"] = gls.clean_value(info_val)
        if ue_filter.is_key_in_line(info_val, "True") or ue_filter.is_key_in_line(info_val, "False"):
            pack["isBoolean"] = True
        # get TextureValue
        if (ue_filter.is_key_in_line(info_type, "SamplerType")):
            pack["isTexture"] = True
            pack["isParam"] = True
            pack["texture_val"] = info_val
        # debug
        # gls.write_log("" ,"param_val:" +pack["param_val"])
        # gls.write_log("" ,"param_name:" +pack["param_name"])

    if pack["isTexture"]:
        # 贴图参数
        pack["param_type"] = "Texture"
    elif pack["isBoolean"]:
        pack["param_type"] = "boolean"
    else:
        if pack["param_type"] == "":
            pack["param_type"] = gls.identify_float_type(pack["param_val"])

    return pack


def decode_hlsl(input):
    input.replace("\n", "")
    lines = ue_filter.match_by_config(input, {"PixelMaterialInputs"})
    lines = lines.replace("PixelMaterialInputs.", "")

    out = {
        'constant': [],
        'custom': [],
        'comment': []
    }
    # vector = []
    # texture = []
    # scalar = []
    for line in lines.split(";"):
        l = line.split("=")
        if len(l) > 1:
            if not ue_filter.is_key_in_line(l[1], "Local"):
                # 存在自定义参数
                t = "fragmentContext." + l[0] + " = " + l[1]
                t = t.replace("\n", "")
                out['constant'].append(t)

    for i in input.split(";"):
        i = i.lstrip()
        if i.startswith("PixelMaterialInputs"):
            t = "//" + i.replace("\n", "")
            out['comment'].append(t)
        else:
            out['custom'].append(i.replace("\n", ""))
    return out


# 制作cginc参数 同步ue材质内设置
def write_cginc(content):
    # gls.write_log("\nwrite_cginc\n", content)
    params = content.split(ue_dict.split_signal)[0].replace("\n", "").replace(" ", "").split("}")
    res = []
    import_par = dict()
    for info in params:
        item = decode_input(info)
        isNotTex = not item["isTexture"]
        checkstatus = not item["isParam"]
        # isNotTex and item["param_val"] == ""
        # checkstatus = checkstatus or item["param_name"] == ""
        if item == None or checkstatus:
            continue
        t = make_param(item["param_type"], "_" + item["param_name"], cginc_dict).replace(";", "") + ";"
        if item["isBoolean"]:
            t = "#ifdef " + item["param_name"].upper() + "\n#endif "
        desc = item["param_group"] + item["param_desc"]
        d = " " + gls.make_comment(desc)
        import_par.setdefault(item["param_name"],
                              ue_filter.replace_content(item["param_type"],
                                                        unity_config.mat_shaderlab_param))
        res.append(t + d)

    hlsl = decode_hlsl(content.split(ue_dict.split_signal)[1])
    local = dict()
    for item in hlsl['custom']:
        par = item.split("=")[0].split(" ")
        if len(par) > 2:
            local.setdefault(par[1], ue_filter.replace_content(par[0], unity_config.mat_shaderlab_param))
    return res  # 将新的列表转换成字符串，每行以换行符连接起来


# 制作shader 参数 同步ue材质内设置
def write_shader_params(content, num):
    params = content.replace("\n", "").replace(" ", "").split("}")
    res = []
    for info in params:
        item = decode_input(info)
        isNotTex = not item["isTexture"]
        checkstatus = not item["isParam"]
        # isNotTex and item["param_val"] == ""
        # checkstatus = checkstatus or item["param_type"] == ""
        gls.write_log("write_shader_params ", json.dumps(item))
        if item == None or checkstatus:
            continue
        name = item["param_name"]
        val = gls.clean_value(item["param_val"])
        desc = item["param_desc"]
        type_str = item["param_type"]

        # gls.write_log("\nwrite_shader","name " + name + " val " + val +" type_str " + type_str)
        if gls.identify_float_type(val) != "float" and ue_filter.is_key_in_line(name, "Color") and isNotTex:
            type_str = "Color"
            val = "(" + val + ")"
        line = "_" + name + '("' + desc + "" + name + '"' + make_param(type_str, "", shader_dict).replace(";", "")
        if item["isTexture"]:
            # gls.write_log("\nwrite_shader","texture_val " + item["texture_val"])
            line += '"'
            if (item["texture_val"] != ""):
                line += ue_filter.replace_content(item["texture_val"], texture_type)
            else:
                line += "white"
            line += '" {' + '}'
        elif type_str != "Color":
            range_str = "Range(0," + val + ")"
            line.replace(" Range(0,1)", range_str)
            line += " " + val
        if item["isBoolean"]:
            line = "[Toggle(" + name.upper() + ")]" + line.replace("True", "1 //True").replace("False", "0 //False")
        res.append(gls.make_indentation(2) + line)
        # gls.write_log("\nwrite_shader",line)
        if desc == "":
            desc = item["param_group"]
        res.append(gls.make_indentation(2) + gls.make_comment(desc) + "\n")
    return res  # 将新的列表转换成字符串，每行以换行符连接起来


def gen_shader_file(input, output):
    content = gls.read_file(input)
    # 写UnityShader
    subshader_num = gls.check_input("Shader文件包含几个subshader:", "num")
    subshader_num = int(subshader_num)
    res = write_shader_params(content.split(ue_dict.split_signal)[0], subshader_num)
    maincontainer = "Shader 'Sample/YourShaderName'\n{\n"
    prop_str = gls.make_indentation(1) + "Properties\n" + gls.make_indentation(1) + "{\n"
    prop_str += "\n".join(res) + "\n" + gls.make_indentation(1) + "}\n"

    sub_str = "\n" + gls.make_indentation(1) + "SubShader\n" + gls.make_indentation(1) + "{"

    # subshader tags
    tag_str = unity_config.make_shader_tags(1, {"Queue": "Geometry", "RenderType": "Opaque"}, "")
    pass1_str = unity_config.make_subshader_pass(2, {"LightMode": "ForwardBase"}, "/gen.cginc", True, True, True)

    sub = []
    for i in range(0, subshader_num):
        if (i == 0):
            pass2_str = unity_config.make_subshader_pass(2, {"LightMode": "ForwardBase"}, "", False, False, False)
            s = sub_str + tag_str + pass1_str + pass2_str + gls.make_indentation(1) + "}\n"
        else:
            pass2_str = unity_config.make_subshader_pass(2, {"LightMode": "ForwardBase"}, "", False, False, False)
            s = sub_str + tag_str + pass2_str + gls.make_indentation(1) + "}\n"
        sub.append(s)
    maincontainer += prop_str + "".join(sub) + "\n}"

    # 将转换后的内容写入输出文件output_shader
    gls.write_file(output, maincontainer)
    return


def gen_cginc_file(input, output):
    content = gls.read_file(input)
    res = write_cginc(content)
    res = "\n".join(res) + "\n"
    out = decode_hlsl(content.split(ue_dict.split_signal)[1])
    func_contents = ""
    indent = "\n" + gls.make_indentation(0)
    for item in out['constant']:
        func_contents += item + ";"
    for item in out['custom']:
        func_contents += item + ";"
    for item in out['comment']:
        func_contents += item + ";"
    func_contents = ue_filter.replace_content(func_contents, unity_config.material_to_shaderlab)
    res += unity_config.make_func(indent, "void", "SetupFragmentAndShadingContext",
                                  "inout FragmentContext fragmentContext, inout ShadingContext shadingContext, in VertexOutput input",
                                  func_contents)
    # 将转换后的内容写入输出文件output_cginc
    gls.write_file(output, res)


# Shader文件包含几个subshader
def main():
    if not gls.check_status("需要生成UnityShader吗？(需要先执行 前置依赖函数UnrealMaterialGraphFilter::Main)",
                            "Unity ShaderGenerator::Main"):
        return False
    if not ue_filter.main():
        return False
    # 定义输入和输出文件路径
    print("当前运行模块为 : Unity Shader Generator UnityShader/Cginc生成模块 ")
    input_file = "output.txt"
    # gls.check_input("输入已过滤好的文件路径 例如 collection_for_unity_shader.txt", "file")

    # "collection_for_unity_shader.txt"

    output_cginc = unity_config.cginc
    output_shader = unity_config.shader

    # 读取输入文件内容
    # 在打开文件时，使用encoding参数指定文件编码格式为gbk（根据实际情况修改），在写入文件时，使用encoding参数指定文件编码格式为utf-8（或其他你需要的编码格式）。这样就可以避免中文字符导致的编码错误了
    # with open(input_file, "r", encoding="utf-8") as f:
    #     content = f.read()

    # main
    gen_cginc_file(input_file, output_cginc)
    print("输出Cginc文件在 " + unity_config.cginc)
    gen_shader_file(input_file, output_shader)
    print("输出shader文件在 " + unity_config.shader)
    return True


print("当前运行模块为 : Unity Shader Generator UnityShader/Cginc生成模块 ")
main()
