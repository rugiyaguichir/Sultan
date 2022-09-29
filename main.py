from flask import Flask, render_template, redirect, request, url_for, session
from passlib.hash import sha256_crypt
import sqlite3

# con = sqlite3.connect('db.db')
# cur = con.cursor()
# create_table = """
# CREATE TABLE users(
#   id int AUTO_INCREMENT,
#   username varchar(30),
#   email varchar(60),
#   password varchar(100), 
#   PRIMARY KEY (id)
# );
# """
# cur.execute(create_table)
# con.commit()
# cur.close()

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/actors')
def actors():
  return render_template('actors.html')

@app.route('/history')
def history():
  return render_template('history.html')

@app.route('/regin', methods=['GET', 'POST'])
def regin():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = sha256_crypt.encrypt(str(request.form['password']))

    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users(username, email, password) VALUES (?,?,?)", (username, email, password))
    con.commit()
    con.close()
    return redirect(url_for('login'))

  return render_template('regin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    con = sqlite3.connect('db.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", [username])
    count = cur.fetchone()[0]

    if count > 0:
      cur.execute("SELECT * FROM users WHERE username = ?", [username])
      data = cur.fetchone()

      password_db = data['password']

      if sha256_crypt.verify(password, password_db):
        session['logged_in'] = True
        
        return redirect(url_for('congrats'))
      else:
        error = 'Неверный логин или пароль!'
        return render_template('login.html', error=error)

    else:
      error = 'Пользователь не найден!'
      return render_template('login.html', error=error)
 
    con.close()
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('login'))

@app.route('/congrats')
def congrats():
  return render_template('congrats.html')

  
if __name__ == "__main__":
  app.secret_key = 'hi_BITCH'
  app.run(host='0.0.0.0', port='7000')
