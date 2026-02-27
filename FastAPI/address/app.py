from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import oracledb

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_conn():
    return oracledb.connect(
        user='python',
        password='1234',
        dsn='localhost:1521/XE'
    )


@app.get('/', response_class=HTMLResponse)
def list_page(request: Request):
    conn = get_conn()
    cursor = conn.cursor()

    sql = 'SELECT * FROM address ORDER BY idx DESC'
    cursor.execute(sql)

    columns = [col[0].lower() for col in cursor.description]
    items = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()
    return templates.TemplateResponse('list.html', {'request': request, 'items': items})

@app.get('/write', response_class=HTMLResponse)
def write_page(request: Request):
    return templates.TemplateResponse('write.html', {'request': request})


@app.post('/insert')
def insert(name: str = Form(...), tel: str = Form(...), email: str = Form(...), address: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "insert into address (name, tel, email, address) values (:1, :2, :3, :4)"
    cursor.execute(sql, (name, tel, email, address))

    conn.commit()
    conn.close()
    return RedirectResponse('/', status_code=303)


@app.get('/detail', response_class=HTMLResponse)
def detail(request: Request, idx: int):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "select * from address where idx=:1"
    cursor.execute(sql, (idx,))

    row = cursor.fetchone()
    columns = [col[0].lower() for col in cursor.description]
    addr = dict(zip(columns, row)) if row else None

    conn.close()
    return templates.TemplateResponse('detail.html', {'request': request, 'addr': addr})


@app.post('/update')
def update(idx: int = Form(...), name: str = Form(...), tel: str = Form(...), email: str = Form(...), address: str = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "update address set name = :1, tel = :2, email = :3, address = :4 where idx= :5"
    cursor.execute(sql, (name, tel, email, address, idx))

    conn.commit()
    conn.close()
    return RedirectResponse('/', status_code=303)


@app.post('/delete')
def delete(idx: int = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "delete from address where idx= :1"
    cursor.execute(sql, (idx,))

    conn.commit()
    conn.close()
    return RedirectResponse('/', status_code=303)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=False)