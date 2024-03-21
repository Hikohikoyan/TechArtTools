import GlobalSettings as gls
import UnityShaderConfig as unity_dict
import json
import UnrealMaterialGraphFilter as ue_filter


def compare_shader_from_txt():
    file = "common_for_project.txt"
    # gls.check_input("请输入要比较的TXT文件", "file")
    if file == None:
        print("文件非法")
        return ""
    print("输入文件为 " + file + " 文件状态 " + str(gls.is_file(file)))
    a_start = gls.check_input("请输入原始内容块A 起始行号为 ", "num")
    a_end = gls.check_input("请输入原始内容块A 结束行号为 ", "num")

    a = gls.get_line_from_index(file, a_start, a_end)
    print("A包含行数" + str(len(a.split("\n"))))
    b_start = gls.check_input("请输入比较内容块B 起始行号为 ", "num")
    b_end = gls.check_input("请输入比较内容块B 结束行号为 ", "num")

    print("将会保留内容块B中与A不重复的部分 并合并")
    b = gls.get_line_from_index(file, b_start, b_end)
    print("B包含行数" + str(len(b.split("\n"))))
    compare_type = gls.check_input("要用哪种方式比较 [1] Shader Properties [2] Cginc Properties : ", "num")
    if int(compare_type) == 1:
        res = compare_shader_prop(a, b)
    else:
        res = compare_cginc_prop(a, b)
    out = "collection_for_unity_shader.txt"
    # gls.check_input("要将结果输出到哪个文件？ ", "file")
    file_original = "".join(gls.get_lines_from_file(out))
    str_out = "\nNewOutput:\n" + res + "\n" + gls.sign + gls.sign + "Old Txt\n" + file_original
    gls.write_file(out, str_out)
    return res


def clean_shader_prop(temp):
    t = []
    temp = temp.lstrip()
    for str_a in temp.split("\n"):
        str_a = gls.remove_inner_string(str_a, "(", ")")
        str_a = gls.remove_inner_string(str_a, "[", "]")

        str_a = str_a.lstrip().replace("(", "").replace(")", "")
        if str_a.startswith("//"):
            continue
        s = str_a.split("=")[0]
        # gls.write_log("\nclean_shader_prop s = ", s)
        t.append(s)
    return t


def clean_cginc_prop(temp):
    t = []
    for str_a in temp.split("\n"):
        str_a = str_a.lstrip()
        if str_a == "":
            continue
        if str_a.startswith("//"):
            continue
        if str_a.startswith("#"):
            continue
        str_a = str_a.split(";")[0]
        str_a = ""+str_a.replace(str_a.split("_")[0],"")
        t.append(str_a)
    return t


def search_in_arrs(a, b):
    diff = []
    set1 = set(a)
    set2 = set(b)
    same = list(set1.intersection(set2))
    gls.write_log("\nsearch_in_arrs\n AA = ", "".join(a))
    gls.write_log("\nsearch_in_arrs\n BB = ", "".join(b))
    diff = list(set1.difference(set2)) + list(set2.difference(set1))
    gls.write_log("\nsearch_in_arrs\n Same = ", json.dumps(same))
    gls.write_log("\nsearch_in_arrs\n Diff = ", json.dumps(diff))
    res = {"same": same, "diff": diff}
    return res


def compare_cginc_prop(a, b):
    print("开始比较两个内容块")
    temp_a = clean_cginc_prop("".join(a))
    temp_b = clean_cginc_prop("".join(b))
    temp = search_in_arrs(temp_a, temp_b)
    same = temp["same"]
    diff = temp["diff"]

    temp = "".join(find_strings(diff, b.split("\n")))
    res = a + "\n" + gls.sign + gls.sign + "New Parameter" + gls.sign + gls.sign + "\n" + temp
    gls.write_log("\ncompare_cginc_prop\n new = ", temp)
    return res


def find_strings(a, b):
    result = []
    for str_b in b:
        s_b = str_b.lstrip()
        if s_b == "":
            continue
        if s_b.startswith("//"):
            result.append(str_b + "\n")
            continue
        for str_a in a:
            if gls.clean_str(str_a) in gls.clean_str(s_b):
                result.append(str_b + "\n")
    return result


def compare_shader_prop(a, b):
    print("开始比较两个内容块")
    temp_a = clean_shader_prop("".join(a))
    temp_b = clean_shader_prop("".join(b))
    temp = search_in_arrs(temp_a, temp_b)
    same = temp["same"]
    diff = temp["diff"]
    b_new = "".join(find_strings(diff, b.split("\n")))
    res = a.replace(gls.sign, "\n")
    if len(b_new.split("\n")) > len(b.split("\n")) * 3:
        b_new = "///////////!Error Too Much Lines!///////////"
    res += "\n" + gls.sign + gls.sign + "New Parameters" + gls.sign + gls.sign + "\n" + b_new.replace(gls.sign, "\n")
    gls.write_log("\ncompare_shader_prop\n new = ", b_new)
    return res


print("当前运行模块为 : Unity Shader CompareHelper UnityShader参数比较模块 ")
compare_shader_from_txt()
