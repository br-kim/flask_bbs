import pymysql
import datetime
from database import connection

def get_dbexam():
    conn = connection.get_connection()
    curs = conn.cursor()
    sql = "select * from emp"
    curs.execute(sql)
    rows= curs.fetchall()
    # print('EMPNO ENAME JOB MGR HIREDATE SAL COMM DEPTNO')
    # for row in rows:
    #     print(row['EMPNO'],row['ENAME'],row['JOB'],row['MGR'],row['HIREDATE'],row['SAL'],row['COMM'],row['DEPTNO'])
    conn.close()
    return rows