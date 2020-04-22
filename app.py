
from flask import Flask, render_template, session, g, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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


def write_db_many(query, values=()):
    db = get_db()
    try:
        cur = db.executemany(query, values)
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

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        sql = 'select username, password, firstname, user_type from user_info where username=\'' + request.form['username'] + '\''
        try:
            user = query_db(sql)[0]
        except IndexError:
            error = 'User does not exist! Please try again'
            return render_template('login.html', error=error)

        if user[0] == request.form['username'] and check_password_hash(user[1], request.form['password']):
            session['user'] = {'username': request.form['username'], 'firstname': user[2], 'type': user[3]}
            return redirect(url_for('index'))
        else:
            error = 'Incorrect username or password'
    elif 'user' in session:
        return redirect(url_for('index'))
    elif len(request.args) > 0 and request.args.get('f') == 'register':
        error = 'Account created successfully! Please log in to access content.'

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = ''
    if request.method == 'POST':
        sql = ('insert into user_info values (\'' +
                request.form['username'] + '\',\'' + generate_password_hash(request.form['password']) + '\',\'' +
                request.form['email'] + '\',\'' + request.form['first'] + '\',\'' +
                request.form['last'] + '\',\'' + request.form['type'] + '\')')

        msg = write_db(sql)

        if type(msg) == int:
            return redirect(url_for('login', f='register'))
        elif 'constraint failed' in msg and 'user_info.username' in msg:
            error = 'User already exists! If you forgot your password, please contact an instructor.'
        elif 'constraint failed' in msg and 'user_info.email' in msg:
            error = 'User with that email already exists! If you forgot your password, please contact an instructor.'
        else:
            error = 'Unknown error. Please contact an instructor.'
    
    return render_template('register.html', error = error)

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('login'))

@app.route('/home')
def index():
    if len(session) == 0:
        return redirect(url_for('login'))

    return render_template('index.html', title = 'Home')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title = 'Calendar')

@app.route('/news') #if time permits, can make it not hardcoded
def news():
    return render_template('news.html', title = 'News')

@app.route('/team')
def team():
    return render_template('team.html', title = 'Course Team')

@app.route('/lectures')
def lec():
    return render_template('lectures.html', title='Lectures')

@app.route('/labs')
def labs():
    return render_template('labs.html', title='Labs')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html', title='Assignments')

@app.route('/tests')
def tests():
    return render_template('tests.html', title='Tests')

@app.route('/grades', methods=['GET', 'POST', 'DEL'])
def grades():
    #pull the entire grades table
    student_grades = query_db('select * from grades')
    evals = [ eval[0] for eval in query_db('select distinct eval from grades') ]
    #show a different set of information if the user is an instructor
    if session['user']['type'] == 'Ins':
        remark_check = 'There are no remark requests at this moment.'
        get_remarks = query_db('select distinct * from remark')
        delete_msg = ''
        if get_remarks != None:
            remark_check = ''

        if request.method == 'POST' and request.form['remark'] == 'no':
            if request.form['eval-name'] in evals and request.form['username'] in [ entry[0] for entry in student_grades ]:
                sql = ('update grades set grade=\'' + request.form['grade'] + '\'' ' where username=\'' +
                    request.form['username'] + '\' and eval=\'' + request.form['eval-name'] + '\'')
            else:
                sql = ('insert into grades values (\'' +
                    request.form['username'] + '\',\'' + request.form['eval-name'] + '\',\'' +
                    request.form['grade'] + '\')')

            msg = write_db(sql)
            if type(msg) == int:
                return redirect(url_for('grades'))
            elif 'constraint failed' in msg:
                ins_err = 'Entry already exists!'
                return render_template('grades_instructor.html', student_grades = student_grades, evals = evals, remark_check = remark_check, get_remarks = get_remarks, ins_err=ins_err)
        elif request.method == 'POST' and request.form['remark'] == 'yes':
            sql = ('delete from remark where username=\'' +
                    request.form['username'] + '\' and eval=\'' + request.form['eval-name'] + '\' and reason=\'' +
                    request.form['reason'] + '\'')
            
            msg = write_db(sql)
            return redirect(url_for('grades'))

        return render_template('grades_instructor.html', student_grades = student_grades, evals = evals, remark_check = remark_check, get_remarks = get_remarks, ins_err='')
        
    #set of information for students
    else:
        send_message = ''
        table_builder = []
        for grade_entry in student_grades:
            if grade_entry[0] == session['user']['username']:
                table_builder.append(grade_entry)

        #remark submission
        if request.method == 'POST':
            sql = ('insert into remark values (\'' +
                    session['user']['username'] + '\',\'' + request.form['eval'] + '\',\'' + request.form['remark_request'] + '\')')
            msg = write_db(sql)
            app.logger.info(msg)
            send_message = 'Thank you for your request.'

        return render_template('grades.html', table_builder = table_builder, send_message = send_message)

@app.route('/resources')
def res():
    return render_template('resources.html', title='Resources')

q_map = {1: 'What do you like about the instructor teaching?',
         2: 'What do you recommend the instructor to do to improve their teaching?',
         3: 'What do you like about the labs?',
         4: 'What do you recommend the lab instructors to do to improve their lab teaching?'}

@app.route('/feedback', methods=['GET','POST'])
def feedback():
    title = 'Feedback'
    ins_list = query_db('select username, firstname, lastname from user_info where user_type = \'Ins\'')

    if request.method == 'POST': #will only be used for students
        feedback_id = query_db('select max(feedback_id) from feedback')[0][0]

        ans_list = []
        for key in request.form:
            if key != 'ins' and request.form[key] != '':
                ans_list.append((request.form['ins'], feedback_id + 1, int(key), request.form[key]))

        write_db_many('insert into feedback values(?,?,?,?)', ans_list)

        return render_template('feedback.html', title=title, ins_list=ins_list, q_map=q_map, submitted=1)
    if session['user']['type'] == 'Ins':
        fb_list = query_db('select q_num, response from feedback where username=\'' + session['user']['username'] + '\'')
        fb_mapped = {}
        for entry in fb_list:
            if entry[0] in fb_mapped.keys():
                fb_mapped[entry[0]].append(entry[1])
            else:
                fb_mapped[entry[0]] = [entry[1]]

        return render_template('view_feedback.html', title=title, q_map=q_map, fb_list=fb_mapped)
    else:
        return render_template('feedback.html', title=title, ins_list=ins_list, q_map=q_map)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') #allow for external devices to access