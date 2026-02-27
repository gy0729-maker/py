from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import oracledb
import Employee

app = FastAPI()

conn = oracledb.connect(user="python", password='1234', dsn='localhost/XE')

templates = Jinja2Templates(directory="templates")


@app.get("/")
def list(request: Request):
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department, hire_date FROM employee ORDER BY id')
    rows = cursor.fetchall()
    cursor.close()

    employees = []
    for row in rows:
        employees.append(Employee.Employee(id=row[0], name=row[1], department=row[2], hire_date=row[3]))

    return templates.TemplateResponse('list.html', {'request': request, 'employees': employees})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000, reload=False)