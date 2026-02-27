from fastapi import FastAPI, Request, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/set_cookie")
def set_cookie(request: Request):
    response = templates.TemplateResponse("set_cookie.html", {"request": request})
    #htttp 요청으로만 쿠키 확인(웹브라우저 주소창에 javascript:document.cookie 입력하여 확인)
    response.set_cookie("id", "Lee", httponly=True, max_age=3600)
    return response


@app.get("/read_cookie", response_class=HTMLResponse)
def read_cookie(request: Request):
    return templates.TemplateResponse("read_cookie.html", {"request": request})


@app.get("/del_cookie", response_class=HTMLResponse)
def del_cookie(request: Request):
    response = templates.TemplateResponse("del_cookie.html", {"request": request})
    response.delete_cookie("id")
    return response


@app.get("/change_cookie", response_class=HTMLResponse)
def change_cookie(request: Request):
    response = templates.TemplateResponse("change_cookie.html", {"request": request})
    response.set_cookie("id", "Song", httponly=True, max_age=3600)
    return response


@app.get("/counter", response_class=HTMLResponse)
def counter(request: Request, visits: Optional[str]=Cookie(None), last_visit: Optional[str]=Cookie(None)):
    now = datetime.now()
    str_now = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        int_visit = int(visits) + 1 if visits else 1
    except:
        int_visit = 1

    str_visits = str(int_visit)
    result = [f"{char}.gif" for char in str_visits]

    response = templates.TemplateResponse("counter.html", {"request": request, "result": result, "last_visit": last_visit})
    response.set_cookie("visits", str_visits)
    response.set_cookie("last_visit", str_now)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)