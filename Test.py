from PIL import Image
import numpy as np
path = 'F:/TechFuture/yume-deutung/Demo/01-Deutung/Assets/inputs/input3_handmade_test_02.png'
# 加载深度图
depth_img = Image.open(path)
depth_data = np.array(depth_img, dtype=np.uint16)

# 相机内参和外参参数
fx = 500  # 相机焦距 x
fy = 500  # 相机焦距 y
cx = 320  # 光心坐标 x
cy = 240  # 光心坐标 y
tx = 0  # 相机在世界坐标系中的位置 x
ty = 0  # 相机在世界坐标系中的位置 y
tz = 0  # 相机在世界坐标系中的位置 z
rx = 0  # 相机朝向 x
ry = 0  # 相机朝向 y
rz = 0  # 相机朝向 z

# 计算每个像素点的3D坐标
rows, cols = depth_data.shape
points = []
for i in range(rows):
    for j in range(cols):
        depth = depth_data[i, j]
        if depth == 0:
            continue
        x = (j - cx) * depth / fx
        y = (i - cy) * depth / fy
        z = depth
        points.append([x, y, z])

# 保存点云数据为PLY格式文件
points = np.array(points)
with open('pointcloud.ply', 'w') as f:
    f.write('ply\n')
    f.write('format ascii 1.0\n')
    f.write('element vertex %d\n' % len(points))
    f.write('property float x\n')
    f.write('property float y\n')
    f.write('property float z\n')
    f.write('end_header\n')
    for p in points:
        f.write('%f %f %f\n' % (p[0], p[1], p[2]))