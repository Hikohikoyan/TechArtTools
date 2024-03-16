Shader 'Sample/YourShaderName'
{
    Properties
    {
        _Normal(" Normal", 2D) = "bump" {}
        // InputTextures

        _NormalIntensity(" NormalIntensity", Range(0,1)) =   1.0
        // MaterialSettings

        _RoughnessIntensity(" RoughnessIntensity", Range(0,1)) =   1.0
        // MaterialSettings

        _Tiling(" Tiling", Range(0,1)) =   1.0
        // MaterialSettings

        _CropY(" CropY", Range(0,1)) =   1.0
        // MaterialSettings

        _CropX(" CropX", Range(0,1)) =   1.0
        // MaterialSettings

        _Metallic(" Metallic", Range(0,1)) =   1.0
        // MaterialSettings

        _DisplacementOffset(" DisplacementOffset", Range(0,1)) =   2.0
        // MaterialSettings

        _Albedo(" Albedo", Range(0,1)) = 4  0.50,0.50,0.50,1.0
        // InputTextures

        _ColorOverlay(" ColorOverlay", Range(0,1)) =   1.0
        // MaterialSettings

        _RMD(" RMD", Range(0,1)) =   True
        // InputTextures

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
            struct VertexInput
            {
                float4  Vertex  :   POSITION;
                half3  Normal  :   NORMAL;
            };
            struct VertexOutput
            {
                float4  Pos    : SV_POSITION;
                float3  WorldPos   : ATTRIB0;
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
            };
            ///////////////////////////////////////////////////////////////////////////
            FragOutput frag(VertexOutput input)
            {
                SETUP_CONSTANTS();
                FragmentContext fragmentContext = GetDefaultFragmentContext();
                ShadingContext shadingContext = GetDefaultShadingContext();
                RETURN_FINAL_PIXEL_OUTPUT(fragmentContext, shadingContext);
            };
            ///////////////////////////////////////////////////////////////////////////
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
            ENDCG
        }
    }

}