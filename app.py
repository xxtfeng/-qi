import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import io

# 1. 计算月供的逻辑
def calculate_monthly_payment(principal, annual_rate, months=12):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0: return principal / months
    payment = (principal * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    return payment

# 2. 生成图片的逻辑
def generate_loan_image(data):
    width, height = 800, 650
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        # 使用你确认的 simsunb.ttf 文件
        font_path = "simsunb.ttf" 
        title_font = ImageFont.truetype(font_path, 40)
        label_font = ImageFont.truetype(font_path, 22)
        value_font = ImageFont.truetype(font_path, 24)
    except:
        st.error("找不到 simsunb.ttf 文件，请检查是否与 app.py 在同一目录下")
        return None

    # 绘制蓝色页眉
    draw.rectangle([0, 0, width, 80], fill=(24, 144, 255))
    draw.text((30, 20), "贷款申请审批凭证", fill=(255, 255, 255), font=title_font)

    # 准备字段数据
    monthly_pay = calculate_monthly_payment(data['amount'], data['rate'], data['months'])
    fields = [
        ("客户姓名", data['name']),
        ("联系电话", data['phone']),
        ("身份证号", data['id_card']),
        ("贷款总额", f"￥ {data['amount']:,.2f}"),
        ("年化利率", f"{data['rate']}%"),
        ("贷款期限", f"{data['months']} 个月"),
        ("每月还款", f"￥ {monthly_pay:,.2f}"),
        ("当前状态", data['status']),
        ("生成时间", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]

    # 循环绘图
    for i, (label, value) in enumerate(fields):
        curr_y = 120 + i * 50
        # 隔行背景色
        if i % 2 == 0:
            draw.rectangle([20, curr_y-5, width-20, curr_y+35], fill=(240, 242, 245))
        draw.text((50, curr_y), label, fill=(100, 100, 100), font=label_font)
        
        # 状态颜色逻辑
        val_color = (0, 0, 0)
        if label == "当前状态":
            val_color = (82, 196, 26) if "通过" in value else (255, 77, 79)
        draw.text((250, curr_y), str(value), fill=val_color, font=value_font)

    return img

# 3. Streamlit 网页布局
st.set_page_config(page_title="贷款生成器", layout="centered")
st.title("🏦 贷款审批生成系统")

with st.sidebar:
    st.header("⚙️ 请输入信息")
    name = st.text_input("客户姓名", "张三")
    phone = st.text_input("联系电话", "13800000000")
    id_card = st.text_input("身份证号", "440101********0000")
    amount = st.number_input("贷款金额 (元)", value=50000.0)
    rate = st.number_input("年化利率 (%)", value=3.85)
    months = st.selectbox("贷款期限 (月)", [6, 12, 24, 36, 60], index=1)
    status = st.radio("审核状态", ["审核通过 ✅", "审核拒绝 ❌"])

if st.button("🚀 生成凭证图片", type="primary"):
    res = generate_loan_image({"name":name, "phone":phone, "id_card":id_card, "amount":amount, "rate":rate, "months":months, "status":status})
    if res:
        buf = io.BytesIO()
        res.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="预览结果", use_column_width=True)
        st.download_button("💾 下载图片", buf.getvalue(), f"{name}_loan.png", "image/png")