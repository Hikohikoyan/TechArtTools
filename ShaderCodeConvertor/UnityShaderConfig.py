
import GlobalSettings as gls
cginc = "gen.cginc"
shader = "gen.shader"

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

#定义生成的hlsl shaderlab的对应关系
material_to_shaderlab = {
    "MaterialFloat2" : "float2",
    "MaterialFloat": "half",
    "MaterialFloat4": "half4",
    "MaterialFloat3": "half3",
    "Parameters.TexCoords[0]":"fragmentContext.UV0",
    "Parameters.TexCoords[1]":"fragmentContext.UV1",
    "Local":"CustomParameter",
    "Material.VectorExpressions" :"CustomParameter_Vector",
    "Material.ScalarExpressions" :"CustomParameter_Scalar",
    "MaterialStoreTexCoordScale":"0;//TextureSampler using UVs,tex2D index(",
    #MaterialStoreTexCoordScale(Parameters, %s, %d) Parameters,*UVs, (int)TextureReferenceIndex
    "Material.Texture2D":"CustomParameter_tex2D",
    "ProcessMaterialColorTextureLookup(Texture2DSample":"tex2D",
    "PixelMaterialInputs":"fragmentContext",
    ".0000000":".0",
    "0000000;":"0;",
    "0000000)":"0)",
    "000000,":"0,"
}
#texture_type
texture_type ={
    "SAMPLERTYPE_Normal":"bump",
    "SAMPLERTYPE_LinearColor":"black",
}


#制作shader tags
def make_shader_tags(num,pack,end):
    tag = "\n" +  gls.make_indentation(num+1) + "Tags\n" +  gls.make_indentation(num+1) 
    tag += "{\n"
    t = ""
    if len(pack.items())<1:
        return "\n" + gls.make_indentation(num+1) + end + "\n"
    for key, value in pack.items():
        t +=  gls.make_indentation(num+2) +'"' + key + '" = ' + '"' + value + '"'+ "\n" 
    tag += t + gls.make_indentation(num+1) +"}\n" + gls.make_indentation(num+1) + end + "\n"
    return tag

#define pragma
def add_pragma(indent,config):
    t = ""
    for key, value in config.items():
        t +=  indent + "#pragma " + key + " " +value
    return t

pragma_0 = {
    "target":"3.0",
    "enable_d3d11_debug_symbols":"",
    "shader_feature":"_ DEBUG_VIEW_MODE",
    "multi_compile":"SHADING_QUALITY_HIGH SHADING_QUALITY_MEDIUM SHADING_QUALITY_LOW",
    "multi_compile_fwbase_br":"",
    "multi_compile_instancing":"",
    "shader_feature_local":"_ TEXTUREATLAS_ENABLE",
    "shader_feature_local":"_ TEXTUREDECODE_ENABLE",
    "shader_feature_local":"_ USE_PURE_COLOR",
    "shader_feature_local":"_ USE_LIGHTMAP",
    "shader_feature_local":"_ ISOLATE_IBL",
}
st_vert_in = "VertexInput"
st_vert_out = "VertexOutput"

st_frag_out = "FragOutput"
frag_context = "FragmentContext"

vert_in_pack = {
    "float4  Vertex":"POSITION",
    "half3  Normal":"NORMAL",
}

vert_out_pack = {
    "float4  Pos":"SV_POSITION",
    "float3  WorldPos":"ATTRIB0",
}

def make_struct(indent,name,pack):
    out = indent + "struct " + name
    out += indent +"{"
    idx = 0
    for key,val in pack.items():
        idx += 1
        out += indent + key + " : " + val
        if idx <= len(pack.items()) :
            out += ";"
    out += indent +"};" 
    return out

def make_func(indent,func_struct,func_name,func_input,content):
    func = indent + func_struct + " " + func_name + "(" + func_input +")"
    func += indent + "{"
    idx = 0
    for con in content.split(";"):
        idx += 1
        func += indent + gls.make_indentation(1) + con 
        if idx <= len(content.split(";"))-1 :
            func += ";"
    func += indent + "}"
    return func

#制作shader pass
def make_subshader_pass(num,tags,include,hasVert,hasFrag,hasFunc):
    pass_str = "\n" +  gls.make_indentation(num) + "Pass\n" +  gls.make_indentation(2) 
    content_indentation = "\n" + gls.make_indentation(num+1)
    #pass tags
    pass_str += "{" + make_shader_tags(num,tags,"") 
    pass_str +=  content_indentation + "CGPROGRAM" 
    pass_str +=  add_pragma(content_indentation,pragma_0) 


    vert_in = make_struct(content_indentation,st_vert_in,vert_in_pack)
    vert_out =  make_struct(content_indentation,st_vert_out ,vert_out_pack)
    vert_func = make_func(content_indentation,st_vert_out,"vert",st_vert_in + " input",
                          st_vert_out + " output = ("+st_vert_out +")0;output.Pos = vertexContext.ClipPosition;return output;")

    frag_content = "SETUP_CONSTANTS();" + frag_context +" fragmentContext = GetDefaultFragmentContext();ShadingContext shadingContext = GetDefaultShadingContext();return output;"
    frag_content += "ShadingContext shadingContext = GetDefaultShadingContext();" + "RETURN_FINAL_PIXEL_OUTPUT(fragmentContext, shadingContext);" 
    frag_func = make_func(content_indentation,st_frag_out,"frag",st_vert_out +" input",
                          frag_content)

    if hasVert:
        pass_str += vert_in
        pass_str += vert_out
        pass_str +=  content_indentation + "#pragma vertex vert" 
    if hasFrag:
        pass_str +=  content_indentation + "#pragma fragment frag"
    if include != "":
        pass_str +=  "\n" + content_indentation + '#include "' + include + '"\n'
    if hasFunc:
        pass_str += content_indentation +"///////////////////////////////////////////////////////////////////////////" 
        pass_str += vert_func
        pass_str += frag_func
        pass_str += content_indentation +"///////////////////////////////////////////////////////////////////////////" 
    pass_str += content_indentation + "ENDCG"
    pass_str +=  "\n" + gls.make_indentation(num) +"}" + "\n"
    return pass_str
