from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import UpdateForm, AddForm
from movieapimodule import *
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

# Creates the class (table) Movie
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=False)
    review = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)


db.create_all()
db.session.commit()

# Renders all html files


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.ranking).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = i + 1
        db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route("/update", methods=['POST', 'GET'])
def update():
    form = UpdateForm()
    id = request.args.get('movie_id')
    movie_selected = Movie.query.get(id)
    if request.method == 'POST':
        if form.validate_on_submit():
            id = request.form['id']
            movie_to_update = Movie.query.get(id)
            movie_to_update.rating = request.form['rating']
            movie_to_update.review = request.form['review']
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("edit.html", movie_selected=movie_selected, form=form)


@app.route("/delete")
def delete():
    id = request.args.get('movie_id')
    movie_to_delete = Movie.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['POST', 'GET'])
def add():
    global no_results
    no_results = True
    add_form = AddForm()
    if request.method == 'POST':
        if add_form.validate_on_submit():
            to_query = request.form["title"]
            global query
            query = get_movie_list(to_query)

            no_results = len(query) == 0
            return redirect(url_for('select_movie'))
    return render_template("add.html", add_form=add_form, no_results=no_results)


@app.route("/select")
def select_movie():
    selected_movie = request.args.get("selected_movie")
    if selected_movie != None:
        add_movie(selected_movie)
        return redirect(url_for('home'))
    return render_template("select.html", query=query, no_results=no_results)


if __name__ == '__main__':
    app.run(debug=True)
