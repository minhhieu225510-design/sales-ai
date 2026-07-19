import os
import gradio as gr
from groq import Groq
from vieneu import Vieneu
from PIL import Image
from rembg import remove
import requests

# Khởi tạo Client Groq (Sẽ lấy Key từ biến môi trường trên Render)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Khởi tạo TTS
tts = Vieneu()
voice_choices = [desc for desc, _ in tts.list_preset_voices()]
voice_map = {desc: name for desc, name in tts.list_preset_voices()}

# Hàm xử lý Content bằng Groq API
def generate_content(prod_name, prod_info, mode_genz):
    trend_prompt = "Dùng từ lóng trend (đỉnh nóc, kịch trần, over hợp...)" if mode_genz else ""
    prompt = f"Viết content bán hàng cho sản phẩm: {prod_name}. Thông tin: {prod_info}. {trend_prompt}. Trả về cấu trúc: ---FACEBOOK---, ---SHOPEE_LAZADA---, ---TIKTOK_SCRIPT---, ---SEEDING---"
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    raw_text = completion.choices[0].message.content
    
    return raw_text.split("---FACEBOOK---")[-1].split("---SHOPEE_LAZADA---")[0].strip(), \
           raw_text.split("---SHOPEE_LAZADA---")[-1].split("---TIKTOK_SCRIPT---")[0].strip(), \
           raw_text.split("---TIKTOK_SCRIPT---")[-1].split("---SEEDING---")[0].strip(), \
           raw_text.split("---SEEDING---")[-1].strip()

# Hàm TTS
def text_to_speech(tiktok_text, voice_desc):
    if not tiktok_text.strip(): return None
    voice_id = voice_map.get(voice_desc)
    voice_data = tts.get_preset_voice(voice_id) if voice_id else None
    audio_spec = tts.infer(text=tiktok_text, voice=voice_data)
    output_audio_path = "tiktok_voiceover.wav"
    tts.save(audio_spec, output_audio_path)
    return output_audio_path

# Giao diện
with gr.Blocks(title="AI Sales Studio") as demo:
    gr.Markdown("# 🚀 AI Sales Studio (Cloud Ready)")
    with gr.Row():
        with gr.Column():
            prod_name = gr.Textbox(label="Tên sản phẩm")
            prod_info = gr.Textbox(label="Mô tả", lines=4)
            mode_genz = gr.Checkbox(label="Chế độ Gen Z")
            btn_run = gr.Button("KÍCH HOẠT AI")
        with gr.Column():
            out_fb = gr.Textbox(label="Facebook")
            out_sp = gr.Textbox(label="Shopee")
            out_tk = gr.Textbox(label="TikTok Script")
            out_sd = gr.Textbox(label="Seeding")

    btn_run.click(generate_content, inputs=[prod_name, prod_info, mode_genz], outputs=[out_fb, out_sp, out_tk, out_sd])

# Cấu hình cổng cho Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)