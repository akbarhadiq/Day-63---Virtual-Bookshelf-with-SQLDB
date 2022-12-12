from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from load_dotenv import load_dotenv
import os
from forms import BookForm, EditRating

load_dotenv('secret.env')


app=Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('APP_KEY')
db = SQLAlchemy(app)

# Book database model
class Book(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    return render_template("index.html", title="Home", book_data = Book.query.all())


@app.route("/add", methods=["POST", "GET"])
def add():
    form = BookForm()

    if request.method == "POST":
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

@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditRating()

    if request.method == "POST":
        # Update book record
        book_id = form.hidden_id.data  # ---> hidden value of id data in edit_rating.html
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))

    
    book_id = request.args.get("id")
    book = Book.query.get(book_id)
    return render_template("edit_rating.html" , book=book, form=form)

if __name__ == "__main__":
    app.run(debug=True)
    # db.create_all()