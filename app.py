import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# Không import PIL, không import rembg để tiết kiệm RAM tối đa
import gradio as gr
from groq import Groq
import requests

# Khởi tạo Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_content(prod_name, prod_info, mode_genz):
    trend_prompt = "Dùng từ lóng trend" if mode_genz else ""
    prompt = f"Viết content bán hàng cho sản phẩm: {prod_name}. Thông tin: {prod_info}. {trend_prompt}. Trả về cấu trúc: ---FACEBOOK---, ---SHOPEE_LAZADA---, ---TIKTOK_SCRIPT---, ---SEEDING---"
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        raw_text = completion.choices[0].message.content
        return raw_text.split("---FACEBOOK---")[-1].split("---SHOPEE_LAZADA---")[0].strip(), \
               raw_text.split("---SHOPEE_LAZADA---")[-1].split("---TIKTOK_SCRIPT---")[0].strip(), \
               raw_text.split("---TIKTOK_SCRIPT---")[-1].split("---SEEDING---")[0].strip(), \
               raw_text.split("---SEEDING---")[-1].strip()
    except:
        return "Lỗi API", "", "", ""

with gr.Blocks() as demo:
    gr.Markdown("# AI Sales Studio")
    prod_name = gr.Textbox(label="Tên sản phẩm")
    prod_info = gr.Textbox(label="Mô tả", lines=2)
    mode_genz = gr.Checkbox(label="Chế độ Gen Z")
    btn_run = gr.Button("KÍCH HOẠT")
    out_fb = gr.Textbox(label="Facebook")
    btn_run.click(generate_content, inputs=[prod_name, prod_info, mode_genz], outputs=[out_fb])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
