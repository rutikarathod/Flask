from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "log_user"


DB_HOST = "localhost"
DB_NAME = "testdb"
DB_USER = "postgres"
DB_PASS = "admin123"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
UPLOAD_FOLDER = 'static/uploads/'
UPLOAD_PDF = 'static/PDF/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_PDF'] = UPLOAD_PDF

  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['pdf'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
      

@app.route("/")
def home():
    if 'checklogin' in session:
        return redirect(url_for('add_user'))
    else:
        if 'userlogin' in session:
            return redirect(url_for('user_panel'))
        else:
            return render_template("login.html")
    


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        cur = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        cur.execute(f"SELECT * FROM admin_user WHERE email='{email}' AND password='{password}'")
        account = cur.fetchone()

        if account:
            session['checklogin'] = True
            session['email'] = account[1]
            session['password'] = account[3]
            
            flash('You were successfully logged in')
            return redirect(url_for('add_user'))
        else:
            error = "Incorrect email/password!"
            return render_template("login.html", error=error)
        cur.close()
    return render_template(" login.html")


@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    if session['checklogin']:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM user_profile,user_login WHERE user_login.id = user_profile.user_id order by user_login.id desc")
        account = cursor.fetchall()
        return render_template("index.html", account=account)
    else:
        return render_template("login.html")


@app.route("/update-user-profile/<int:user_id>")
def fetch_update_user(user_id):
    if session['checklogin']:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}' and user_profile.user_id = '{user_id}'")
        account = cursor.fetchone()
        cursor.close()
        return render_template("edit.html", account=account)
    else:
        return redirect(url_for('admin_login'))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if session['checklogin']:
        if request.method == "POST":
            user_id = request.form.get("user_id")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            dob = request.form.get("dob")
            mob = request.form.get("mob")
            gender = request.form.get("gender")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("zipcode")
            username = request.form.get("username")
            email = request.form.get("email")
            date_modified = datetime.date.today()
            cur = conn.cursor()
            cur.execute(f"""UPDATE user_profile set first_name='{first_name}', last_name='{last_name}', dob='{dob}',
                                    mob='{mob}', gender='{gender}', address='{address}', city='{city}',
                                    state='{state}', zipcode='{zipcode}', profile_dt='{date_modified}' WHERE user_id='{user_id}'""")

            conn.commit()
            cur.close()
        flash("Update succsessfully !!")
        return redirect(url_for('add_user'))
    else:
        return redirect(url_for('home'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_student(id):
    cur = conn.cursor()

    cur.execute('DELETE FROM admin_user WHERE id = {0}'.format(id))
    conn.commit()
    
    return redirect(url_for('add_user'))


@app.route('/add_user_form')
def add_user_form():
    return render_template("user.html")


@app.route('/user', methods=["GET", "POST"])
def user():
    if session['checklogin']:
        cursor = conn.cursor()
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conf_pwd = request.form.get("conf_pwd")
        cursor.execute(f"select * from user_login where email='{email}'")
        user_exist = cursor.fetchone()
        cursor.close()
        if user_exist:
            message = "Account with this email aready exist, please try another email..!!"
            return render_template("user.html", error=message)
        elif request.method == 'POST':
            if password == conf_pwd:
                new_user()
                flash("User Create succsessfully !!")
                return redirect(url_for('add_user'))
            else:
                message = "Password and confirm password doesn't match..!! "
                return render_template("user.html", denied=message)
    else:
        return redirect(url_for('login_user'))
    return redirect(url_for('add_user_form'))


def new_user():
    cursor = conn.cursor()
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hash_pwd = generate_password_hash(password)
    cursor.execute(f"""INSERT INTO user_login (username,email,password)
                            VALUES('{username}','{email}','{hash_pwd}')""")
    conn.commit()
    cursor.execute("SELECT max(id) FROM user_login")
    user_id = cursor.fetchone()
    cursor.execute(f"""INSERT INTO user_profile (user_id)
                            VALUES('{user_id[0]}')""")
    conn.commit()
    cursor.close()
    return redirect(url_for('add_user'))


@app.route("/user-login", methods=["GET", "POST"])
def user_login():
    cursor = conn.cursor()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor.execute(f"SELECT * FROM user_login where email = '{email}'")
        account = cursor.fetchone()
        print(account)
        if account:
            password_rs = account[3]
            check = check_password_hash(password_rs, password)
            if check:
                session['userlogin'] = True
                session['username'] = account[2]
                session['uid'] = account[0]
                
                return redirect(url_for('user_panel'))
            else:
                error = "Invalid credentials"
                return render_template('user_login.html', error=error)
        else:
            error = "Account with is email doesn't exist..!!"
            return render_template('user_login.html', error=error)
    cursor.close()
    return render_template('user_login.html')


@app.route('/user-dashboard')
def user_panel():
    if session['userlogin']:
        cursor = conn.cursor()
        user_id = session['uid']
        cursor.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}' and user_profile.user_id = '{user_id}'")
        account = cursor.fetchone()
        return render_template("user_dashboard.html", name=session['username'], account=account)
    else:
        return render_template("user_login.html")


@app.route("/user_id")
def fetch_edit_user():
    user_id = session['uid']
    if session['userlogin']:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}' and user_profile.user_id = '{user_id}'")
        account = cursor.fetchone()
        cursor.close()
        return render_template("update.html", account=account)

    else:
        return redirect(url_for('home'))

