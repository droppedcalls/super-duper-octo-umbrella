
from flask import Flask, render_template, session, g, request, redirect, url_for #do we need g?
import sqlite3
app = Flask(__name__)
app.secret_key = 'billpearl'.encode('utf-8')

### DATABASE RELATED ###
# the database file we are going to communicate with
DATABASE = './assignment3.db'

# connects to the database
def get_db():
    # if there is a database, use it
    db = getattr(g, '_database', None)
    if db is None:
        # otherwise, create a database to use
        db = g._database = sqlite3.connect(DATABASE)
    return db

""" # converts the tuples from get_db() into dictionaries
# (don't worry if you don't understand this code)
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row)) """

# given a query, executes and returns the result
# (don't worry if you don't understand this code)
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def write_db(query, args=()):
    db = get_db()
    try:
        cur = db.execute(query, args)
        db.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        return str(e)

### START OF FLASK METHODS ###
# this function gets called when the Flask app shuts down
# tears down the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if we are connected to it
        db.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        sql = 'select username, password, firstname, user_type from user_info'
        creds = query_db(sql)

        for cred in creds:
            if cred[0] == request.form['username'] and cred[1] == request.form['password']:
                    session['username'] = [request.form['username'], cred[2], cred[3]]
                    return redirect(url_for('index'))

        error = 'Incorrect username or password'
    elif 'username' in session:
        return redirect(url_for('index'))
    elif len(request.args) > 0 and request.args.get('f') == 'register':
        error = 'Account created successfully! Please log in to access content.'

    return render_template('login.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        sql = ('insert into user_info values (\'' +
                request.form['username'] + '\',\'' + request.form['password'] + '\',\'' +
                request.form['email'] + '\',\'' + request.form['type'] + '\')')
        msg = write_db(sql)

        if type(msg) == int:
            return redirect(url_for('login', f='register'))
        elif 'constraint failed' in msg:
            error = 'User already exists! If you forgot your password, please contact an instructor.'
        else:
            error = 'Unknown error. Please contact an instructor.'
    
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/home')
def index():
    if len(session) == 0:
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/news') #if time permits, can make it not hardcoded
def news():
    return render_template('news.html')

@app.route('/lectures')
def lec():
    return render_template('lectures.html')

@app.route('/labs')
def labs():
    return render_template('labs.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/tests')
def tests():
    return render_template('tests.html')

@app.route('/resources')
def res():
    return render_template('resources.html')

@app.route('/feedback')
def feedback():
    if session['username'][1] == 'Ins':
        return render_template('view_feedback.html')
    else:
        return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') #allow for external devices to access