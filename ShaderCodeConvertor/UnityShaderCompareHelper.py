import GlobalSettings as gls
import UnityShaderConfig as unity_dict
import json
import UnrealMaterialGraphFilter as ue_filter


def compare_shader_from_txt():
    file = gls.check_input("请输入要比较的TXT文件", "file")
    if file == None:
        print("文件非法")
        return ""
    print("输入文件为 " + file + " 文件状态 " + str(gls.is_file(file)))
    a_start = gls.check_input("请输入原始内容块A 起始行号为 ", "num")
    a_end = gls.check_input("请输入原始内容块A 结束行号为 ", "num")

    a = gls.get_line_from_index(file, a_start, a_end)

    b_start = gls.check_input("请输入比较内容块B 起始行号为 ", "num")
    b_end = gls.check_input("请输入比较内容块B 结束行号为 ", "num")

    print("将会保留内容块B中与A不重复的部分 并合并")
    b = gls.get_line_from_index(file, b_start, b_end)

    compare_type = gls.check_input("要用哪种方式比较 [1] Shader Properties [2] Cginc Properties : ", "num")
    if int(compare_type) == 1:
        res = compare_shader_prop(a, b)
    else:
        res = compare_cginc_prop(a, b)
    out = gls.check_input("要将结果输出到哪个文件？ ", "file")
    file_original = gls.read_file(out)
    file_original = file_original.replace(gls.sign, "\n")
    str_out = "\nNewOutput:\n" + res + "\n" + gls.sign + gls.sign + "Old Txt\n" + file_original
    gls.write_file(out, str_out)
    return res


def clean_shader_prop(temp):
    t = []
    temp = temp.lstrip()
    for str_a in temp.split(gls.sign):
        str_a = gls.remove_inner_string(str_a, "(", ")")
        str_a = gls.remove_inner_string(str_a, "[", "]")

        str_a = str_a.lstrip().replace("(", "").replace(")", "")
        if str_a.startswith("//"):
            continue
        s = str_a.split("=")[0]
        t.append(s)
    return t


def clean_cginc_prop(temp):
    t = []
    temp = temp.lstrip()
    for str_a in temp.split(gls.sign):
        if str_a == "":
            continue
        if str_a.startswith("//"):
            continue
        if str_a.startswith("#"):
            t.append(str_a)
            continue
        if str_a.count("//") > 0:
            str_a = str_a.split("//")[0]
        str_a = str_a.replace(str_a.split(" ")[0], "")
        t.append(str_a)
    return t


def search_in_arrs(a, b):
    same = []
    diff = []
    # gls.write_log("\nsearch_in_arrs\n AA = ", "".join(a))
    # gls.write_log("\nsearch_in_arrs\n BB = ", "".join(b))

    for key in b:
        is_same = False
        key = gls.clean_str(key)

        for key_a in a:
            key_a = gls.clean_str(key_a)
            if key == key_a:
                if key in same:
                    is_same = True
                    continue
                same.append(key)
                is_same = True
        if not is_same:
            diff.append(key)
        # gls.write_log("\nsearch_in_arrs\n key = ", key)
        # gls.write_log("\nsearch_in_arrs\n is_same = ", str(is_same))
    res = {"same": same, "diff": diff}
    return res


def compare_cginc_prop(a, b):
    print("开始比较两个内容块")
    temp_a = clean_cginc_prop(a)
    temp_b = clean_cginc_prop(b)
    temp = search_in_arrs(temp_a, temp_b)
    same = temp["same"]
    diff = temp["diff"]
    gls.write_log("\ncompare_cginc_prop\n Same = ", "".join(same))
    gls.write_log("\ncompare_cginc_prop\n Diff = ", "".join(diff))
    res = ""
    for line in b.split(gls.sign):
        tl = line.replace('"', "").lstrip()
        if tl == "":
            continue
        if tl.startswith("//"):
            res += line + "\n"
            continue
        is_same = False
        for s in same:
            if is_same:
                break
            is_same = ue_filter.is_key_in_line(tl, s)
        if is_same:
            continue
        res += line + "\n"

    res = a.replace(gls.sign,
                    "\n") + "\n\n" + gls.sign + gls.sign + "New Parameter" + gls.sign + gls.sign + "\n" + res.replace(
        gls.sign, "\n//////New Parameters End/////")
    #gls.write_log("\ncompare_cginc_prop\n new = ", res)
    return res


def compare_shader_prop(a, b):
    print("开始比较两个内容块")
    temp_a = clean_shader_prop(a)
    temp_b = clean_shader_prop(b)

    same = search_in_arrs(temp_a, temp_b)["same"]
    diff = search_in_arrs(temp_a, temp_b)["diff"]
    gls.write_log("\ncompare_shader_prop\n Same = ", "".join(same))
    gls.write_log("\ncompare_shader_prop\n Diff = ", "".join(diff))
    b_new = ""
    for line in b.split(gls.sign):
        tl = line.replace('"', "").lstrip()
        if tl == "":
            continue
        if tl.startswith("//"):
            b_new += line + "\n"
            continue
        is_same = False
        for s in same:
            if is_same:
                break
            is_same = ue_filter.is_key_in_line(tl, s)
        if is_same:
            continue
        b_new += line + "\n"
    res = a.replace(gls.sign, "\n")
    res += "\n\n" + gls.sign + gls.sign + "New Parameters" + gls.sign + gls.sign + "\n" + b_new.replace(gls.sign, "\n")
    gls.write_log("\ncompare_shader_prop\n new = ", res)
    return res


print("当前运行模块为 : Unity Shader CompareHelper UnityShader参数比较模块 ")
compare_shader_from_txt()
