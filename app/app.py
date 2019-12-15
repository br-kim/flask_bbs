from flask import Flask, render_template, request, session, redirect, url_for
from database import bbs_dao
from flask_sqlalchemy import SQLAlchemy
from database import db_orm
import sqlalchemy

app = Flask(__name__)
app.secret_key = 'testkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@localhost/testdb"
db_orm.db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/dbtest')
def dbtest():
    dbdata = bbs_dao.get_dbexam()
    return render_template('dbtest.html',db_data = dbdata)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_result',methods=['POST'])
def register_result():
    me = db_orm.User_info(request.form['register_id'],request.form['register_pw'])
    db_orm.db.session.add(me)
    result = None
    try :
        db_orm.db.session.commit()
    except sqlalchemy.exc.IntegrityError : 
        result = "가입에 실패하셨습니다."
    else : 
        result = "%s님 안녕하세요. 가입에 성공하셨습니다."%(request.form['register_id'])
    return render_template('register_result.html',text=result)

@app.route('/login_result',methods=['POST'])
def login_result():
    login_user = db_orm.User_info.query.filter_by(user_id=request.form['login_id']).first()
    result = None
    if login_user is None :
        result = "가입되지 않은 아이디입니다. 가입해주세요."
    else :
        if login_user.user_password == request.form['login_pw'] :
            session['login_user'] = login_user.user_id
            result = "로그인 성공"
        else :
            result = "로그인 실패"
    return render_template('login_result.html',text=result)

@app.route('/about')
def about():
    return redirect(url_for('need_login')) if not session.get('login_user') else None
    return "로그인 됨. %s "%session.get('login_user')#render_template('about.html')

@app.route('/need_login')
def need_login():
    return render_template('need_login.html')

@app.route('/board')
def board():
    post = db_orm.Article_list.query.filter().all()
    return render_template('board.html',posts=post)

if __name__=="__main__":
    app.run()