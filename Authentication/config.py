from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dbpg@localhost/reg"
app.config['SECRET_KEY'] = "sputum"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
	id = db.Column("user_id", db.Integer, primary_key = True)

	username = db.Column(db.String(25), unique=True, nullable = False)

	password = db.Column(db.String(15), nullable=False)

	def __init__ (self,username,password):
		self.username = username
		self.password = password

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)