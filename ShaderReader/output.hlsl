// ---- Created with 3Dmigoto v1.3.16 on Tue Jan 14 16:10:38 2025
Texture2DArray<float4> t4 : register(t4);

Texture2D<float4> t3 : register(t3);

Texture2D<float4> t2 : register(t2);

Texture2D<float4> t1 : register(t1);

struct t0_t {
  float val[4];

 //Branch-0 End
};
StructuredBuffer<t0_t> t0 : register(t0);

 // Texture?
SamplerState s2_s : register(s2);

 // Texture?
SamplerState s1_s : register(s1);

 // Texture?
SamplerState s0_s : register(s0);

cbuffer cb2 : register(b2)
{
  float4 cb2[20];

 //Branch-0 End
}

cbuffer cb1 : register(b1)
{
  float4 cb1[161];

 //Branch-0 End
}

cbuffer cb0 : register(b0)
{
  float4 cb0[1];

 //Branch-0 End
}




// 3Dmigoto declarations
#define cmp -


void main(
  float4 v0 : SV_Position0,
  float4 v1 : TEXCOORD6,
  float4 v2 : TEXCOORD7,
  linear centroid float4 v3 : TEXCOORD10,
  linear centroid float4 v4 : TEXCOORD11,
  float4 v5 : COLOR0,
  float4 v6 : TEXCOORD0,
  nointerpolation uint v7 : PRIMITIVE_ID0,
  float v8 : CLOTH_VISIBILITY0,
  float3 w8 : TEXCOORD8,
  uint v9 : SV_IsFrontFace0,
  out float4 o0 : SV_Target0)
{
  const float4 icb[] = { { 0.556000, 0, 0, 0},
                              { 0.889000, 0, 0, 0},
                              { 0.333000, 0, 0, 0},
                              { 1.000000, 0, 0, 0},
                              { 0.667000, 0, 0, 0},
                              { 0.111000, 0, 0, 0},
                              { 0.444000, 0, 0, 0},
                              { 0.222000, 0, 0, 0},
                              { 0.778000, 0, 0, 0} };
  float4 r0,r1,r2,r3,r4,r5,r6,r7;
  uint4 bitmask, uiDest;
  float4 fDest;

  r0.xy = (int2)v0.xy;
  r0.zw = (int2)r0.xy ^ int2(3,3);
  r0.xy = max((int2)-r0.xy, (int2)r0.xy);
  uiDest.xy = (uint2)r0.xy / int2(3,3);
  r0.xy = uiDest.xy;
  r0.zw = (int2)r0.zw & int2(0x80000000,0x80000000);
  r1.xy = -(int2)r0.xy;
  r0.xy = r0.zw ? r1.xy : r0.xy;
  r0.xy = (int2)r0.xy;
  r0.zw = trunc(v0.xy);
// UV?
  r0.xy = -r0.xy * float2(3,3) + r0.zw;
  r0.xy = (int2)r0.xy;
  r0.x = mad((int)r0.y, 3, (int)r0.x);
  r0.y = 1 + -cb0[0].x;
  r0.x = r0.y * 1.00999999 + -icb[r0.x+0].x;
  r0.x = cmp(r0.x < 0);

 //Branch-1 Begin 
  if (r0.x != 0) discard;

 //Branch-2 Begin 
  if (r0.x != 0) discard;
  r0.xyz = -cb1[112].xyz + w8.xyz;
  r0.xyz = -cb1[110].xyz + r0.xyz;
  r1.xyz = float3(4.76837158e-007,4.76837158e-007,4.76837158e-007) * r0.xyz;
  r2.xyz = r1.xyz * r0.xyz;
  r1.xyz = float3(2,2,2) * r1.xyz;
  r0.w = r2.x + r2.y;
  r0.w = r0.w + r2.z;
  r0.w = 4.76837158e-007 * r0.w;
  r2.xyz = cb1[109].xyz + -cb1[109].xyz;
  r1.xyz = r2.xyz + r1.xyz;
  r1.xyz = r2.xyz * r1.xyz;
  r1.x = r1.x + r1.y;
  r1.x = r1.x + r1.z;
  r0.w = r1.x + r0.w;
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r0.w = 4.76837158e-007 * r0.w;
  r1.xyz = r2.xyz * r0.www;
  r0.xyz = r0.xyz * r0.www;
  r1.xyz = float3(2097152,2097152,2097152) * r1.xyz;
  r0.xyz = r1.xyz + r0.xyz;
  r0.xyz = float3(-1,-1,-1) * r0.xyz;
  r1.xyz = cb1[62].yzx * r0.zxy;
  r2.xyz = cb1[62].zxy * r0.yzx;
  r1.xyz = -r2.xyz + r1.xyz;
  r0.w = dot(r1.xyz, r1.xyz);
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r1.xyz = r1.xyz * r0.www;
  r2.xyz = r1.zxy * r0.yzx;
  r3.xyz = r1.yzx * r0.zxy;
  r2.xyz = -r3.xyz + r2.xyz;
  r0.w = dot(r2.xyz, r2.xyz);
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r2.xyz = r2.xyz * r0.www;
  r3.z = 0.0399999991;
// UV?
  r3.xy = float2(-0.5,-0.5) + v6.xy;
  r0.w = dot(r3.xyz, r3.xyz);
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r4.xyz = r3.xyz * r0.www;
  r2.xyz = r4.yyy * r2.xyz;
  r1.xyz = r4.xxx * r1.xyz;
  r0.xyz = r4.zzz * r0.xyz;
  r1.xyz = r1.xyz + r2.xyz;
  r0.xyz = r1.xyz + r0.xyz;
  r0.w = dot(r0.xyz, r0.xyz);
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r0.xyz = r0.xyz * r0.www;
  r1.xyzw = v4.zxxy * v3.xyyz;
  r2.xyzw = v4.xyyz * v3.zxxy;
  r1.xyzw = -r2.xyzw + r1.xyzw;
  r0.w = dot(r1.wxz, r1.wxz);
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r1.xyzw = r1.xyzw * r0.wwww;
  r2.xyzw = float4(1,0,0,1) * r1.xyzw;
  r1.xy = r2.xy + -r2.zw;
  r0.w = dot(r1.xy, r1.xy);
  r1.w = 1 / sqrt(r0.w);
 //Original Codes :   r1.w = rsqrt(r0.w); Normalize ? 

  r1.xy = r1.xy * r1.ww;
  r1.w = cmp(r0.w >= 9.99999997e-007);
  r0.w = -9.99999997e-007 + r0.w;
  r0.w = cmp(9.99999975e-006 < abs(r0.w));
  r1.xy = r1.ww ? r1.xy : 0;
  r2.yz = r0.ww ? r1.xy : 0;
  r0.w = dot(r2.yz, r0.xy);
  r4.xy = r2.yz * r0.ww;
  r4.z = 0;
  r0.xyz = -r4.xyz + r0.xyz;
  r2.x = 0;
  r1.xyw = r2.xyz * r0.yzx;
  r2.xz = r2.zy * r0.zy;
  r2.y = 0;
  r1.xyw = r2.xyz + -r1.xyw;
  r0.w = -0.156582996 * abs(r1.z);
  r0.w = 1.57079637 + r0.w;
  r2.x = 1 + -abs(r1.z);
  r1.z = cmp(r1.z >= 0);
  r2.x = sqrt(r2.x);
  r0.w = r2.x * r0.w;
  r2.x = 3.14159274 + -r0.w;
  r0.w = r1.z ? r0.w : r2.x;
  r0.w = 0.159235656 * r0.w;
  r0.w = 6.28318548 * r0.w;
  sincos(r0.w, r2.x, r5.x);
  r1.xyz = r2.xxx * r1.xyw;
  r0.xyz = r5.xxx * r0.xyz;
  r0.xyz = r0.xyz + r1.xyz;
  r0.xyz = r4.xyz + r0.xyz;
  r0.w = dot(r0.xyz, r0.xyz);
  r0.w = 1 / sqrt(r0.w);
 //Original Codes :   r0.w = rsqrt(r0.w); Normalize ? 

  r0.xyz = r0.xyz * r0.www;
  r0.w = max(abs(r0.x), abs(r0.y));
  r0.w = 1 / r0.w;
  r1.x = min(abs(r0.x), abs(r0.y));
  r0.w = r1.x * r0.w;
  r1.x = r0.w * r0.w;
  r1.y = 0.0208350997 * r1.x;
  r1.y = -0.0851330012 + r1.y;
  r1.y = r1.x * r1.y;
  r1.y = 0.180141002 + r1.y;
  r1.y = r1.x * r1.y;
  r1.y = -0.330299497 + r1.y;
  r1.x = r1.x * r1.y;
  r1.x = 0.999866009 + r1.x;
  r0.w = r1.x * r0.w;
  r1.x = -2 * r0.w;
  r1.x = 1.57079637 + r1.x;
  r1.y = cmp(abs(r0.y) < abs(r0.x));
  r1.x = r1.y ? r1.x : 0;
  r0.w = r1.x + r0.w;
  r1.x = cmp(-r0.y < r0.y);
  r1.x = r1.x ? -3.141593 : 0;
  r0.w = r1.x + r0.w;
  r1.x = min(r0.x, -r0.y);
  r1.x = cmp(r1.x < -r1.x);
  r0.x = max(r0.x, -r0.y);
  r0.x = cmp(r0.x >= -r0.x);
  r0.x = r0.x ? r1.x : 0;
  r0.x = r0.x ? -r0.w : r0.w;
  r0.x = 0.318309873 * r0.x;
  r0.x = 1 + r0.x;
  r1.x = 0.5 * r0.x;
  r0.x = -0.0187292993 * abs(r0.z);
  r0.x = 0.0742610022 + r0.x;
  r0.x = r0.x * abs(r0.z);
  r0.x = -0.212114394 + r0.x;
  r0.x = r0.x * abs(r0.z);
  r0.x = 1.57072878 + r0.x;
  r0.y = 1 + -abs(r0.z);
  r0.z = cmp(r0.z < -r0.z);
  r0.y = sqrt(r0.y);
  r0.x = r0.x * r0.y;
  r0.y = -2 * r0.x;
  r0.y = 3.14159274 + r0.y;
  r0.y = r0.z ? r0.y : 0;
  r0.x = r0.x + r0.y;
  r1.y = 0.318309873 * r0.x;
  r0.x = cb2[5].x + -cb2[5].y;
  r0.y = 2 * v5.z;
  r0.y = -1 + r0.y;
  r0.x = r0.y * r0.x;
  r1.z = cb2[5].y + r0.x;
 // Texture?
  r0.x = t4.SampleBias(s0_s, r1.xyz, cb2[5].z).x;
  r0.zw = cb2[4].xy + -cb2[4].zw;
  r0.yz = r0.yy * r0.zw;
  r0.yz = cb2[4].zw + r0.yz;
  r0.z = r0.z + -r0.y;
  r0.x = r0.x * r0.z;
  r0.x = r0.y + r0.x;
// UV?
  r0.yz = float2(2,2) * r3.xy;
  r0.w = dot(r3.xy, r3.xy);
  r0.w = sqrt(r0.w);
  r0.w = -r0.w * 2.22222233 + 1;
  r0.w = saturate(100000 * r0.w);
  r0.y = dot(r0.yz, r0.yz);
  r0.y = sqrt(r0.y);
  r0.x = cmp(r0.x >= r0.y);
  r0.x = r0.x ? 1.000000 : 0;
 // Texture?
  r0.y = t1.SampleBias(s1_s, v6.xy, cb1[151].x).w;
  r0.x = -r0.y * r0.w + r0.x;
  r0.y = r0.y * r0.w;
  r0.z = cmp(9.99999975e-006 < abs(v5.z));
  r0.w = cmp(v5.z >= 0);
  r0.z = r0.z ? r0.w : 0;
  r0.z = r0.z ? 1.000000 : 0;
  r0.z = cb2[5].w * r0.z;
  r0.x = r0.z * r0.x + r0.y;
  r0.yz = -cb1[135].xy + v0.xy;
  r1.xy = cb1[160].xx + r0.yz;
// UV?
  r0.yz = float2(0.015625,0.015625) * r0.yz;
  r1.xy = (uint2)r1.xy;
  r0.w = (uint)r1.y << 1;
  r0.w = (int)r0.w + (int)r1.x;
  r0.w = (uint)r0.w % 5;
  r0.w = (uint)r0.w;
 // Texture?
  r1.x = t3.SampleBias(s2_s, r0.yz, cb1[151].x).x;
 // Texture?
  r0.y = t3.Sample(s0_s, r0.yz).x;
  r0.y = r0.w + r0.y;
  r0.z = r1.x + r0.w;
  r0.x = r0.z * 0.166649997 + r0.x;
  r0.x = -0.5 + r0.x;
  r0.y = 0.200000003 * r0.y;
  r0.z = 1 + -v8.x;
  r0.x = r0.x * r0.z;
  r1.xyzw = cb1[44].xyzw * v0.xxxx;
  r2.xyzw = cb1[45].xyzw * v0.yyyy;
  r1.xyzw = r2.xyzw + r1.xyzw;
  r2.xyzw = cb1[46].xyzw * v0.zzzz;
  r1.xyzw = r2.xyzw + r1.xyzw;
  r1.xyzw = cb1[47].xyzw + r1.xyzw;
  r1.xyz = r1.xyz / r1.www;
  r1.xyz = -cb1[112].xyz + r1.xyz;
  r0.z = (int)v7.x * 44;
  r0.w = mad((int)v7.x, 44, 2);
  r2.x = t0[r0.w].val[0/4];
  r2.y = t0[r0.w].val[0/4+1];
  r2.z = t0[r0.w].val[0/4+2];
  r2.w = t0[r0.w].val[0/4+3];
  r3.x = r2.y;
  r4.xy = mad((int2)v7.xx, int2(44,44), int2(4,18));
  r5.x = t0[r4.x].val[0/4];
  r5.y = t0[r4.x].val[0/4+1];
  r5.z = t0[r4.x].val[0/4+2];
  r5.w = t0[r4.x].val[0/4+3];
  r0.w = t0[r4.y].val[12/4];
  r0.w = cb2[17].x * r0.w;
  r0.w = 1 / r0.w;
 //Original Codes :   r0.w = rcp(r0.w); 

  r3.z = r5.y;
  r4.xy = mad((int2)v7.xx, int2(44,44), int2(1,3));
  r0.z = t0[r0.z].val[0/4];
  r0.z = (int)r0.z & 0x02000000;
  r0.z = r0.z ? 1 : 0;
  r6.x = t0[r4.y].val[0/4];
  r6.y = t0[r4.y].val[0/4+3];
  r6.z = t0[r4.y].val[0/4+1];
  r6.w = t0[r4.y].val[0/4+2];
  r4.x = t0[r4.x].val[0/4];
  r4.y = t0[r4.x].val[0/4+1];
  r4.z = t0[r4.x].val[0/4+2];
  r3.y = r6.z;
  r3.xyz = cb2[16].zzz * r3.xyz;
  r7.x = r2.x;
  r7.z = r5.x;
  r7.y = r6.x;
  r3.xyz = cb2[16].yyy * r7.xyz + r3.xyz;
  r5.x = r2.z;
  r6.x = r2.w;
  r6.z = r5.w;
  r5.y = r6.w;
  r2.xyz = cb2[16].www * r5.xyz + r3.xyz;
  r3.xyz = r4.xyz / float3(2097152,2097152,2097152);
  r3.xyz = round(r3.xyz);
  r4.xyz = r3.xyz * float3(-2097152,-2097152,-2097152) + r4.xyz;
  r3.xyz = -cb1[109].xyz + r3.xyz;
  r4.xyz = r6.xyz + r4.xyz;
  r2.xyz = r4.xyz + r2.xyz;
  r1.xyz = r2.xyz + -r1.xyz;
// UV?
  r2.xy = float2(4.76837158e-007,4.76837158e-007) * r1.xy;
  r2.xy = r2.xy * r1.xy;
  r1.w = r2.x + r2.y;
  r2.x = 4.76837158e-007 * r1.z;
  r1.w = r1.z * r2.x + r1.w;
// UV?
  r1.xy = r1.xy * float2(9.53674316e-007,9.53674316e-007) + r3.xy;
  r1.z = r1.z * 9.53674316e-007 + r3.z;
  r1.xy = r3.xy * r1.xy;
  r1.x = r1.x + r1.y;
  r1.x = r3.z * r1.z + r1.x;
  r1.x = r1.w * 4.76837158e-007 + r1.x;
  r1.x = sqrt(r1.x);
  r0.w = r1.x * r0.w;
  r0.w = saturate(2097152 * r0.w);
  r1.x = 1 + -r0.w;
  r1.x = r1.x + -r0.w;
  r0.w = cb2[17].y * r1.x + r0.w;
  r1.xy = cb2[16].xx * v6.xy;
 // Texture?
  r1.x = t2.Sample(s0_s, r1.xy).x;
  r0.w = saturate(-r1.x * cb2[17].z + r0.w);
  r0.w = r0.w + -r1.x;
  r0.w = cb2[17].w * r0.w + r1.x;
  r1.x = cb2[18].x * cb2[18].y + cb2[18].z;
  r0.w = -r1.x + r0.w;
  r0.w = -cb2[19].x + r0.w;
  r1.x = 1 / -cb2[19].x;
  r0.w = saturate(r1.x * r0.w);
  r1.x = r0.w * -2 + 3;
  r0.w = r0.w * r0.w;
  r0.w = r1.x * r0.w + -0.5;
  r0.y = r0.w * 2 + r0.y;
  r0.y = -0.5 + r0.y;
  r0.y = saturate(2 * r0.y);
  r0.x = r0.x * r0.y + -0.333299994;
  r0.x = cmp(r0.x < 0);

 //Branch-3 Begin 
  if (r0.x != 0) discard;
  r0.xyw = v1.xyz / v1.www;
  r0.xy = -cb1[132].xy + r0.xy;
  r1.xyz = v2.xyz / v2.www;
  r1.xy = -cb1[132].zw + r1.xy;
  r0.xyw = -r1.xyz + r0.xyw;
// UV?
  r1.xy = cmp(float2(0,0) < r0.xy);
// UV?
  r1.zw = cmp(r0.xy < float2(0,0));
  r0.xy = sqrt(abs(r0.xy));
  r1.xy = (int2)-r1.xy + (int2)r1.zw;
  r1.xy = (int2)r1.xy;
  r0.xy = r1.xy * r0.xy;
// UV?
  o0.xy = r0.xy * float2(0.352846295,0.352846295) + float2(0.499992371,0.499992371);
  r0.x = (int)r0.w & 0x0000fffe;
  r0.y = (uint)r0.w >> 16;
  r0.y = (uint)r0.y;
  r0.y = r0.y * 1.52590219e-005 + 1.52590223e-006;
  r0.x = (int)r0.x + (int)r0.z;
  r0.x = (uint)r0.x;
  r0.x = r0.x * 1.52590219e-005 + 1.52590223e-006;
// UV?
  o0.zw = min(float2(1,1), r0.yx);
  return;

 //Branch-3 End
}

