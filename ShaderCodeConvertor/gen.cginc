sampler2D Normal;  // InputTextures
half NormalIntensity;  // MaterialSettings
half RoughnessIntensity;  // MaterialSettings
half Tiling;  // MaterialSettings
half CropY;  // MaterialSettings
half CropX;  // MaterialSettings
half Metallic;  // MaterialSettings
half DisplacementOffset;  // MaterialSettings
half4 Albedo;  // InputTextures
half ColorOverlay;  // MaterialSettings
half RMD;  // InputTextures

void SetupFragmentAndShadingContext(inout FragmentContext fragmentContext, inout ShadingContext shadingContext, in VertexOutput input)
{
    fragmentContext.Opacity  =  1.00;
    fragmentContext.OpacityMask  =  1.00;
    fragmentContext.Specular  =  0.50;
    fragmentContext.Anisotropy  =  0.00;
    fragmentContext.Tangent  =  half3(1.00,0.00,0.00);
    fragmentContext.Subsurface  =  0;
    fragmentContext.AmbientOcclusion  =  1.00;
    fragmentContext.Refraction  =  0;
    fragmentContext.PixelDepthOffset  =  0.00;
    fragmentContext.ShadingModel  =  1;
    float2 CustomParameter0 = (fragmentContext.UV0.xy * CustomParameter_Scalar[0].y);
    float2 CustomParameter1 = (CustomParameter0 + CustomParameter_Vector[3].rg);
    half CustomParameter2 = 0;
    //TextureSampler using UVs,tex2D index((Parameters, CustomParameter1, 0);
    half4 CustomParameter3 = UnpackNormalMap(Texture2DSample(CustomParameter_tex2D_0, GetMaterialSharedSampler(CustomParameter_tex2D_0Sampler,View.MaterialTextureBilinearWrapedSampler),CustomParameter1));
    half CustomParameter4 = MaterialStoreTexSample(Parameters, CustomParameter3, 0);
    half3 CustomParameter5 = (CustomParameter_Vector[4].rgb * CustomParameter3.rgb);
    half3 CustomParameter6 = (CustomParameter5 + CustomParameter3.rgb);
    half3 CustomParameter7 = lerp(half3(0.00,0.00,0.00),CustomParameter_Vector[5].rgb,half(CustomParameter_Scalar[1].x));
    half CustomParameter8 = 0;
    //TextureSampler using UVs,tex2D index((Parameters, CustomParameter1, 1);
    half4 CustomParameter9 = tex2D(CustomParameter_tex2D_1, GetMaterialSharedSampler(CustomParameter_tex2D_1Sampler,View.MaterialTextureBilinearWrapedSampler),CustomParameter1));
    half CustomParameter10 = MaterialStoreTexSample(Parameters, CustomParameter9, 1);
    half3 CustomParameter11 = (1.00 - CustomParameter9.rgb);
    half3 CustomParameter12 = (CustomParameter11 * 2.00);
    half3 CustomParameter13 = (CustomParameter12 * CustomParameter_Vector[8].rgb);
    half3 CustomParameter14 = (1.00 - CustomParameter13);
    half3 CustomParameter15 = (CustomParameter9.rgb * 2.00);
    half3 CustomParameter16 = (CustomParameter15 * CustomParameter_Vector[7].rgb);
    half CustomParameter17 = ((CustomParameter9.rgb.r >= 0.50) ? CustomParameter14.r : CustomParameter16.r);
    half CustomParameter18 = ((CustomParameter9.rgb.g >= 0.50) ? CustomParameter14.g : CustomParameter16.g);
    half CustomParameter19 = ((CustomParameter9.rgb.b >= 0.50) ? CustomParameter14.b : CustomParameter16.b);
    half3 CustomParameter20 = lerp(CustomParameter9.rgb,half3(float2(CustomParameter17,CustomParameter18),CustomParameter19),half(CustomParameter_Scalar[1].y));
    half CustomParameter21 = 0;
    //TextureSampler using UVs,tex2D index((Parameters, CustomParameter1, 4);
    half4 CustomParameter22 = tex2D(CustomParameter_tex2D_2, GetMaterialSharedSampler(CustomParameter_tex2D_2Sampler,View.MaterialTextureBilinearWrapedSampler),CustomParameter1));
    half CustomParameter23 = MaterialStoreTexSample(Parameters, CustomParameter22, 4);
    half CustomParameter24 = (CustomParameter22.g.r * CustomParameter_Scalar[1].z);
    half CustomParameter25 = (CustomParameter22.r.r * CustomParameter_Scalar[1].w);
    ;
    //fragmentContext.Normal = CustomParameter6;
    //fragmentContext.EmissiveColor = CustomParameter7;
    //fragmentContext.Opacity = 1.00;
    //fragmentContext.OpacityMask = 1.00;
    //fragmentContext.BaseColor = CustomParameter20;
    //fragmentContext.Metallic = CustomParameter24;
    //fragmentContext.Specular = 0.50;
    //fragmentContext.Roughness = CustomParameter25;
    //fragmentContext.Anisotropy = 0.00;
    //fragmentContext.Tangent = half3(1.00,0.00,0.00);
    //fragmentContext.Subsurface = 0;
    //fragmentContext.AmbientOcclusion = 1.00;
    //fragmentContext.Refraction = 0;
    //fragmentContext.PixelDepthOffset = 0.00;
    //fragmentContext.ShadingModel = 1;
}