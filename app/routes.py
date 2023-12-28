from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Book, Author, Loan
from datetime import datetime

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        new_book = Book(title=title)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        new_author = Author(name=name)
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_author.html')

@app.route('/loan_book/<int:book_id>', methods=['GET', 'POST'])
def loan_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        loan_date = datetime.utcnow()
        new_loan = Loan(book_id=book_id, loan_date=loan_date)
        db.session.add(new_loan)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('loan_book.html', book=book)

@app.route('/return_book/<int:loan_id>', methods=['POST'])
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.return_date = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('index'))
