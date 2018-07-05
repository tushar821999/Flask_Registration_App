from flask import *
import sqlite3
import os

conn = sqlite3.connect('database.db')

app = Flask(__name__)

print("Opened Database Succesfully")
conn.execute('create table if not exists user (email Text,pass Text,rpass Text)')
print("Table created Successfully")

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/signup')
def new_user():
    return render_template('signup.html')

@app.route('/signups',methods=['POST','GET'])
def signups():
    try:
        email = request.form['email']
        password = request.form['psw']
        rpassword = request.form['psw-repeat']

        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("insert into user (email,pass,rpass) values (?,?,?)",(email,password,rpassword))
            conn.commit()
            msg = "User Added Successfully"
    except:
        conn.rollback()
        msg = "error in insert operation"

    finally:
        return render_template("result.html",msg = msg)
        conn.close()

@app.route('/users')
def list():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from user")
    rows = cur.fetchall()
    return render_template("users.html",rows=rows)

if __name__ == '__main__':
    app.run(debug=True,port=8080)