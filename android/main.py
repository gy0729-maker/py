from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import cv2
import numpy as np
import random

app = FastAPI()

if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 서버 상태를 저장할 변수들
current_image = ""
current_mod_image = ""
answer_coords = {"x": 0.0, "y": 0.0}


@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    global current_image, current_mod_image, answer_coords

    file_name = image.filename
    file_path = f"uploads/{file_name}"
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    # OpenCV 변형 작업
    img = cv2.imread(file_path)
    h, w, _ = img.shape

    # 랜덤 정답 생성
    ans_x = random.randint(int(w * 0.1), int(w * 0.9))
    ans_y = random.randint(int(h * 0.1), int(h * 0.9))
    size = 150

    mask = np.zeros((h, w), np.uint8)
    cv2.rectangle(mask, (ans_x - size, ans_y - size), (ans_x + size, ans_y + size), 255, -1)
    modified_img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    # 변형 이미지 저장 (이름 규칙: mod_파일이름)
    mod_file_name = file_name.replace(".jpg", "_mod.jpg")
    mod_file_path = f"uploads/{mod_file_name}"
    cv2.imwrite(mod_file_path, modified_img)

    # 데이터 업데이트
    current_image = file_name
    current_mod_image = mod_file_name
    answer_coords = {"x": ans_x / w, "y": ans_y / h}

    return {"message": "AI 변형 완료!", "filename": file_name}


@app.get("/game")
def get_game_data():
    global current_image, current_mod_image, answer_coords

    # 본인 컴퓨터 IP 확인 필수! (192.168.0.186 가 맞는지 확인하세요)
    base_url = "http://192.168.0.186:8000/uploads/"

    if not current_image:
        return {
            "image_url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
            "mod_image_url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
            "answer_x": 0.5,
            "answer_y": 0.5,
            "message": "사진을 먼저 업로드해주세요!"
        }

    return {
        "image_url": base_url + current_image,
        "mod_image_url": base_url + current_mod_image,  # 변형된 이미지 주소 추가
        "answer_x": answer_coords["x"],
        "answer_y": answer_coords["y"],
        "message": "틀린 곳을 찾아보세요!"
    }