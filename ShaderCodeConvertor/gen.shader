Shader 'Sample/YourShaderName'
{
    Properties
    {
        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _NormalTex("NormalTex", 2D) = "bump" {}
        // 

        _AlphaMask("AlphaMask", 2D) = "black" {}
        // 

        _AO("AO", 2D) = "black" {}
        // 

        _BaseColorTex("BaseColorTex", 2D) = "white" {}
        // 

        _Color("Color", Range(0,1)) =   1.0
        // 

        _Metallic("Metallic", Range(0,1)) =   1.0
        // 

        _MetallicTex("MetallicTex", 2D) = "black" {}
        // 

        _RoughnessTex("RoughnessTex", 2D) = "black" {}
        // 

        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _EmissiveTex("EmissiveTex", 2D) = "black" {}
        // 

        _EnableTextureCompression("EnableTextureCompression", 2D) = "white" {}
        // Decode

        _Roughness_IBL("Roughness_IBL", Range(0,1)) =   0.20
        // 大理石高光

        _Specular_IBL("Specular_IBL", Range(0,1)) =   0.0150
        // 大理石高光

    }

    SubShader
    {
        Tags
        {
            "Queue" = "Geometry"
            "RenderType" = "Opaque"
        }
        

        Pass
        {
            Tags
            {
                "LightMode" = "ForwardBase"
            }
            

            CGPROGRAM
            #pragma target 3.0
            #pragma enable_d3d11_debug_symbols 
            #pragma shader_feature _ DEBUG_VIEW_MODE
            #pragma multi_compile SHADING_QUALITY_HIGH SHADING_QUALITY_MEDIUM SHADING_QUALITY_LOW
            #pragma multi_compile_fwbase_br 
            #pragma multi_compile_instancing 
            #pragma shader_feature_local _ ISOLATE_IBL
            struct VertexInput
            {
            float4  Vertex : POSITION;
            half3  Normal : NORMAL;
            };
            struct VertexOutput
            {
            float4  Pos : SV_POSITION;
            float3  WorldPos : ATTRIB0;
            };
            #pragma vertex vert
            #pragma fragment frag

            #include "/gen.cginc"

            ///////////////////////////////////////////////////////////////////////////
            VertexOutput vert(VertexInput input)
            {
                VertexOutput output = (VertexOutput)0;
                output.Pos = vertexContext.ClipPosition;
                return output;
                
            }
            FragOutput frag(VertexOutput input)
            {
                SETUP_CONSTANTS();
                FragmentContext fragmentContext = GetDefaultFragmentContext();
                ShadingContext shadingContext = GetDefaultShadingContext();
                return output;
                ShadingContext shadingContext = GetDefaultShadingContext();
                RETURN_FINAL_PIXEL_OUTPUT(fragmentContext, shadingContext);
                
            }
            ///////////////////////////////////////////////////////////////////////////
            ENDCG
        }

        Pass
        {
            Tags
            {
                "LightMode" = "ForwardBase"
            }
            

            CGPROGRAM
            #pragma target 3.0
            #pragma enable_d3d11_debug_symbols 
            #pragma shader_feature _ DEBUG_VIEW_MODE
            #pragma multi_compile SHADING_QUALITY_HIGH SHADING_QUALITY_MEDIUM SHADING_QUALITY_LOW
            #pragma multi_compile_fwbase_br 
            #pragma multi_compile_instancing 
            #pragma shader_feature_local _ ISOLATE_IBL
            ENDCG
        }
    }

    SubShader
    {
        Tags
        {
            "Queue" = "Geometry"
            "RenderType" = "Opaque"
        }
        

        Pass
        {
            Tags
            {
                "LightMode" = "ForwardBase"
            }
            

            CGPROGRAM
            #pragma target 3.0
            #pragma enable_d3d11_debug_symbols 
            #pragma shader_feature _ DEBUG_VIEW_MODE
            #pragma multi_compile SHADING_QUALITY_HIGH SHADING_QUALITY_MEDIUM SHADING_QUALITY_LOW
            #pragma multi_compile_fwbase_br 
            #pragma multi_compile_instancing 
            #pragma shader_feature_local _ ISOLATE_IBL
            ENDCG
        }
    }

}