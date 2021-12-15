__author__ = 'Spencer Shilling, Mason Shockley'

success = False

#imports
import sqlite3
from flask import Flask, render_template
from flask import request, redirect, url_for

#instantiate
app = Flask(__name__)
# route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():

    
    conn = sqlite3.connect('celebrities.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM member_login''')
    data = c.fetchall()
    
        
    error = None
    
    if request.method == 'POST':
        for val in data:
            global memID
            memID = int(request.form['memberID'])
            if request.form['username'] != val[1] or request.form['password'] != val[2] or int(request.form['memberID']) != val[0]:
            
                error = 'Invalid Credentials. Please try again.'
            else:
                
                return redirect(url_for('info'))
    return render_template('login.htm', error=error)

@app.route('/info', methods=['GET', 'POST'])
def info():
    memberID=None
    firstname = ''
    lastname = ''
    age = None
    email = ''
    bio = ''
    success = False
    #this is called when the page is FIRST LOADED

    if request.method == 'GET':
        #connect to the database and select one record (row of data)
        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM members''')
        rows = c.fetchall()
        #print(row)
        #if the row contains data, store it in variables
        for row in rows:
            if row[0] == memID:
                memberID = row[0]
                firstname = row[1]
                lastname = row[2]
                age = row[3]
                email = row[4]
                bio = row[5]
                photo = str(row[6])
            
            
        #close connection to the database
        conn.close()
        #print(row)
    #this is called when the submit button is clicked
    if request.method == 'POST':
        #get the data from the form and store it in variables
        #this uses the request method to get the data from named elements on the form
        memberID = request.form['memberID']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        email = request.form['email']
        bio = request.form['bio']
        success = True
        #now store the data from the form into the database
        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM members''')
        row = c.fetchone()
        
        if row: #if the row exist, update the data in the row
            c.execute('''UPDATE members SET firstname = ?, lastname = ?, age = ?, email = ?, bio = ? WHERE
memberID = ?''',
                      (firstname, lastname, age, email, bio, memberID))
            success = True
        else:
            c.execute('''INSERT INTO members VALUES (?, ?, ?, ?, ?, ?)''',
                      (memberID, firstname, lastname, age, email, bio))
            success = True
        conn.commit()
        conn.close()
    return render_template('profile.htm', memberID=memberID, firstname=firstname, lastname=lastname, age=age,
                           email=email, bio=bio, success=success, photo=photo)

@app.route('/view_all_celebs')
def view_all():
    celebID=None
    firstname=''
    lastname=''
    age=''
    email=''
    photo=''
    bio=''
    test=0

    conn=sqlite3.connect('celebrities.db')
    c=conn.cursor()
    c.execute('''SELECT * FROM celebs ORDER BY celebID''')
    rows=c.fetchall()
    conn.close()
    return render_template('view_all_celebs.htm',
                           rows=rows, test=test)

@app.route('/view_one_celeb')
def view():
    celebID=None
    firstname=''
    lastname=''
    age=''
    email=''
    photo=''
    bio=''

    conn=sqlite3.connect('celebrities.db')
    c=conn.cursor()
    c.execute('''SELECT * FROM celebs''')
    row = c.fetchone()

    
    celebID = row[0]
    firstname = row[1]
    lastname = row[2]
    age = row[3]
    email = row[4]
    photo = row[5]
    conn.close
    return render_template('view_one_celeb.htm', celebID=celebID, firstname=firstname, lastname=lastname, age=age, email=email, photo=photo, bio=bio)

def get(request):
    pass

def post(request):
    pass

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":

    app.run(debug=False)
    
