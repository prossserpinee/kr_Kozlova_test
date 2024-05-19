from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user


app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kursach.db'


db = SQLAlchemy(app)
manager = LoginManager(app)


class Jury(db.Model):
    name = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return f"<users {self.id}>"


class Players(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    contact = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return f"<users {self.id}>"


class Team(db.Model):
    name_teamleader = db.Column(db.String(100), primary_key=True)
    name_players = db.Column(db.String(300), primary_key=True)
    name_team = db.Column(db.String(100), primary_key=True)
    contact = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return f"<users {self.id}>"


class Manager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_manager = db.Column(db.String(200), nullable=False)
    name_game = db.Column(db.String(200), nullable=False)
    type_game = db.Column(db.String(200), nullable=False)
    type_players = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Codes(db.Model):
    code_jury = db.Column(db.String(100), primary_key=True)
    code_players = db.Column(db.String(100), primary_key=True)
    id_game = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"


@manager.user_loader
def load_user(user_id):
    return Manager.query.get(user_id)


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/home')
def index_home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/instruction')
def instruction():
    return render_template("instruction.html")


@app.route('/jury', methods=["POST", "GET"])
def jury():
    if request.method == "POST":
        hash = generate_password_hash(request.form['psw'])
        if check_password_hash(hash, '0000') == True:
            namee = request.form['name']
            db.session.add(Jury(name=namee))
            db.session.commit()

            return redirect(url_for('about'))

        else:
            return render_template('jury_error.html')
    else:
        db.session.rollback()
    return render_template('jury.html')


@app.route('/player', methods=["POST", "GET"])
def player():
    if request.method == "POST":
        hash = generate_password_hash(request.form['psw'])
        if check_password_hash(hash, '0000') is True:
            namee = request.form['name']
            contactt = request.form['contact']
            db.session.add(Players(name=namee, contact=contactt))
            db.session.commit()

            return redirect(url_for('about'))

        else:
            return render_template('player_error.html')
    else:
        db.session.rollback()
    return render_template('player.html')


@app.route('/teamleader', methods=["POST", "GET"])
def teamleader():
    if request.method == "POST":
        hash = generate_password_hash(request.form['psw'])
        if check_password_hash(hash, '0000') == True:
            namee_teamleader = request.form["teamleader"]
            namee_players = request.form['players']
            namee_team = request.form['team']
            contactt = request.form['contact']
            db.session.add(Team(name_teamleader=namee_teamleader, name_players=namee_players, name_team=namee_team, contact=contactt))
            db.session.commit()

            return redirect(url_for('about'))

        else:
            return render_template('teamleader_error.html')
    else:
        db.session.rollback()
    return render_template('teamleader.html')


@app.route('/manager')
def manager():
    return render_template("manager.html")


@app.route('/manager_new_account', methods=["POST", "GET"])
def manager_new_account():
    if request.method == "POST":
        hash = generate_password_hash(request.form['psw'])
        psw_confirm = request.form['psw_confirm']
        if check_password_hash(hash, psw_confirm) == True:
            namee = request.form["name"]
            email = request.form['email']
            db.session.add(Manager(name=namee, email=email, password=hash))
            db.session.commit()

            return redirect(url_for('manager_account'))

        else:
            return render_template('manager_new_account_error.html')
    else:
        db.session.rollback()
    return render_template("manager_new_account.html")


@app.route('/manager_account', methods=["POST", "GET"])
def manager_account():
    email = request.form.get('email_manager', 'my default')
    password = request.form.get('psw', 'my default')

    if email and password:
        user = Manager.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password) is True:
            login_user(user)
            return redirect(url_for('manager_menu'))

    return render_template("manager_account.html")


@app.route('/manager_menu')
def manager_menu():
    return render_template("manager_menu.html")


@app.route('/manager_new_game', methods=["POST", "GET"])
def manager_new_game():
    if request.method == "POST":

        namee_manager = request.form['name_manager']
        namee_game = request.form['name_game']

        options = request.form.get('options')
        if options == 'option1':
            typee_game = 'Хакатон'
        elif options == 'option2':
            typee_game = 'Квиз'
        elif options == 'option3':
            typee_game = 'Своя игра'

        optionss = request.form.get('optionss')
        if optionss == 'option4':
            typee_players = 'Одиночная игра'
        elif optionss == 'option5':
            typee_players = 'Командная игра'


        db.session.add(Games(name_manager=namee_manager, name_game=namee_game, type_game=typee_game, type_players=typee_players))
        db.session.commit()

        return redirect(url_for('about'))

    else:
        db.session.rollback()

    return render_template('manager_new_game.html')


@app.route('/create_code', methods=["POST", "GET"])
def create_code():
    if request.method == "POST":

        codee_jury = request.form['code_jury']
        codee_players = request.form['code_players']

        db.session.add(Codes(code_jury=codee_jury, code_players=codee_players))
        db.session.commit()

        return redirect(url_for('manager_menu'))
    return render_template("create_code.html")


if __name__ == "__main__":
    app.run(debug=True)