from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import oracledb
import uvicorn

app=FastAPI()
templates = Jinja2Templates(directory="templates")



def get_conn():
    return oracledb.connect(user='python', password='1234', dsn='localhost:1521/XE')



@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('select id, product, qty, price from sales order by id')
    rows = cursor.fetchall()

    sales_list = []
    total_sum = 0

    for row in rows:
        amount = row[2] * row[3]
        total_sum += amount
        sales_list.append({'id':row[0], 'product':row[1], 'qty':row[2], 'price':row[3], 'amount':amount})

    cursor.close()
    conn.close()

    return templates.TemplateResponse('index.html', {'request':request, 'sales':sales_list, 'total_sum':total_sum})



@app.post('/add')
def add(product: str = Form(...), qty: int = Form(...), price: int = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('insert into sales(product, qty, price) values (:1, :2, :3)', (product, qty, price))
    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse('/', status_code=303)


@app.post('/update')
def update(id: int = Form(...), product: str = Form(...), qty: int = Form(...), price: int = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "update sales set product = :1, qty = :2, price = :3 where id= :4"
    cursor.execute(sql, (product, qty, price, id))

    conn.commit()
    conn.close()
    return RedirectResponse('/', status_code=303)


@app.post('/delete')
def delete(id: int = Form(...)):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "delete from sales where id = :1"
    cursor.execute(sql, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse('/', status_code=303)



if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=8000, reload=False)

