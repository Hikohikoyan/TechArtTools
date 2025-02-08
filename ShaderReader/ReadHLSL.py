import re
import ShaderCalculationDict as shader_dict
def read_file(input):
    res = ""
    with open(input, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        res += line + "@"
    res = res.replace("@", "")
    #res = '\n'.join(lines)
    return res
# 示例 HLSL 代码

path = "calculation.hlsl " #"H:/NN/helloworld/v2/temp.hlsl"
hlsl_code = read_file(path)

# 提取定义
cbuffers = re.findall(shader_dict.cbuffer_pattern, hlsl_code, re.MULTILINE | re.DOTALL)
samplers = re.findall(shader_dict.sampler_pattern, hlsl_code, re.MULTILINE)
structs = re.findall(shader_dict.struct_pattern, hlsl_code, re.MULTILINE | re.DOTALL)

# 将所有定义存储在一个集合中
definitions = set(cbuffers + samplers + structs)

# 提取计算
#calculations = hlsl_code.split(";")#re.findall(calculation_pattern, hlsl_code, re.MULTILINE)


# 提取函数
#functions = re.findall(shader_dict.function_pattern, hlsl_code, re.MULTILINE)

# 写入 header.hlsl
#with open('header.hlsl', 'w') as header_file:
#    header_file.write('\n'.join(definitions) + '\n')

# 写入 calculation.hlsl，避免重复定义
#with open('output.hlsl', 'w') as calculation_file:
    #for calc in hlsl_code:
        # 检查计算中是否包含定义
        #if not any(definition in calc for definition in definitions):
            #calculation_file.write(calc + '\n')

def GetBranchs(input):
    t = input.split("\n")
    branchs = []
    temp_line = ""

    count = 0
    sub_count = 0
    cur_line = 0
    start_line_idx = 0
    end_line_idx = 0
    result = ""
    bStartBlock = False
    bEndBlock = False

    for line in t:

        cur_line += 1
        #main branch
        if line.lstrip().startswith("if"):
            if bStartBlock:
                #是子分支
                sub_count += 1
            else:
                sub_count = 0

            start_line_idx = cur_line +2
            branchs.append(start_line_idx)
            count = len(branchs)
            bStartBlock = True
            bEndBlock = False
            temp_line += "\n //Branch-" + str(count) + " Begin \n"


        if line.replace("\n","").replace(" ","").startswith( "}") :
            #branchs.append(str("// \n start :" + start_line_idx  + "\n //end: " + end_line_idx + "\n"))
            if sub_count>0:
                temp_line += "\n //Branch-" + str(count) + " End" + "\n"
                count -= 1
                sub_count -= 1
            else:
                temp_line += "\n //Branch-" + str(count) + " End" + "\n"
            bEndBlock = True
            bStartBlock = False
        temp_line += line + "\n"
    return temp_line

def Replace(input):
    t = input.split("\n")
    temp = ""
    for line in t:
        #line = shader_dict.replace_function_call("mad",line,"slot1 * slot2 + slot3")
        line = shader_dict.replace_function_call("rcp",line,"1 / slot1","")
        line = shader_dict.replace_function_call("rsqrt", line, "1 / sqrt(slot1)"," Normalize ?")
        if line.count("float2") > 0:
            temp += "// UV?" + "\n"
        if line.count("Sample") > 0:
            temp += " // Texture?" + "\n"
        if line.count("Gather") > 0:
            temp += " // Texture2DArray、TextureCube ?" + "\n"
        if line.count("Load") > 0:
            temp += " // Texture mipmap?" + "\n"
        temp += line + "\n"
    return temp

with open('output.hlsl', 'w') as header_file:
   header_file.write(Replace(GetBranchs(hlsl_code)))

