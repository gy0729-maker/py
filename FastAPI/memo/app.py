from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import oracledb
import Memo


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_conn():
    return oracledb.connect(user="python", password="1234", dsn="localhost:1521/XE")



@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
def list_memo(request: Request):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "select idx, writer, memo, post_date from memo order by idx desc"
    cursor.execute(sql)

    memoList = []

    for row in cursor:
        memo_obj = Memo.Memo(row[0], row[1], row[2], row[3])
        memoList.append(memo_obj)

    cursor.close()
    conn.close()

    return templates.TemplateResponse("list.html", {"request": request, "memoList": memoList})


@app.post("/insert_memo")
def insert_memo(writer: str = Form(...), memo: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "insert into memo (writer, memo) values (:1, :2)"
    cursor.execute(sql, (writer, memo))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse("/")


@app.get("/detail", response_class=HTMLResponse)
def detail(request: Request, idx: int):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "select idx, writer, memo, post_date from memo where idx=:1"
    cursor.execute(sql, (idx,))

    row = cursor.fetchone()

    memo_obj = None
    if row:
        memo_obj = Memo.Memo(row[0], row[1], row[2], row[3])

    cursor.close()
    conn.close()

    return templates.TemplateResponse("detail.html", {"request": request, "row": memo_obj})


@app.post("/update_memo")
def update_memo(idx: int = Form(...), writer: str = Form(...), memo: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "update memo set writer = :1, memo = :2 where idx = :3"
    cursor.execute(sql, (writer, memo, idx))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse("/")


@app.post('/delete')
def delete(idx: int = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "delete from memo where idx= :1"
    cursor.execute(sql, (idx,))

    conn.commit()
    conn.close()
    return RedirectResponse('/', status_code=303)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)