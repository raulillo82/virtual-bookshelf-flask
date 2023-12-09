from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# create the extension
db = SQLAlchemy()
# initialize the app with the extension
db.init_app(app)

#Create table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

#Create table schema
#Exceptions already handled, if it exists, it'll be fine
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    #Read all records
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["title"],
                    author=request.form["author"],
                    rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route('/edit', methods=["GET", "POST"])
def edit():

    if request.method == "GET":
    #Read a Particular Record By Query
        with app.app_context():
            selected_book = db.get_or_404(Book, request.args.get("book_id"))
            return render_template("edit.html", book=selected_book)

    elif request.method == "POST":
    #Update a Particular Record By Query
        with app.app_context():
            book_to_update = db.get_or_404(Book, request.form["book_id"])
            book_to_update.rating = request.form["rating"]
            db.session.commit()
            return redirect(url_for("home"))

@app.route('/delete')
def delete():
    #Delete a Particular Record By PRIMARY KEY
    book_id = request.args.get("book_id")
    with app.app_context():
        book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
