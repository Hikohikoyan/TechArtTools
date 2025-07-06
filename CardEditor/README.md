# 卡牌模板编辑器

一个基于Web的卡牌模板编辑器，可以可视化编辑卡牌模板，并根据配表数据批量生成卡牌图片。

## 功能特点

- 可视化拖放编辑卡牌模板
- 文本框链接卡牌配表数据（支持Excel、CSV、JSON格式）
- 编辑卡牌底图和属性框底图
- 保存模板配置
- 根据模板和配表批量导出PNG卡牌图集
- 设置卡牌真实尺寸等参数

## 技术栈

- 后端：Python (Flask)
- 前端：HTML5, CSS3, JavaScript
- 数据处理：Pandas, Pillow
- UI框架：Bootstrap
- 交互：jQuery, jQuery UI (拖拽功能)

## 使用方法

1. 运行 `app.py` 启动Web服务
2. 在浏览器中访问 `http://localhost:5000`
3. 上传卡牌配表数据
4. 设计卡牌模板
5. 批量导出卡牌图片