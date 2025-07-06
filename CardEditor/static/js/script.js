$(document).ready(function() {
    let selectedElement = null;
    let dataColumns = [];
    let dataFile = null;
    let nextElementId = 1;
    
    // 初始化拖拽功能
    function initDraggable() {
        $(".element").draggable({
            containment: "#card-canvas",
            stop: function(event, ui) {
                if ($(this).hasClass('selected')) {
                    updatePositionProperties($(this));
                }
            }
        });
    }
    
    // 添加文本元素
    $("#add-text").click(function() {
        const id = nextElementId++;
        const element = $(`<div id="element-${id}" class="element element-text" data-type="text">示例文本</div>`);
        element.css({
            left: '50px',
            top: '50px',
            fontSize: '24px',
            color: '#000000',
            fontFamily: 'Arial'
        });
        
        $("#card-canvas").append(element);
        initDraggable();
        selectElement(element);
    });
    
    // 添加图片元素
    $("#add-image").click(function() {
        const id = nextElementId++;
        const element = $(`<div id="element-${id}" class="element element-image" data-type="image"></div>`);
        element.css({
            left: '50px',
            top: '50px',
            width: '100px',
            height: '100px',
            backgroundColor: '#f0f0f0'
        });
        
        $("#card-canvas").append(element);
        initDraggable();
        selectElement(element);
    });
    
    // 选择元素
    $(document).on('click', '.element', function(e) {
        e.stopPropagation();
        selectElement($(this));
    });
    
    // 点击画布取消选择
    $("#card-canvas").click(function() {
        deselectElement();
    });
    
    // 选择元素函数
    function selectElement(element) {
        deselectElement();
        selectedElement = element;
        element.addClass('selected');
        $("#delete-element").prop('disabled', false);
        
        // 显示对应的属性面板
        $("#no-selection").addClass('d-none');
        $("#position-properties").removeClass('d-none');
        
        // 更新位置属性
        updatePositionProperties(element);
        
        const type = element.data('type');
        if (type === 'text') {
            $("#text-properties").removeClass('d-none');
            $("#image-properties").addClass('d-none');
            
            // 更新文本属性
            $("#text-content").val(element.text());
            $("#text-field").val(element.data('field') || '');
            $("#font-family").val(element.css('fontFamily').replace(/['"]*/g, '') || 'Arial');
            $("#font-size").val(parseInt(element.css('fontSize')) || 24);
            $("#text-color").val(rgbToHex(element.css('color')) || '#000000');
        } else if (type === 'image') {
            $("#image-properties").removeClass('d-none');
            $("#text-properties").addClass('d-none');
            
            // 更新图片属性
            $("#image-field").val(element.data('field') || '');
            $("#image-width").val(parseInt(element.css('width')));
            $("#image-height").val(parseInt(element.css('height')));
        }
    }
    
    // 取消选择元素
    function deselectElement() {
        if (selectedElement) {
            selectedElement.removeClass('selected');
            selectedElement = null;
        }
        
        $("#delete-element").prop('disabled', true);
        $("#no-selection").removeClass('d-none');
        $("#text-properties").addClass('d-none');
        $("#image-properties").addClass('d-none');
    }
    
    // 更新位置属性
    function updatePositionProperties(element) {
        $("#element-x").val(parseInt(element.css('left')));
        $("#element-y").val(parseInt(element.css('top')));
    }
    
    // 删除元素
    $("#delete-element").click(function() {
        if (selectedElement) {
            selectedElement.remove();
            deselectElement();
        }
    });
    
    // 清空画布
    $("#clear-canvas").click(function() {
        if (confirm('确定要清空画布吗？所有元素将被删除。')) {
            $("#card-canvas").empty();
            deselectElement();
            $("#card-canvas").css('backgroundImage', '');
        }
    });
    
    // 文本属性变更
    $("#text-content").on('input', function() {
        if (selectedElement && selectedElement.data('type') === 'text') {
            selectedElement.text($(this).val());
        }
    });
    
    $("#text-field").on('change', function() {
        if (selectedElement && selectedElement.data('type') === 'text') {
            selectedElement.data('field', $(this).val());
        }
    });
    
    $("#font-family").on('change', function() {
        if (selectedElement && selectedElement.data('type') === 'text') {
            selectedElement.css('fontFamily', $(this).val());
        }
    });
    
    $("#font-size").on('input', function() {
        if (selectedElement && selectedElement.data('type') === 'text') {
            selectedElement.css('fontSize', $(this).val() + 'px');
        }
    });
    
    $("#text-color").on('input', function() {
        if (selectedElement && selectedElement.data('type') === 'text') {
            selectedElement.css('color', $(this).val());
        }
    });
    
    // 图片属性变更
    $("#image-upload").on('change', function() {
        if (selectedElement && selectedElement.data('type') === 'image' && this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                selectedElement.css('backgroundImage', `url(${e.target.result})`);
                selectedElement.data('image', e.target.result);
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    $("#image-field").on('change', function() {
        if (selectedElement && selectedElement.data('type') === 'image') {
            selectedElement.data('field', $(this).val());
        }
    });
    
    $("#image-width").on('input', function() {
        if (selectedElement && selectedElement.data('type') === 'image') {
            selectedElement.css('width', $(this).val() + 'px');
        }
    });
    
    $("#image-height").on('input', function() {
        if (selectedElement && selectedElement.data('type') === 'image') {
            selectedElement.css('height', $(this).val() + 'px');
        }
    });
    
    // 位置属性变更
    $("#element-x").on('input', function() {
        if (selectedElement) {
            selectedElement.css('left', $(this).val() + 'px');
        }
    });
    
    $("#element-y").on('input', function() {
        if (selectedElement) {
            selectedElement.css('top', $(this).val() + 'px');
        }
    });
    
    // 卡牌尺寸变更
    $("#card-width").on('input', function() {
        $("#card-canvas").css('width', $(this).val() + 'px');
    });
    
    $("#card-height").on('input', function() {
        $("#card-canvas").css('height', $(this).val() + 'px');
    });
    
    // 设置背景图
    $("#background-image").on('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $("#card-canvas").css('backgroundImage', `url(${e.target.result})`);
                $("#card-canvas").data('background', e.target.result);
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    // 上传数据文件
    $("#upload-form").submit(function(e) {
        e.preventDefault();
        const fileInput = document.getElementById('data-file');
        if (fileInput.files.length === 0) {
            alert('请选择一个文件');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    dataFile = response.filename;
                    dataColumns = response.columns;
                    
                    // 更新文件信息
                    $("#file-name").text(`文件名: ${response.filename}`);
                    $("#file-rows").text(`行数: ${response.rows}`);
                    $("#file-info").removeClass('d-none');
                    
                    // 更新字段选择器
                    updateFieldSelectors(dataColumns);
                    
                    // 启用生成按钮
                    $("#generate-cards").prop('disabled', false);
                } else {
                    alert('上传失败: ' + response.error);
                }
            },
            error: function(xhr) {
                alert('上传失败: ' + (xhr.responseJSON ? xhr.responseJSON.error : '未知错误'));
            }
        });
    });
    
    // 更新字段选择器
    function updateFieldSelectors(columns) {
        const textField = $("#text-field");
        const imageField = $("#image-field");
        
        textField.empty().append('<option value="">无</option>');
        imageField.empty().append('<option value="">无</option>');
        
        columns.forEach(function(column) {
            textField.append(`<option value="${column}">${column}</option>`);
            imageField.append(`<option value="${column}">${column}</option>`);
        });
    }
    
    // 保存模板
    $("#save-template").click(function() {
        const templateName = $("#template-name").val();
        if (!templateName) {
            alert('请输入模板名称');
            return;
        }
        
        const templateData = getTemplateData();
        
        $.ajax({
            url: '/save_template',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                template_name: templateName,
                template_data: templateData
            }),
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    loadTemplateList();
                } else {
                    alert('保存失败: ' + response.error);
                }
            },
            error: function(xhr) {
                alert('保存失败: ' + (xhr.responseJSON ? xhr.responseJSON.error : '未知错误'));
            }
        });
    });
    
    // 获取模板数据
    function getTemplateData() {
        const elements = [];
        
        $(".element").each(function() {
            const $el = $(this);
            const type = $el.data('type');
            const element = {
                type: type,
                x: parseInt($el.css('left')),
                y: parseInt($el.css('top'))
            };
            
            if (type === 'text') {
                element.text = $el.text();
                element.field = $el.data('field') || '';
                element.fontFamily = $el.css('fontFamily').replace(/['"]*/g, '');
                element.fontSize = parseInt($el.css('fontSize'));
                element.color = hexToRgb($el.css('color'));
            } else if (type === 'image') {
                element.field = $el.data('field') || '';
                element.width = parseInt($el.css('width'));
                element.height = parseInt($el.css('height'));
                element.image = $el.data('image') || '';
            }
            
            elements.push(element);
        });
        
        return {
            width: parseInt($("#card-width").val()),
            height: parseInt($("#card-height").val()),
            background: $("#card-canvas").data('background') || '',
            elements: elements
        };
    }
    
    // 加载模板列表
    function loadTemplateList() {
        $.ajax({
            url: '/templates',
            type: 'GET',
            success: function(response) {
                const templateList = $("#template-list ul");
                templateList.empty();
                
                if (response.templates.length > 0) {
                    response.templates.forEach(function(template) {
                        templateList.append(`<li class="list-group-item template-item" data-name="${template}">${template}</li>`);
                    });
                    $("#template-list").removeClass('d-none');
                } else {
                    $("#template-list").addClass('d-none');
                }
            }
        });
    }
    
    // 加载模板按钮
    $("#load-template").click(function() {
        loadTemplateList();
        const templatesModal = new bootstrap.Modal(document.getElementById('templates-modal'));
        
        // 加载模板预览
        $.ajax({
            url: '/templates',
            type: 'GET',
            success: function(response) {
                const container = $("#templates-container");
                container.empty();
                
                if (response.templates.length > 0) {
                    response.templates.forEach(function(template) {
                        const card = $(`
                            <div class="col-md-4 mb-3">
                                <div class="card preview-card" data-name="${template}">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">${template}</h5>
                                        <button class="btn btn-sm btn-primary load-template-btn">加载</button>
                                    </div>
                                </div>
                            </div>
                        `);
                        container.append(card);
                    });
                } else {
                    container.html('<div class="col-12 text-center">没有保存的模板</div>');
                }
                
                templatesModal.show();
            }
        });
    });
    
    // 点击加载模板
    $(document).on('click', '.load-template-btn', function() {
        const templateName = $(this).closest('.preview-card').data('name');
        loadTemplate(templateName);
        bootstrap.Modal.getInstance(document.getElementById('templates-modal')).hide();
    });
    
    // 点击模板列表项
    $(document).on('click', '.template-item', function() {
        const templateName = $(this).data('name');
        loadTemplate(templateName);
    });
    
    // 加载模板
    function loadTemplate(templateName) {
        $.ajax({
            url: `/template/${templateName}`,
            type: 'GET',
            success: function(templateData) {
                // 清空画布
                $("#card-canvas").empty();
                
                // 设置卡牌尺寸
                $("#card-width").val(templateData.width || 750);
                $("#card-height").val(templateData.height || 1050);
                $("#card-canvas").css({
                    width: templateData.width + 'px',
                    height: templateData.height + 'px'
                });
                
                // 设置背景
                if (templateData.background) {
                    $("#card-canvas").css('backgroundImage', `url(${templateData.background})`);
                    $("#card-canvas").data('background', templateData.background);
                }
                
                // 添加元素
                templateData.elements.forEach(function(element) {
                    let $el;
                    if (element.type === 'text') {
                        $el = $(`<div class="element element-text" data-type="text">${element.text}</div>`);
                        $el.css({
                            left: element.x + 'px',
                            top: element.y + 'px',
                            fontSize: element.fontSize + 'px',
                            fontFamily: element.fontFamily,
                            color: rgbToString(element.color)
                        });
                        $el.data('field', element.field || '');
                    } else if (element.type === 'image') {
                        $el = $(`<div class="element element-image" data-type="image"></div>`);
                        $el.css({
                            left: element.x + 'px',
                            top: element.y + 'px',
                            width: element.width + 'px',
                            height: element.height + 'px'
                        });
                        if (element.image) {
                            $el.css('backgroundImage', `url(${element.image})`);
                            $el.data('image', element.image);
                        }
                        $el.data('field', element.field || '');
                    }
                    
                    if ($el) {
                        $("#card-canvas").append($el);
                        nextElementId++;
                    }
                });
                
                // 初始化拖拽
                initDraggable();
                
                // 更新模板名称
                $("#template-name").val(templateName);
            },
            error: function() {
                alert('加载模板失败');
            }
        });
    }
    
    // 生成卡牌
    $("#generate-cards").click(function() {
        if (!dataFile) {
            alert('请先上传数据文件');
            return;
        }
        
        const templateData = getTemplateData();
        
        $.ajax({
            url: '/generate_cards',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                template_data: templateData,
                data_file: dataFile
            }),
            success: function(response) {
                if (response.success) {
                    $("#generation-message").text(response.message);
                    $("#download-link").attr('href', response.download_url);
                    $("#generation-info").removeClass('d-none');
                } else {
                    alert('生成卡牌失败: ' + response.error);
                }
            },
            error: function(xhr) {
                alert('生成卡牌失败: ' + (xhr.responseJSON ? xhr.responseJSON.error : '未知错误'));
            }
        });
    });
    
    // 辅助函数：RGB转十六进制
    function rgbToHex(rgb) {
        if (!rgb) return '#000000';
        
        // 处理rgb(r, g, b)格式
        const match = rgb.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
        if (match) {
            return '#' + (
                (1 << 24) + 
                (parseInt(match[1]) << 16) + 
                (parseInt(match[2]) << 8) + 
                parseInt(match[3])
            ).toString(16).slice(1);
        }
        
        return rgb;
    }
    
    // 辅助函数：十六进制转RGB数组
    function hexToRgb(hex) {
        if (!hex) return [0, 0, 0];
        
        // 处理rgb(r, g, b)格式
        const match = hex.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
        if (match) {
            return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
        }
        
        // 处理十六进制格式
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? [
            parseInt(result[1], 16),
            parseInt(result[2], 16),
            parseInt(result[3], 16)
        ] : [0, 0, 0];
    }
    
    // 辅助函数：RGB数组转字符串
    function rgbToString(rgb) {
        if (Array.isArray(rgb) && rgb.length === 3) {
            return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
        }
        return '#000000';
    }
});