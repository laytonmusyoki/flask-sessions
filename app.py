from flask import Flask ,redirect,render_template,flash,session,request,url_for
from flask_mysqldb import MySQL

app=Flask(__name__)
app.secret_key='layton'
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dashboard"

mysql=MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['uname']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s",(username,password))
        mysql.connection.commit()
        user=cur.fetchone()
        cur.close()
        if user is not None:
            session['loggedin']=True
            session['user_id']=user[0]
            session['username']=user[2]
            return redirect(url_for('dashboard'))
            if 'username' in session:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['uname']
        email=request.form['email']
        password=request.form['password']

        cur=mysql.connection.cursor()
        cur.execute("SELECT username FROM users")
        result=cur.fetchall()
        existing_username=[row[0] for row in result]
        if username in existing_username:
            flash('Username is already taken')
            return render_template('register.html',name=name,username=username,email=email,password=password)
        else:
            cur.execute("INSERT INTO users(name,username,email,password)VALUES(%s,%s,%s,%s)",(name,username,email,password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
     return render_template('dashboard.html',username=session['username'])


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('loggedin',None)
        session.pop('username',None)
        session.pop('user_id',None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST','GET'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method=='POST':
        quote=request.form['quote']
        user_id=session['user_id']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO quotes(user_id,quote)VALUES(%s,%s)",(user_id,quote))
        flash('quote added successfully')
        mysql.connection.commit()
        cur.close()
    return render_template('add.html',username=session['username'])


@app.route('/show')
def show():
    if 'user_id' in session:
        user_id=session['user_id']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM quotes WHERE user_id=%s",(user_id,))
        data=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('show.html',username=session['username'],data=data)


if __name__=='__main__':
    app.run(debug=True)