sampler2D _EnableTextureCompression; // Decode
sampler2D _EnableTextureCompression; // Decode
sampler2D _EnableTextureCompression; // Decode
sampler2D _NormalTex; // 
sampler2D _AlphaMask; // 
sampler2D _AO; // 
sampler2D _BaseColorTex; // 
half _Color; // 
half _Metallic; // 
sampler2D _MetallicTex; // 
sampler2D _RoughnessTex; // 
sampler2D _EnableTextureCompression; // Decode
sampler2D _EnableTextureCompression; // Decode
sampler2D _EnableTextureCompression; // Decode
sampler2D _EmissiveTex; // 
sampler2D _EnableTextureCompression; // Decode
half _Roughness_IBL; // 大理石高光
half _Specular_IBL; // 大理石高光

void SetupFragmentAndShadingContext(inout FragmentContext fragmentContext, inout ShadingContext shadingContext, in VertexOutput input)
{
    fragmentContext.Normal  =  half3(0.00,0.00,1.00);
    fragmentContext.Opacity  =  1.00;
    fragmentContext.OpacityMask  =  1.00;
    fragmentContext.BaseColor  =  half3(0.00,0.00,0.00);
    fragmentContext.Metallic  =  0.00;
    fragmentContext.Specular  =  0.50;
    fragmentContext.Roughness  =  0.50;
    fragmentContext.Anisotropy  =  0.00;
    fragmentContext.Tangent  =  half3(1.00,0.00,0.00);
    fragmentContext.Subsurface  =  0;
    fragmentContext.AmbientOcclusion  =  1.00;
    fragmentContext.Refraction  =  0;
    fragmentContext.PixelDepthOffset  =  0.00;
    fragmentContext.ShadingModel  =  0;
    half3 CustomParameter0 = lerp(half3(0.00,0.00,0.00),CustomParameter_Vector[1].rgb,half(CustomParameter_Scalar[0].x));
    ;
    //fragmentContext.Normal = half3(0.00,0.00,1.00);
    //fragmentContext.EmissiveColor = CustomParameter0;
    //fragmentContext.Opacity = 1.00;
    //fragmentContext.OpacityMask = 1.00;
    //fragmentContext.BaseColor = half3(0.00,0.00,0.00);
    //fragmentContext.Metallic = 0.00;
    //fragmentContext.Specular = 0.50;
    //fragmentContext.Roughness = 0.50;
    //fragmentContext.Anisotropy = 0.00;
    //fragmentContext.Tangent = half3(1.00,0.00,0.00);
    //fragmentContext.Subsurface = 0;
    //fragmentContext.AmbientOcclusion = 1.00;
    //fragmentContext.Refraction = 0;
    //fragmentContext.PixelDepthOffset = 0.00;
    //fragmentContext.ShadingModel = 0;
    
}