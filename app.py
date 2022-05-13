from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from calc1rm import Calc1rm
from squat_overload import SquatOverload
import os


class InputForm(FlaskForm):
    weight = IntegerField(label='Weight', validators=[DataRequired()])
    reps = IntegerField(label='Reps', default=1, validators=[DataRequired()])
    workout = SelectField(label='Workout', choices=[('overload', 'Squat Overload'), ('nothing', 'Nothing'), ('also', 'Also Nothing')])
    submit = SubmitField(label='Submit')


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['flask_key']

    Bootstrap(app)

    return app


app = create_app()


def squat_overload_func(one_rm, max_dict):
    squat = SquatOverload(one_rm=one_rm, max_dict=max_dict)
    return squat.day1(), squat.day2(), squat.day3()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    if form.validate_on_submit():
        weight = form.weight.data
        reps = form.reps.data
        calc = Calc1rm()
        one_rm = calc.calc_one_rm(weight=weight, reps=reps)
        max_dict = calc.max_reps
        squat = squat_overload_func(one_rm=one_rm, max_dict=max_dict)
        return f'<h1>Day 1:</h1>{squat[0]}' \
               f'<h1>Day 2:</h1>{squat[1]}' \
               f'<h1>Day 3:</h1>{squat[2]}'

    else:
        return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    pass
    # logout_user()
    # return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
