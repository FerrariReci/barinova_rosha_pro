import os
from _datetime import datetime
from flask import url_for, Flask, render_template, redirect, request, flash
from data import db_session
from data.users import User
from data.index import Index
from data.category import Category
from data.user_competitions import User_competitions
from data.competition import Competition
from forms.user import RegisterForm
from forms.new_info import InfoForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.login import LoginForm
from forms.new_event import EventForm
from werkzeug.utils import secure_filename
from flask import send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = './static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def age(birthdate_str, date_format='%Y-%m-%d'):
    birthdate = datetime.strptime(str(birthdate_str), date_format)
    return (datetime.now() - birthdate).days // 365


def all_categories(line, g):
    arr = [int(x.strip()) for x in line.split(',')]
    db_sess = db_session.create_session()
    list_categories = []
    for a in arr:
        cat = db_sess.query(Category).filter(Category.id == a).first()
        gender = cat.gender
        if str(g) in str(gender):
            list_categories.append(cat)
    return list_categories


def all_distances(line):
    list_dist = [float(x.strip()) for x in line.split(',')]
    return list_dist


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
    db_sess = db_session.create_session()
    new_info = db_sess.query(Index).first()
    return render_template("index.html", title='Главная', info=new_info)


@app.route("/events")
def events():
    db_sess = db_session.create_session()
    events = db_sess.query(Competition).filter(Competition.status == 1).order_by(
        Competition.date).all()
    return render_template("events.html", title='События', events=events)


@app.route("/results")
def results():
    db_sess = db_session.create_session()
    events = db_sess.query(Competition).filter(Competition.status == 0).order_by(
        Competition.date).all()
    return render_template("new_res.html", title='Результаты', events=events)


@app.route('/events/<int:id>', methods=['GET', 'POST'])
@login_required
def new_event(id):
    db_sess = db_session.create_session()
    now_id = current_user.id
    ev = db_sess.query(User_competitions.type).filter(User_competitions.user_id == now_id).all()
    comp = db_sess.query(Competition).filter(Competition.id == id).first()
    g = current_user.gender
    cat = comp.categories
    dist = comp.distances
    categories = all_categories(cat, g)
    distances = all_distances(dist)
    category = request.form.get('category')
    distance = request.form.get('distance')
    if str(category) == 'None' or str(distance) == 'None':
        if str(category) == 'None':
            mess = "Выберите категорию"
        else:
            mess = "Выберите дистанцию"
        return render_template("reg_for_comp.html", title='Запись на соревнование', comp=comp,
                               categories=categories, distances=distances, message=mess)
    if (id, ) not in ev:
        new_comp = User_competitions()
        new_comp.user_id = now_id
        new_comp.type = id
        new_comp.category = category
        new_comp.distance = distance
        db_sess.add(new_comp)
        db_sess.commit()
        events = db_sess.query(Competition).filter(Competition.status == 1).order_by(
            Competition.date).all()
        return render_template("events.html", title='События', events=events)
    events = db_sess.query(Competition).filter(Competition.status == 1).order_by(
        Competition.date).all()
    comp = db_sess.query(Competition.name).filter(Competition.id == id).first()
    return render_template("events.html", title='События', events=events,
                           message=f'Вы уже записаны на "{comp[0]}"')


@app.route('/save/<int:id>', methods=['GET', 'POST'])
@login_required
def save(id):
    db_sess = db_session.create_session()
    event = db_sess.query(User_competitions).filter(User_competitions.type == id).all()
    arr = []
    for e in event:
        user = db_sess.query(User).filter(User.id == e.user_id).first()
        cat = db_sess.query(Category).filter(Category.id == e.category).first()
        dist = e.distance
        arr.append((user, cat.name, dist))
    filename = './static/users_docs/list_of_users.txt'
    name = db_sess.query(Competition).filter(Competition.id == id).first()
    name = name.name
    with open(filename, 'w', encoding='utf-8') as f:
        s = f'Список участников "{name}"' + '\n' + 'Имя, фамилия - пол, возраст, категория,' \
                                                   ' дистанция' + '\n'
        for user in arr:
            if user[0].gender == 1:
                g = 'ж'
            else:
                g = 'м'
            user_age = age(user[0].age)

            s += user[0].username + ' ' + user[0].surname + ' - ' + g + ', ' + str(user_age) \
                 + ', ' + str(user[1]) + ', ' + str(user[2]) + 'км' + '\n'
        f.write(s)
    return send_file(filename, as_attachment=True)


