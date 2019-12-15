import pymysql

def get_connection():
    conn = pymysql.connect(host='localhost',
    user='root',
    password ='1234',
    db='testdb',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
    )
    return conn