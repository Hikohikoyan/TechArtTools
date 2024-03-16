
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


#制作shader pass
def make_subshader_pass(num,tags,include,hasVert,hasFrag,hasFunc):
    pass_str = "\n" +  gls.make_indentation(num) + "Pass\n" +  gls.make_indentation(2) 
    content_indentation = "\n" + gls.make_indentation(num+1)
    func_indentation = "\n" + gls.make_indentation(num+2)
    #pass tags
    pass_str += "{" + make_shader_tags(num,tags,"") 
    pass_str +=  content_indentation + "CGPROGRAM" 
    pass_str +=  content_indentation + "#pragma target 3.0" 

    vert_in = content_indentation +"struct VertexInput" 
    vert_in += content_indentation +"{" 
    vert_in += func_indentation +"float4  Vertex  :   POSITION;"
    vert_in += func_indentation +"half3  Normal  :   NORMAL;" 
    vert_in += content_indentation +"};" 

    vert_out = content_indentation +"struct VertexOutput" 
    vert_out += content_indentation +"{" 
    vert_out += func_indentation +"float4  Pos    : SV_POSITION;"
    vert_out += func_indentation +"float3  WorldPos   : ATTRIB0;" 
    vert_out += content_indentation +"};" 

    vert_func = ""
    vert_func += content_indentation +"VertexOutput vert(VertexInput input)" 
    vert_func += content_indentation +"{" 
    vert_func += func_indentation +"VertexOutput output = (VertexOutput)0;"
    vert_func += func_indentation +"output.Pos = vertexContext.ClipPosition;"
    vert_func += func_indentation +"return output;" 
    vert_func += content_indentation +"};" 
    vert_func += content_indentation +"///////////////////////////////////////////////////////////////////////////"

    frag_func = ""
    frag_func += content_indentation +"FragOutput frag(VertexOutput input)" 
    frag_func += content_indentation +"{" 
    frag_func += func_indentation +"SETUP_CONSTANTS();"
    frag_func += func_indentation +"FragmentContext fragmentContext = GetDefaultFragmentContext();"
    frag_func += func_indentation +"ShadingContext shadingContext = GetDefaultShadingContext();"
    frag_func += func_indentation +"RETURN_FINAL_PIXEL_OUTPUT(fragmentContext, shadingContext);" 
    frag_func += content_indentation +"};" 
    frag_func += content_indentation +"///////////////////////////////////////////////////////////////////////////"

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
