_RoughnessTex("粗糙度贴图 RoughnessTex", 2D) = "black" {}
// 粗糙度贴图

_BaseColorTex("颜色贴图 BaseColorTex", 2D) = "white" {}
// 颜色贴图

_AOTex("AO贴图 AOTex", 2D) = "black" {}
// AO贴图

_NormalTex("法线贴图 NormalTex", 2D) = "bump" {}
// 法线贴图

_TintColor("叠色 TintColor", Color) = (1,1,1) 
// 叠色

_ShadowIntensity("阴影强度 ShadowIntensity", Range(0,1)) =   1.0
// 阴影强度

_Lerp_Color("0原贴图颜色-1叠色 Lerp_Color", Range(0,1)) =   0.50
// 0原贴图颜色-1叠色

_BottomMaskSmooth("接地过渡的边缘软硬 BottomMaskSmooth", Range(0,1)) =   0.60
// 接地过渡的边缘软硬

_BottomMaskBias("接地过渡的高度 BottomMaskBias", Range(0,1)) =   3.30
// 接地过渡的高度

_BakedAO("顶点色AO强度（R通道） BakedAO", Range(0,1)) =   0.40
// 顶点色AO强度（R通道）

_DetailUV("细节UV大小 DetailUV", Range(0,1)) =   5.0
// 细节UV大小

_NormalDetailTex("细节法线贴图 NormalDetailTex", 2D) = "bump" {}
// 细节法线贴图

_DetailRo("细节法线贴图旋转角度[0,360] DetailRo", Range(0,1)) =   90.0
// 细节法线贴图旋转角度[0,360]

_Detail_V_Scale("细节法线贴图V方向缩放 Detail_V_Scale", Range(0,1)) =   0.50
// 细节法线贴图V方向缩放

_DepthThreshold(" DepthThreshold", Range(0,1)) =   0.60
// 

_WorldColorIntensity("接地颜色明度 WorldColorIntensity", Range(0,1)) =   1.0
// 接地颜色明度

_LightMask("受光面遮罩 LightMask", Range(0,1)) =   0.50
// 受光面遮罩

_U_Scale("基础贴图U方向缩放 U_Scale", Range(0,1)) =   1.0
// 基础贴图U方向缩放

_WorldColorLerp("接地颜色透明度0-1 WorldColorLerp", Range(0,1)) =   1.0
// 接地颜色透明度0-1
