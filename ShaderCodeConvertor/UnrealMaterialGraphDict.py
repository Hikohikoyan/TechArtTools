# 过滤参数集中的杂项
filter_dict_param = {
    "LinearInterpolate":"lerp",
    "CustomProperties Pin ":"",
    "Class=/Script/Engine." :"",
    "Class=/Script/UnrealEd.MaterialGraphNode":"",
    '"':"",
    "MaterialExpression":"",
    "End Object":"\n",
    "R=":"DefaultValue = "
}
object_start = '   Begin Object'
object_end = 'End Object'
# 过滤节点集的杂项
filter_dict_object = {
    "LinearInterpolate":"lerp",
    "CustomProperties Pin ":"",
    "Class=/Script/Engine." :"",
    "Class=/Script/UnrealEd.MaterialGraphNode":"",
    '"':"",
    "MaterialExpression":"",
    "End Object":"\n",
    "Begin Object ":"Object",
    "R=":"DefaultValue = ",
    "MaterialGraph":"",
}

#去掉对应的行
filter_object = {

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
    "A=","B=","R="
}


param_start = "ParameterName"
param_end = "   End Object"

match_param = {
    #"Begin Object Name=",
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

split_signal = "////"
