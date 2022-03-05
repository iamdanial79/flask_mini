from flask import Flask, redirect,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, true
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_main"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    f_name = db.Column(db.String(125))
    l_name = db.Column(db.String(125))
    email = db.Column(db.String(125))

db.create_all()
db.session.commit()

@app.route("/")
def Table():
    users = User.query.all()
    return render_template("table.html",users = users)

@app.route("/Form")
def Form():

    return render_template("form.html")

@app.route("/new")
def new():
    return render_template("form.html",form_action = 'insert' , user = None)

@app.route('/add',methods=["Post"])
def add():
    first = request.form["first name"]
    last = request.form["last name"]
    email = request.form["email"]

    users = User(f_name = first , l_name = last , email=email)
    db.session.add(users)
    db.session.commit()
    return redirect(url_for('Table'))

@app.route('/edit/<id>')
def edit(id):
    user = User.query.get(id)
    return render_template("form.html",user = user , form_action = 'update')

@app.route("/update",methods=["Post"])
def update():
    first = request.form["first name"]
    last = request.form["last name"]
    email = request.form["email"]

    id = request.form["id"]
    user = User.query.get(id)
    user.f_name = first
    user.l_name = last
    user.email = email
    db.session.commit()
    return redirect(url_for('Table'))


@app.route('/remove/<id>')
def remove(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('Table'))


if __name__ == "__main__" :
    app.run(debug=True)