@app.route('/events/del/<int:id>', methods=['GET', 'POST'])
@login_required
def del_event(id):
    db_sess = db_session.create_session()
    now_id = current_user.id
    event = db_sess.query(User_competitions).filter(User_competitions.type == id,
                                                    User_competitions.user_id == now_id).first()
    db_sess.delete(event)
    db_sess.commit()
    return redirect('/profile')


@app.route('/reg_for_comp/<int:id>', methods=['GET', 'POST'])
@login_required
def show(id):
    db_sess = db_session.create_session()
    comp = db_sess.query(Competition).filter(Competition.id == id).first()
    g = current_user.gender
    cat = comp.categories
    dist = comp.distances
    categories = all_categories(cat, g)
    distances = all_distances(dist)
    return render_template("reg_for_comp.html", title='Запись на соревнование', comp=comp,
                           categories=categories, distances=distances)


@app.route('/del_events/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    db_sess = db_session.create_session()
    events = db_sess.query(User_competitions).filter(User_competitions.type == id).all()
    for e in events:
        db_sess.delete(e)
    db_sess.commit()
    comp = db_sess.query(Competition).filter(Competition.id == id).first()
    st = comp.status
    db_sess.delete(comp)
    db_sess.commit()
    if st == 0:
        return redirect('/results')
    return redirect('/events')


@app.route('/last_events/<int:id>', methods=['GET', 'POST'])
@login_required
def last_event(id):
    db_sess = db_session.create_session()
    events = db_sess.query(User_competitions).filter(User_competitions.type == id).all()
    for e in events:
        db_sess.delete(e)
    db_sess.commit()
    comp = db_sess.query(Competition).filter(Competition.id == id).first()
    comp.status = 0
    db_sess.commit()
    return redirect('/events')


@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        name = form.name.data
        comp = Competition()
        comp.name = name
        comp.status = 1
        comp.date = form.date_time.data
        comp.place = form.place.data
        comp.photo = '-'
        comp.description = form.text.data
        db_sess.add(comp)
        db_sess.commit()
        return redirect('/events')
    return render_template('new_event.html', title='События', form=form)


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
        user.age = form.age.data
        user.email = form.email.data
        user.gender = form.gender.data
        user.status = 0
        user.avatar = '/static/img/profile.jpg'
        user.docs = '-'
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


@app.route('/upload_file', methods=["POST", "GET"])
@login_required
def upload_file():
    if request.method == 'POST':
        try:
            folder = './static/users_docs/'
            file = request.files['file']
            if file.filename[-3:] in ('jpg', 'JPG', 'PNG', 'png', 'pdf', "PDF"):
                now_id = current_user.id
                filename = str(now_id) + '_doc.' + file.filename[-3:]
                s = os.path.join(folder, filename)
                file.save(s)
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.id == now_id).first()
                user.docs = folder + filename
                db_sess.commit()
            else:
                return redirect("/profile")
        except Exception:
            return redirect("/profile")
    return redirect("/profile")


@app.route('/download')
def download():
    filename = current_user.docs
    return send_file(filename, as_attachment=True)


@app.route('/download_res/<int:id>')
def download_res(id):
    db_sess = db_session.create_session()
    comp = db_sess.query(Competition).filter(Competition.id == id).first()
    filename = comp.res
    return send_file(filename, as_attachment=True)


@app.route("/profile")
def profile():
    db_sess = db_session.create_session()
    now_id = current_user.id
    u_s = db_sess.query(User_competitions).filter(User_competitions.user_id == now_id).all()
    return render_template("profile.html", competitions=u_s, title='Мой профиль')


@app.route("/new_info", methods=['GET', 'POST'])
def new_info():
    form = InfoForm()
    db_sess = db_session.create_session()
    new_info = db_sess.query(Index).first()
    folder = './static/img/'
    if form.validate_on_submit():
        try:
            file = request.files['file']
            if file.filename == '':
                return render_template("new_info.html", form=form,
                                       title='Обновление информации',
                                       message='Файл не может быть пустым')
            if file.filename[-3:] not in ('jpg', 'JPG', 'PNG', 'png', 'pdf', "PDF"):
                return render_template("new_info.html", form=form,
                                       title='Обновление информации',
                                       message='Файл должен являться фотографией')
            new_info.name = form.name.data
            new_info.date = form.date.data
            new_info.photo = folder + file.filename
            s = os.path.join(folder, file.filename)
            file.save(s)
            db_sess.commit()
            return redirect("/")
        except Exception:
            return redirect("/new_info")
    return render_template("new_info.html", form=form, title='Обновление информации')


def main():
    db_session.global_init("db/users.db")
    app.run()


if __name__ == '__main__':
    main()