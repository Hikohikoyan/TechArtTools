, 2D) ="white" {} NormalTex;
// 法线贴图

, Range(0,1)) =   TintColor;
// 叠色

, Range(0,1)) =   ShadowIntensity;
// 阴影强度

, Range(0,1)) =   Lerp_Color;
// 0原贴图颜色-1叠色

, Range(0,1)) =   BottomMaskSmooth;
// 接地过渡的边缘软硬

, Range(0,1)) =   BottomMaskBias;
// 接地过渡的高度

, Range(0,1)) =   BakedAO;
// 顶点色AO强度（R通道）

, 2D) ="white" {} NormalDetailTex;
// 细节法线贴图

, Range(0,1)) =   DetailRo;
// 细节法线贴图旋转角度[0,360]

, Range(0,1)) =   Detail_V_Scale;
// 细节法线贴图V方向缩放

, Range(0,1)) =   DepthThreshold;
// 

, Range(0,1)) =   WorldColorIntensity;
// 接地颜色明度

, Range(0,1)) =   LightMask;
// 受光面遮罩

, Range(0,1)) =   U_Scale;
// 基础贴图U方向缩放
