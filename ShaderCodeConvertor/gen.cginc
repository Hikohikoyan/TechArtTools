sampler2D RoughnessTex;
// 粗糙度贴图

sampler2D BaseColorTex;
// 颜色贴图

sampler2D AOTex;
// AO贴图

sampler2D NormalTex;
// 法线贴图

half4 TintColor;
// 叠色

half ShadowIntensity;
// 阴影强度

half Lerp_Color;
// 0原贴图颜色-1叠色

half BottomMaskSmooth;
// 接地过渡的边缘软硬

half BottomMaskBias;
// 接地过渡的高度

half BakedAO;
// 顶点色AO强度（R通道）

half DetailUV;
// 细节UV大小

sampler2D NormalDetailTex;
// 细节法线贴图

half DetailRo;
// 细节法线贴图旋转角度[0,360]

half Detail_V_Scale;
// 细节法线贴图V方向缩放

half DepthThreshold;
// 

half WorldColorIntensity;
// 接地颜色明度

half LightMask;
// 受光面遮罩

half U_Scale;
// 基础贴图U方向缩放

half WorldColorLerp;
// 接地颜色透明度0-1
