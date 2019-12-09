from flask import Flask, redirect, render_template, url_for,request, flash, session
from passlib.hash import sha256_crypt
from forms import LoginForm
from config import *


app.secret_key = "postgres"


@app.route("/")
def index():
	form = LoginForm()
	if 'username' in session:
		flash("You are already logged in")
		return redirect(url_for('home', name = session['username']))
	else:
		flash('Please sign in')
	return render_template("index.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
	form = LoginForm()
	if request.method == "POST":
		if form.validate() == False:
			flash("All fields are required")
		else:
			users = Users.query.all()
			uname = request.form['uname']
			upass = request.form['upass']
			for user in users: 
				if user.username == uname and sha256_crypt.verify(upass, user.password):
					session['username'] = uname
					flash("You are already logged in")
					return redirect(url_for('home', name = session['username']))
					
		flash("Details incorrect! try again!")
		return render_template("index.html", form=form)
	return render_template("index.html", form=form)


@app.route("/signup", methods = ["POST","GET"])
def signup():
	form = LoginForm()
	if request.method == "POST" and form.validate():
		upass = request.form['upass']
		upass = sha256_crypt.encrypt(upass)
		user = Users(
				request.form["uname"],
				upass
			)
		try:
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('index'))
		except:
			flash('Signup failed! user probably already exists')
			return render_template('signup.html', form=form)
	elif request.method == 'GET':
		if 'username' in session:
			flash('You are already logged in')
			return redirect(url_for('home', name = session['username']))	
	return render_template('signup.html', form=form)

@app.route("/home/<name>", methods=["GET","POST"])
def home(name):
	if 'username' in session:
		if name == session['username']:
			name = session['username']
			return render_template('home.html', name=name)
		else:
			return "<h2>Error! invalid user!</h2>"	
	return redirect(url_for('index'))

@app.route('/logout', methods=["GET","POST"])
def logout():
	if "username" in session:
		session.pop('username')
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug= True)

