from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'booksdb')

app.secret_key = 'KeepItSecretKeepItSafe'

@app.route('/')
def index():
    query = "SELECT * FROM books"                          
    books = mysql.query_db(query)     
    # print books
    for i in range(len(books)):
        books[i]['created_at']=books[i]['created_at'].strftime('%b %d %Y')                      # run query with query_db()
    return render_template('index.html', all_books=books)

@app.route('/add', methods=['POST'])
def add():
   
    data = {
             'title': request.form['title'],
             'author': request.form['author']
           }
    # Run query, with dictionary values injected into the query.
    query = "INSERT INTO books (title, author, created_at, updated_at) VALUES (:title, :author, NOW(), NOW() )"
    mysql.query_db(query, data)
    
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    data = {
        'id': request.form['delete']
    }
    print 'data', data
    query = 'DELETE FROM books WHERE id=:id'
    mysql.query_db(query, data)
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    print "in update"
    data = {
        'id': request.form['update']
    }
    print 'data', data
    session['update']= data

    print "UPDATE sessions:", session['update']

    return render_template('update.html')

@app.route('/update_action', methods=['POST'])
def update_action():
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'id': session['update']['id']
    }
    query = 'UPDATE books SET title = :title, author = :author, updated_at = NOW(), created_at = NOW() WHERE id = :id'
    print "QUERY", query
    mysql.query_db(query, data)

    # clear my sessions
    session.clear()
    return redirect('/')

app.run(debug=True)