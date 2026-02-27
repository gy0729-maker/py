from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

app = FastAPI()             #안쓰면 기본 templates, 변경가능
templates = Jinja2Templates(directory='templates')

#문장을 단어/형태소로 분리
tokenizer = PreTrainedTokenizerFast.from_pretrained('skt/kogpt2-base-v2')
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')  #미리 학습된 모델
model.eval() #평가모드(순전파만)


@app.get("/", response_class=HTMLResponse)
async def read_input(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})


@app.post('/generate', response_class=HTMLResponse)
async def generate_story(request: Request, prompt: str = Form(...)):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')  #프롬포트를 토큰화 인코드
    output = model.generate(
        input_ids,
        max_length=80,
        temperature=0.9,
        top_k=60,
        top_p=0.95,
        do_sample=True,
        no_repeat_ngram_size=2
    )
    story = tokenizer.decode(output[0], skip_special_tokens=True)  #토큰화된걸 다시 아웃풋형태로 디코드

    sentences = story.replace('\n', ' ').split('. ')
    short_sentences = [s.strip() for s in sentences if 3 < len(s) <=50]
    final_story = '. '.join(short_sentences)
    if not final_story.endswith('.'):
        final_story += '.'

    return templates.TemplateResponse('result.html', {
        'request': request,
        'prompt': prompt,
        'story': final_story
    })


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='127.0.0.1', port=5000, reload=True)