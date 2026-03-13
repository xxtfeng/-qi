import io
from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# 中文字体路径（请根据实际情况修改）
FONT_PATH = "simhei.ttf"  # 如果使用其他字体，请修改此处
try:
    title_font = ImageFont.truetype(FONT_PATH, 40)
    label_font = ImageFont.truetype(FONT_PATH, 28)
    value_font = ImageFont.truetype(FONT_PATH, 28)
except:
    # 回退到默认字体（不支持中文）
    title_font = ImageFont.load_default()
    label_font = ImageFont.load_default()
    value_font = ImageFont.load_default()

# HTML 表单模板
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>贷款图片生成器</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 500px; margin: auto; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input[type="text"], input[type="number"] { width: 100%; padding: 8px; box-sizing: border-box; }
        input[type="submit"] { margin-top: 25px; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; font-size: 16px; }
        input[type="submit"]:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h2>贷款图片生成器</h2>
        <p>填写以下信息，生成贷款详情图片</p >
        <form action="/generate" method="post">
            <label>姓名：</label>
            <input type="text" name="name" value="张三" required>

            <label>手机号：</label>
            <input type="text" name="phone" value="13800138000" required>

            <label>身份证号码：</label>
            <input type="text" name="id_card" value="123456199001011234" required>

            <label>贷款金额（元）：</label>
            <input type="number" name="amount" step="0.01" value="100000.00" required>

            <label>年利率（%）：</label>
            <input type="number" name="rate" step="0.01" value="4.5" required>

            <label>月供（元）：</label>
            <input type="number" name="monthly_payment" step="0.01" value="4567.89" required>

            <label>日期：</label>
            <input type="text" name="date" value="2025-03-13" required>

            <label>状态：</label>
            <input type="text" name="status" value="审批通过" required>

            <input type="submit" value="生成图片">
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/generate', methods=['POST'])
def generate_image():
    # 获取表单数据
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    id_card = request.form.get('id_card', '').strip()
    amount = request.form.get('amount', '').strip()
    rate = request.form.get('rate', '').strip()
    monthly_payment = request.form.get('monthly_payment', '').strip()
    date = request.form.get('date', '').strip()
    status = request.form.get('status', '').strip()

    # 验证必填字段
    if not all([name, phone, id_card, amount, rate, monthly_payment, date, status]):
        return "所有字段均为必填", 400

    # 创建图片
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 绘制标题
    title = "贷款信息单"
    draw.text((50, 30), title, fill=(0, 0, 0), font=title_font)

    # 绘制分隔线
    draw.line([(50, 90), (750, 90)], fill=(200, 200, 200), width=2)

    # 准备数据行 (字段名, 值)
    rows = [
        ("姓名", name),
        ("手机号", phone),
        ("身份证号", id_card),
        ("贷款金额 (元)", amount),
        ("年利率 (%)", rate),
        ("月供 (元)", monthly_payment),
        ("日期", date),
        ("状态", status),
    ]

    y_start = 120
    row_height = 50
    for i, (label, value) in enumerate(rows):
        y = y_start + i * row_height
        # 绘制字段名
        draw.text((50, y), label + "：", fill=(50, 50, 50), font=label_font)
        # 绘制字段值（蓝色突出）
        draw.text((250, y), value, fill=(0, 0, 255), font=value_font)

    # 保存图片到内存
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=False, download_name='loan_info.png')

if __name__ == '__main__':
    app.run(debug=True)