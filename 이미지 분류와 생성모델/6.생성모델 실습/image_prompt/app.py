from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse, FileResponse, JSONResponse)
from fastapi.templating import Jinja2Templates
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os
import threading
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

os.makedirs('outputs', exist_ok=True)

pipe = StableDiffusionPipeline.from_pretrained(
    'runwayml/stable-diffusion-v1-5',
    torch_dtype=torch.float32)

#작업 상태 저장
tasks = {} #task_id -> {status, image, prompt}

#입력 페이지
@app.get('/', response_class=HTMLResponse)
def input_page(request: Request):
                #변수명 : 자료형
    return templates.TemplateResponse(
        'input.html',
        {'request': request}
    )

#이미지 생성 시작(async:비동기-여러작업 한번에) / 동기-순서대로 한번의 하나의 작업 수행
@app.post('/start')
async def start_generate(request: Request):
    form = await request.form()
    prompt = form.get('prompt')
            #uuid:식별자
    task_id = uuid.uuid4().hex
    tasks[task_id] = {'status': 'running'}

    thread = threading.Thread(
        target=generate_image,
        args=(task_id, prompt),
        daemon=True
    )
    thread.start() #백그라운드에서 실행
        #JavaScript Object Notation 자바스크림트 객체 표기법(=딕셔너리)
    return JSONResponse({'task_id': task_id})

def generate_image(task_id: str, prompt: str):
    image = pipe(
        prompt,
        num_inferene_steps=10
    ).images[0]

    filename = f'{task_id}.png'
    filepath = os.path.join('outputs', filename)
    image.save(filepath)

    tasks[task_id]['status'] = 'done'
    tasks[task_id]['image'] = filename
    tasks[task_id]['prompt'] = prompt


#진행 상태 확인
@app.get('/status/{task_id}')
def check_status(task_id: str):
    return tasks.get(task_id, {'status': 'unknown'})

#결과 페이지
@app.get('/result/{task_id}', response_class=HTMLResponse)
def result_page(request: Request, task_id: str):
    task = tasks.get(task_id)

    return templates.TemplateResponse(
        'result.html',
        {
            'request': request,
            'prompt': task['prompt'],
            'image_path': f'/image/{task['image']}'
        }
    )

#이미지 제공
@app.get('/image/{filename}')
def get_image(filename: str):
    return FileResponse(
        path=os.path.join('outputs', filename),
        media_type='image/png'
    )


#main실행부 (Fast api -> cmd에서 uvicorn으로 구동)
if __name__ == '__main__':
    uvicorn.run(
        app,
        host='127.0.0.1',
        port=5000,
        #log-level= debug/info/
        log_level='info'
    )