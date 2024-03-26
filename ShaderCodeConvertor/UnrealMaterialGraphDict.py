# 过滤参数集中的杂项
filter_dict_param = {
    "LinearInterpolate": "lerp",
    "CustomProperties Pin ": "",
    "Class=/Script/Engine.": "",
    "Class=/Script/UnrealEd.MaterialGraphNode": "",
    '"': "",
    "MaterialExpression": "",
    "End Object": "\n",
    "R=": "DefaultValue = "
}
object_start = '   Begin Object'
object_end = 'End Object'
# 过滤节点集的杂项
filter_dict_object = {
    "Begin Object Name=",
    "ParameterName",
    "Group",
    "Desc",
    "Texture=Texture2D",
    "SamplerType",
    "DefaultValue",
}

# 匹配节点自定义配置
match_object = {
    "NodeComment",
    "Text",
    "Begin Object Class",
    "CustomProperties"
    "MaterialFunction",
    object_start,
    object_end,
    'Begin Object Name="MaterialExpression',
    "CustomProperties",
    "MaterialExpression",
    "A=", "B=", "R="
}

param_start = '   Begin Object Name="MaterialExpression'  # "   Begin Object Name"
param_end = "   MaterialExpression=MaterialExpression"  # "   End Object"

match_param = {
    # "Begin Object Name=",
    "ParameterName",
    "Group",
    "Desc",
    "Texture=Texture2D",
    "SamplerType",
    "DefaultValue",
    "R=",
    param_start,
    param_end
}

split_signal = "split_signal"

hlsl_start = "    "
hlsl_end = ";"
# 只保留匹配的行
filter_shader = {
    "MaterialFloat2 Local",
    "MaterialFloat Local",
    "MaterialFloat4 Local",
    "MaterialFloat3 Local",
    "PixelMaterialInputs"
}
bool_dict = {
    "switch", "bool", "is", "if", "use"
}