@app.route("/update",methods=['GET', 'POST'])
def update():
    if session['userlogin']:
        if request.method == "POST":
            user_id = request.form.get("user_id")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            dob = request.form.get("dob")
            mob = request.form.get("mob")
            gender = request.form.get("gender")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("zipcode")
            username = request.form.get("username")
            email = request.form.get("email")
            file = request.files['file']
            pdf = request.files['pdf']
            date_modified = datetime.date.today()
            cur = conn.cursor()
            if request.method == "POST":
                
                filename = secure_filename(file.filename)
                pdfname = secure_filename(pdf.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pdf.save(os.path.join(app.config['UPLOAD_FOLDER_PDF'], pdfname))
                 
                cur.execute(f"""update user_profile set first_name='{first_name}', last_name='{last_name}', dob='{dob}',
                    mob='{mob}', gender='{gender}', address='{address}', city='{city}',
                    state='{state}', zipcode='{zipcode}', profile_dt='{date_modified}', file='{filename}', pdf='{pdfname}'  WHERE user_id='{user_id}'""")
                
                conn.commit()
                cur.close()
                
                return redirect(url_for('user_panel'))
    else:
        return redirect(url_for('home'))


   


@app.route('/resetpw/<int:user_id>', methods=["GET", "POST"])
def resetpw(user_id):
    if session['checklogin']:
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}'and user_profile.user_id = '{user_id}'")
        account = cur.fetchone()
        print(account)

        return render_template("password.html", account=account)
    else:
        return redirect(url_for('add_user'))


@app.route('/newpw/<int:user_id>', methods=["GET", "POST"])
def newpw(user_id):
    if session['checklogin']:
        password = request.form.get('password')
        conf_pwd = request.form.get('conf_pwd')
        if request.method == "POST":
            if password == conf_pwd:
                confirm_pw()

            else:
                
                cur = conn.cursor()
                cur.execute(
                    f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}'and user_profile.user_id = '{user_id}'")
                account = cur.fetchone()
                msg = "Password and Confirm password doesn't match..."
                return render_template("password.html", account=account, error=msg)
    else:
        return redirect(url_for('login_user'))
    return redirect(url_for('add_user'))


def confirm_pw():
    cur = conn.cursor()
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    hash_pwd = generate_password_hash(password)
    cur.execute(f"UPDATE user_login set password='{hash_pwd}' WHERE id='{user_id}'")
    conn.commit()
    cur.close()
    flash(' Password Successfully')
    return redirect(url_for('add_user'))


@app.route("/delete/<int:user_id>")
def delete(user_id):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM user_profile where user_id ='{user_id}'")
    cursor.execute(f"DELETE FROM user_login where id ='{user_id}'")
    conn.commit()
    cursor.close()
    return redirect(url_for('add_user'))







@app.route("/logout-admin")
def logout_admin():
    session.pop('checklogin',None)
    session.clear()
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('userlogin',None)
    session.clear()
    return render_template("user_login.html")
if __name__ == '__main__':
    app.run()
