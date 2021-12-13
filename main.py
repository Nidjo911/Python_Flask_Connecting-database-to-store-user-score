import random
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import User, db
app = Flask(__name__)
db.create_all()

@app.route("/", methods=["GET"])
def index():
    email_address=request.cookies.get("email")

    if email_address:
        user=db.query(User).filter_by(email=email_address).first()
        #da je umjesto first stavljeno - all(), onda bi sve podatke dalo

    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():

    name = request.form.get("user-name")
    email = request.form.get("user-email")

    #kod za tajni broj
    secret_number = random.randint(1, 20)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)
        #user.save()

        db.add(user)
        db.commit()

    #spremanje user emaila u cookie
    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response

#novi route za rezultat.html

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    email_address = request.cookies.get("email")

    user=db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        message = "Tocno! {0}".format(str(guess))

        new_secret = random.randint(1, 20)

        user.secret_number = new_secret
        user.save()

    elif guess > user.secret_number:
        message = "Treba biti manji broj od {0}".format(str(guess))

    elif guess < user.secret_number:
        message = "Treba biti veci broj od {0}".format(str(guess))

    return render_template("result.html", message=message)


if __name__ == "__main__":
    app.run()