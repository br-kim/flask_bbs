from flask import Flask, render_template, request, session, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from database import db_orm
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
import sqlalchemy

app = Flask(__name__)
app.secret_key = 'test_key'

# Create Databases
engine = sqlalchemy.create_engine("mysql://root:1234@localhost/testdb")
if not database_exists(engine.url):
    create_database(engine.url)

with app.app_context():
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@localhost/testdb"
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
    db_orm.db.init_app(app)
    db_orm.db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_result', methods=['POST'])
def register_result():
    me = db_orm.User_info(request.form['register_id'], request.form['register_pw'])
    db_orm.db.session.add(me)
    result = None
    try:
        db_orm.db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        result = "가입에 실패하셨습니다."
    else:
        result = "%s님 안녕하세요. 가입에 성공하셨습니다." % (request.form['register_id'])
    return render_template('register_result.html', text=result)


@app.route('/login_result', methods=['POST'])
def login_result():
    login_user = db_orm.User_info.query.filter_by(user_id=request.form['login_id']).first()
    result = None
    if login_user is None:
        result = "가입되지 않은 아이디입니다. 가입해주세요."
    else:
        if login_user.user_password == request.form['login_pw']:
            session['login_user'] = login_user.user_id
            result = "로그인 성공"
        else:
            result = "로그인 실패"
    return render_template('login_result.html', text=result)


@app.route(
    '/about')
def about():
    if not session.get('login_user'):
        return redirect(url_for('need_login'))
    else:
        return render_template('about.html')


@app.route('/need_login')
def need_login():
    return render_template('need_login.html')


@app.route('/board')
def board():
    post = db_orm.Article_list.query.filter().all()
    return render_template('board.html', posts=post)


@app.route('/write_article')
def write_article():
    return render_template('write_article.html')


@app.route('/write_article_result', methods=['POST'])
def write_article_result():
    user_id = session['login_user']
    my_article = db_orm.Article_list(user_id, request.form["article_title"], request.form["article_contents"],
                                     datetime.now())
    db_orm.db.session.add(my_article)
    _result = None
    try:
        db_orm.db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        _result = "글 쓰기 실패"
    else:
        _result = "글 쓰기 성공"

    return render_template('write_article_result.html', result=_result)


@app.route('/article/<target_article_number>')
def article(target_article_number):
    _article = db_orm.Article_list.query.filter_by(article_number=target_article_number).first()
    return render_template('article.html', article=_article)


@app.route('/change_article', methods=['POST'])
def change_article():
    article_number = request.form['article_num']
    return render_template('change_article.html', number=article_number)


@app.route('/change_article_result', methods=['POST'])
def change_article_result():
    target_article = db_orm.Article_list.query.filter_by(article_number=request.form['number']).first()
    target_article.article_title = request.form['article_title']
    target_article.article_contents = request.form['article_contents']
    target_article.time = datetime.now()
    try:
        db_orm.db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "글 수정 실패"
    return "글이 수정되었습니다."


@app.route('/delete_article', methods=['POST'])
def delete_article():
    article_number = request.form['article_num']
    return render_template('delete_article.html', number=article_number)


@app.route('/delete', methods=['POST'])
def delete():
    if request.form['what'] == 'article':
        db_orm.Article_list.query.filter_by(article_number=request.form['number']).delete()
        try:
            db_orm.db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print("에러 발생")
        else:
            print("글 삭제")
    elif request.form['what'] == 'comment':
        print("댓글 삭제")
    return "글이 삭제되었습니다."


if __name__ == "__main__":
    app.debug = True
    app.run()
