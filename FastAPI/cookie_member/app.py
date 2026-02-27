from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import oracledb
import uvicorn
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_conn():
    return oracledb.connect(user="python", password="1234", dsn="localhost:1521/xe")


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, userid: str = Form(...), password: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "select userid, username from users where userid = :1 and password = standard_hash(:2, 'SHA256')"
    cursor.execute(sql, (userid, password))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return templates.TemplateResponse("login.html", {"request": request, "error": "아이디 또는 비밀번호가 올바르지 않습니다."})

    userid_db = row[0]

    cursor.execute("update users set last_login_at = sysdate where userid = :1", (userid_db,))

    client_ip = request.client.host
    cursor.execute("insert into login_history (userid, client_ip) values (:1, :2)", (userid_db, client_ip))

    conn.commit()
    cursor.close()
    conn.close()

    response = RedirectResponse(url="/main", status_code=302)
    response.set_cookie(key="userid", value=userid_db, httponly=True)
    return response


@app.get("/main", response_class=HTMLResponse)
def main(request: Request, userid: Optional[str] = Cookie(None)):
    if not userid:
        return RedirectResponse(url="/")

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("select username from users where userid = :1", (userid,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return RedirectResponse(url="/")

    username = row[0]

    return templates.TemplateResponse("main.html", {"request": request, "username": username, "userid": userid})


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("userid")
    return response


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(request: Request, userid: str = Form(...), password: str = Form(...), username: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("select count(*) from users where userid = :1", (userid,))
    count = cursor.fetchone()[0]

    if count > 0 :
        cursor.close()
        conn.close()
        return templates.TemplateResponse("register.html", {"request": request, "error": "이미 존재하는 아이디입니다."})

    cursor.execute("insert into users (userid, password, username) values (:1, standard_hash(:2, 'SHA256'), :3)", (userid, password, username))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/", status_code=302)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)