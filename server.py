from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from load_dotenv import load_dotenv
import os
from forms import BookForm

load_dotenv('secret.env')


app=Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('APP_KEY')
db = SQLAlchemy(app)

# Book database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="Home")


@app.route("/add", methods=["POST", "GET"])
def add():
    form = BookForm()
    if form.validate_on_submit:
        book_title = form.title.data
        book_author = form.author.data
        book_rating = form.rating.data

        # add the book data to database
        new_book = Book(title=book_title, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()

        # flash a message, return to home
        flash(f"{book_title} by {book_author} is successfully added to the database!")
        return redirect(url_for('home'))


    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
    # db.create_all()