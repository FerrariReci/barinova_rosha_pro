import os
from flask import Flask, render_template, redirect, request, flash
from data import db_session
from data.users import User
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.login import LoginForm
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = '!'
MAX_CONTENT_LENGTH = 1024 * 1024
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = './static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def check_password(password):
    password = str(password)
    if len(password) < 8:
        return 'Пароль должен содержать не менее 8 символов'
    numb = False
    lett = False
    up_lett = False
    for w in password:
        if w.isdigit():
            numb = True
        elif w.isalpha():
            lett = True
            if w.upper() == w:
                up_lett = True
    if numb is False:
        return 'В пароле должны присутствовать цифры'
    if lett is False:
        return 'В пароле должны присутствовать строчные буквы'
    if up_lett is False:
        return 'В пароле должны прописные буквы'
    return 'True'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        password = form.password.data
        response = check_password(password)
        if response != 'True':
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message=response.capitalize())
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Аккаунт с этой почтой уже существует")
        user = User()
        user.username = form.username.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.avatar = '/static/img/profile.jpg'
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file.filename[-3:] in ('jpg', 'JPG', 'PNG', 'png'):
                filename = secure_filename(file.filename)
                s = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(s)
                now_id = current_user.id
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.id == now_id).first()
                user.avatar = UPLOAD_FOLDER + filename
                db_sess.commit()
            else:
                return redirect("/profile")
        except Exception:
            return redirect("/profile")
    return redirect("/profile")


@app.route("/profile")
def profile():
    return render_template("profile.html")


def main():
    db_session.global_init("db/users.db")
    app.run()


if __name__ == '__main__':
    main()