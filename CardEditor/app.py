import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMPLATE_FOLDER'] = 'templates'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls', 'json'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMPLATE_FOLDER'], exist_ok=True)
os.makedirs('static/images', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        # 确保文件名不为空
        if file.filename:
            filename = secure_filename(file.filename)
        else:
            return jsonify({'error': '无效的文件名'}), 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 初始化df变量，确保在任何情况下都有定义
        df = None
        columns = []
        rows = 0
        
        # 解析文件并返回列名
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif filename.endswith('.json'):
                df = pd.read_json(file_path)
            
            # 确保df已定义后再获取列名
            if df is not None:
                columns = df.columns.tolist()
                rows = len(df)
        except Exception as e:
            return jsonify({'error': f'解析文件时出错: {str(e)}'}), 500
        
        return jsonify({
            'success': True,
            'filename': filename,
            'columns': columns,
            'rows': rows
        })
    
    return jsonify({'error': '不允许的文件类型'}), 400

@app.route('/save_template', methods=['POST'])
def save_template():
    data = request.json
    template_name = data.get('template_name')
    template_data = data.get('template_data')
    
    if not template_name or not template_data:
        return jsonify({'error': '模板名称或数据缺失'}), 400
    
    # 保存模板配置
    template_path = os.path.join(app.config['TEMPLATE_FOLDER'], f'{template_name}.json')
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True, 'message': f'模板 {template_name} 已保存'})

@app.route('/templates', methods=['GET'])
def list_templates():
    templates = []
    for filename in os.listdir(app.config['TEMPLATE_FOLDER']):
        if filename.endswith('.json'):
            templates.append(filename.rsplit('.', 1)[0])
    
    return jsonify({'templates': templates})

@app.route('/template/<name>', methods=['GET'])
def get_template(name):
    template_path = os.path.join(app.config['TEMPLATE_FOLDER'], f'{name}.json')
    
    if not os.path.exists(template_path):
        return jsonify({'error': '模板不存在'}), 404
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_data = json.load(f)
    
    return jsonify(template_data)

@app.route('/generate_cards', methods=['POST'])
def generate_cards():
    data = request.json
    template_data = data.get('template_data')
    data_file = data.get('data_file')
    
    if not template_data or not data_file:
        return jsonify({'error': '模板数据或数据文件缺失'}), 400
    
    # 加载数据文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], data_file)
    try:
        if data_file.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif data_file.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        elif data_file.endswith('.json'):
            df = pd.read_json(file_path)
    except Exception as e:
        return jsonify({'error': f'读取数据文件时出错: {str(e)}'}), 500
    
    # 创建临时目录存储生成的卡牌
    temp_dir = os.path.join('static', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # 生成卡牌图片
    card_paths = []
    for index, row in df.iterrows():
        try:
            card_path = generate_card_image(template_data, row, index, temp_dir)
            card_paths.append(card_path)
        except Exception as e:
            return jsonify({'error': f'生成卡牌 {index} 时出错: {str(e)}'}), 500
    
    # 创建ZIP文件
    zip_path = os.path.join('static', 'cards.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for card_path in card_paths:
            zipf.write(card_path, os.path.basename(card_path))
    
    return jsonify({
        'success': True,
        'message': f'已生成 {len(card_paths)} 张卡牌',
        'download_url': url_for('static', filename='cards.zip')
    })

def generate_card_image(template_data, row_data, index, output_dir):
    # 获取卡牌尺寸
    card_width = template_data.get('width', 750)
    card_height = template_data.get('height', 1050)
    
    # 创建基础图像
    card_image = Image.new('RGBA', (card_width, card_height), (255, 255, 255, 0))
    
    # 添加背景图
    if 'background' in template_data and template_data['background']:
        bg_data = template_data['background'].split(',')[1]
        bg_image = Image.open(io.BytesIO(base64.b64decode(bg_data)))
        bg_image = bg_image.resize((card_width, card_height))
        card_image.paste(bg_image, (0, 0))
    
    draw = ImageDraw.Draw(card_image)
    
    # 添加文本元素
    for element in template_data.get('elements', []):
        if element['type'] == 'text':
            # 获取字段值
            field_name = element.get('field')
            text = str(row_data.get(field_name, '')) if field_name else element.get('text', '')
            
            # 设置字体
            font_size = element.get('fontSize', 24)
            try:
                font = ImageFont.truetype(element.get('fontFamily', 'arial.ttf'), font_size)
            except IOError:
                font = ImageFont.load_default()
            
            # 绘制文本
            position = (element.get('x', 0), element.get('y', 0))
            color = tuple(element.get('color', (0, 0, 0)))
            draw.text(position, text, font=font, fill=color)
        
        elif element['type'] == 'image' and 'field' in element:
            # 处理图像元素（如果数据中包含图像URL或Base64）
            field_name = element.get('field')
            image_data = row_data.get(field_name)
            if image_data and isinstance(image_data, str):
                try:
                    if image_data.startswith('data:image'):
                        # Base64图像
                        img_data = image_data.split(',')[1]
                        img = Image.open(io.BytesIO(base64.b64decode(img_data)))
                    else:
                        # 假设是本地路径
                        img_path = os.path.join('static', 'images', image_data)
                        if os.path.exists(img_path):
                            img = Image.open(img_path)
                        else:
                            continue
                    
                    # 调整图像大小并放置
                    img = img.resize((element.get('width', 100), element.get('height', 100)))
                    card_image.paste(img, (element.get('x', 0), element.get('y', 0)))
                except Exception:
                    pass
    
    # 保存卡牌图像
    output_path = os.path.join(output_dir, f'card_{index}.png')
    card_image.save(output_path)
    
    return output_path

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('static', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)