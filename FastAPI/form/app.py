from fastapi import FastAPI, Request
from typing import List, Optional
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    msg = "welcome"
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg})


@app.get("/hello", response_class=HTMLResponse)
def hello(request: Request):
    msg = "test django"
    return templates.TemplateResponse("test.html", {"request": request, "msg": msg})


@app.get("/now", response_class=HTMLResponse)
def now(request: Request):
    date = datetime.datetime.now()
    today = f"{date.year}-{date.month:02d}-{date.day:02d} {date.hour:02d}:{date.minute:02d}:{date.second:02d}"
    return templates.TemplateResponse("now.html", {"request": request, "today": today})


@app.get("/array", response_class=HTMLResponse)
def array(request: Request):
    items = ["apple", "peach", "grapes", "orange"]
    return templates.TemplateResponse("array.html", {"request": request, "items": items})


@app.get("/age", response_class=HTMLResponse)
def age(request: Request):
    return templates.TemplateResponse("age.html", {"request": request})

@app.post("/age", response_class=HTMLResponse)
def age_result(request: Request, name: str = Form(...), year: int = Form(...)):
    current_year = datetime.now().year
    age = current_year - year
    return templates.TemplateResponse("age_result.html", {"request": request, "name": name, "year": year, "age": age})


@app.get("/mysum", response_class=HTMLResponse)
def mysum_form(request: Request):
    return templates.TemplateResponse("mysum.html", {"request": request})

@app.post("/mysum", response_class=HTMLResponse)
def mysum_result(request: Request, num: int = Form(...)):
    result = sum(range(1, num + 1))
    sum1 = sum(i for i in range(1, num+1) if i % 2 == 0)
    sum2 = sum(i for i in range(1, num+1) if i % 2 != 0)
    return templates.TemplateResponse("mysum_result.html", {"request": request, "num": num, "result": result, "sum1": sum1, "sum2": sum2})


@app.get("/radio", response_class=HTMLResponse)
def radio_form(request: Request):
    return templates.TemplateResponse("radio.html", {"request": request})

@app.post("/radio", response_class=HTMLResponse)
def radio_result(request: Request, name: str = Form(...), gender: str = Form(...)):
    gender_text = "남성" if gender == "male" else "여성"
    return templates.TemplateResponse("radio_result.html", {"request": request, "name": name, "gender": gender_text})


@app.get("/checkbox", response_class=HTMLResponse)
def checkbox_form(request: Request):
    return templates.TemplateResponse("checkbox.html", {"request": request})

@app.post("/checkbox", response_class=HTMLResponse)
def checkbox_result(request: Request, fruits: List[str] = Form(default=[])):
    return templates.TemplateResponse("checkbox_result.html", {"request": request, "fruits": fruits})


@app.get("/button", response_class=HTMLResponse)
def button_form(request: Request):
    return templates.TemplateResponse("button.html", {"request": request})

@app.post("/button", response_class=HTMLResponse)
def button_result(request: Request, price: int = Form(...), amount: int = Form(...)):
    money = price * amount
    return templates.TemplateResponse("button_result.html", {"request": request, "price": price, "amount": amount, "money": money})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)