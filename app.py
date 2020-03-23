from flask import Flask
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class xzhang270_nobelprizeinliterature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issued_year=db.Column(db.Integer)
    first_name=db.Column(db.String(255))
    last_name=db.Column(db.String(255))
    country=db.Column(db.String(255))
    language_used=db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | year: {1} | first name: {2} | last name: {3} | country: {4} | language: {5}".format(self.id, self.issued_year, self.first_name, self.last_name, self.country, self.language_used)

class NobelForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    issued_year = StringField('Year:', validators=[DataRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    country= StringField('Country:', validators=[DataRequired()])
    language_used = StringField('Language:', validators=[DataRequired()])


@app.route('/')
def index():
    some_winners = xzhang270_nobelprizeinliterature.query.all()
    return render_template('index.html', winners=some_winners, pageTitle='Nobel Prize in Literature')

@app.route('/add_winner', methods=['GET','POST'])
def add_winner():
    form = NobelForm()
    if form.validate_on_submit():
        winner=xzhang270_nobelprizeinliterature(issued_year=form.issued_year.data, first_name=form.first_name.data, last_name=form.last_name.data, country=form.country.data, language_used=form.language_used.data)
        db.session.add(winner)
        db.session.commit()
        return redirect('/')

    return render_template('add_winner.html', form=form, pageTitle='Add A New Winner')

@app.route('/delete_winner/<int:winner_id>', methods=['GET','POST'])
def delete_winner(winner_id):
    if request.method=='POST':
        winner=xzhang270_nobelprizeinliterature.query.get_or_404(winner_id)
        db.session.delete(winner)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
