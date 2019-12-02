from flask import Flask, redirect, render_template, url_for,request, flash
from forms import LoginForm
from config import *


app.secret_key = "postgres"


@app.route("/")
def index():
	form = LoginForm()
	return render_template("index.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		form = LoginForm()
		if form.validate() == False:
			flash("All fields are required")
		else:
			users = Users.query.all()
			uname = request.form['uname']
			upass = request.form['upass']
			for user in users:
				if user.username == uname and user.password == upass:
					return redirect(url_for('home', name = user.username))
				else:
					flash("Details incorrect! try again!")
	return redirect(url_for("index"))


@app.route("/signup", methods = ["POST","GET"])
def signup():
	form = LoginForm()
	if request.method == "POST":
		if form.validate() == False:
			user = Users(
					request.form["uname"],
					request.form["upass"]
				)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('index'))	
	return render_template('signup.html', form=form)

@app.route("/home/<name>", methods=["GET","POST"])
def home(name):
	users = Users.query.all()
	for user in users:
		name = user.username
	return render_template('home.html', name=name)

if __name__ == "__main__":
	app.run(debug= True)

