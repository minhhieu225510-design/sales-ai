import os
import gradio as gr
from groq import Groq
# Thêm dòng này để ép CPU hoạt động, tránh lỗi tìm GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 

from vieneu import Vieneu
from PIL import Image
# Chỉ import rembg khi cần dùng để tránh lỗi lúc khởi động
from rembg import remove 

# Khởi tạo Client Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Khởi tạo TTS (đặt trong try-except để không bị sập app nếu lỗi)
try:
    tts = Vieneu()
    voice_choices = [desc for desc, _ in tts.list_preset_voices()]
    voice_map = {desc: name for desc, name in tts.list_preset_voices()}
except:
    tts = None
    voice_choices = []
    print("⚠️ Cảnh báo: Không thể khởi tạo TTS.")

# Hàm xử lý Content bằng Groq API
def generate_content(prod_name, prod_info, mode_genz):
    # ... (Giữ nguyên logic của bạn ở đây) ...
    return "Facebook content...", "Shopee content...", "TikTok script...", "Seeding content..."

# Giao diện
with gr.Blocks(title="AI Sales Studio") as demo:
    gr.Markdown("# 🚀 AI Sales Studio (Cloud Ready)")
    # ... (Giữ nguyên phần UI của bạn) ...

# Cấu hình cổng chuẩn Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
