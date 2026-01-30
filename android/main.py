from fastapi import FastAPI, UploadFile, File
from diffusers import StableDiffusionImg2ImgPipeline
import torch
from io import BytesIO
from PIL import Image



app = FastAPI()

from fastapi.staticfiles import StaticFiles
import os

# 'outputs'라는 폴더를 만들고, 외부에서 접속 가능하게 설정
if not os.path.exists("outputs"):
    os.makedirs("outputs")

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# 1. AI 모델 불러오기 (컴퓨터 사양에 따라 시간이 걸릴 수 있어요)
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "runwayml/stable-diffusion-v1-5"

# 이미지를 이미지로 변형하는(Img2Img) 파이프라인 설정
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id,
                                                      torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe = pipe.to(device)


@app.post("/generate-game")
async def generate_game(file: UploadFile = File(...)):
    # 2. 휴대폰에서 보낸 원본 사진 받기
    content = await file.read()
    init_image = Image.open(BytesIO(content)).convert("RGB")
    init_image = init_image.resize((512, 512))  # AI가 처리하기 좋은 크기로 변경

    # 3. AI에게 "이 사진을 살짝만 바꿔줘!"라고 요청 (틀린 그림 찾기용)
    # strength가 높을수록 원본과 많이 달라집니다.
    prompt = "high quality, subtle changes, photorealistic"  #strength 강도(난이도)
    result = pipe(prompt=prompt, image=init_image, strength=0.3, guidance_scale=7.5).images[0]

    # 4. 결과 이미지 저장 및 확인 (나중에는 휴대폰으로 전송합니다)
    result.save("game_image.png")

    return {"status": "success", "message": "게임 이미지가 생성되었습니다!"}

    # ... 이전 AI 생성 코드 ...
    file_name = "game_1.png"
    file_path = f"outputs/{file_name}"
    result.save(file_path)  # 결과 이미지를 outputs 폴더에 저장

    # 내 컴퓨터 IP 주소를 포함한 이미지 다운로드 주소 생성
    image_url = f"http://YOUR_IP_ADDRESS:8000/outputs/{file_name}"

    return {"status": "success", "image_url": image_url}