import os
from dotenv import load_dotenv
import openai
from PIL import Image, ImageDraw

# 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = "openai"

# 이미지 불러오기 및 리사이즈
original_image = Image.open("1.png").convert("RGB").resize((1024, 1024))
mask_image = Image.new("RGB", original_image.size, (0, 0, 0))
draw = ImageDraw.Draw(mask_image)

# 마스킹 영역 (대충 좌표 수정)
draw.polygon([(1188, 791), (1282, 791), (1284, 937), (1189, 936)], fill=(255, 255, 255))
draw.polygon([(1323, 792), (1417, 793), (1420, 938), (1325, 938)], fill=(255, 255, 255))

# 저장
original_image.save("input_image.png")
mask_image.save("mask_image.png")

# API 호출
with open("input_image.png", "rb") as image_file, open("mask_image.png", "rb") as mask_file:
    response = openai.images.edit(
        image=image_file,
        mask=mask_file,
        prompt=(
            "This is a Korean restaurant poster. "
            "Please change the word '보' to '볶' and '끔' to '음'. "
            "Preserve the original style, font, and layout."
        ),
        n=1,
        size="1024x1024"
    )

# 결과 확인
print("URL:", response["data"][0]["url"])