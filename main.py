from flask import Flask, url_for, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

#skapar självaste app/hemsidan samn configurerar några saker har ingen aning om vad exakt
app = Flask(__name__)
app.secret_key = "shahab"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#skapar variabel för databas(db)
db = SQLAlchemy(app)

#skapar en model för hur informationen ska vara i databasen
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name, riot):
        self.name = name


#domain rutt för default
@app.route("/")
def home():
    return render_template("home.html")


#domain rutt för home samma som default("/")
@app.route("/home")
def homee():
    return redirect(url_for("home"))


#domain rutt för att kunna se datan i databasen
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


#domain rutt för login som inte direkt är login, det är post funktionen men den skapar en session samtidigt som upplägget
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["riot"]
        session["riot"] = user
        #den gör saker jag inte helt förstått så kan it riktigft beskriva
        users.query.filter_by(name=user).first()

        usr = users(user, "")
        db.session.add(usr)
        db.session.commit()

        return redirect(url_for('view'))
    else:
        return render_template("login.html")


#domain rutt för att logga ut, den tar bort sessionen som skapats
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
