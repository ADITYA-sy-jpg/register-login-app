from flask import Flask, render_template, request, redirect, session, flash
from models import User, SessionLocal, create_tables
from utils import generate_otp, send_otp_email
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
import time
from sqlalchemy.exc import OperationalError
from models import engine

# Wait for DB to be ready
while True:
    try:
        conn = engine.connect()
        conn.close()
        break
    except OperationalError:
        print("Waiting for database...")
        time.sleep(2)

app = Flask(__name__)
app.secret_key = "secret_key"
create_tables()

# ✅ Context manager for independent DB sessions
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required")
            return redirect("/register")

        with get_db() as db:
            if db.query(User).filter(User.email == email).first():
                flash("Email already registered")
                return redirect("/register")

            otp = generate_otp()
            send_otp_email(email, otp)

            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password),
                otp=otp,
                otp_verified=False
            )
            db.add(new_user)
            db.commit()
        
        session["email"] = email
        return redirect("/verify-otp")

    return render_template("register.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    email = session.get("email")
    if not email:
        return redirect("/login")

    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()

    if request.method == "POST":
        entered_otp = request.form.get("otp")
        if user and user.otp == entered_otp:
            with get_db() as db:
                user.otp_verified = True
                db.add(user)
                db.commit()
            flash("OTP Verified! Please log in.")
            return redirect("/login")
        flash("Invalid OTP")

    return render_template("verify_otp.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with get_db() as db:
            user = db.query(User).filter(User.email == email).first()

        if user and user.otp_verified and check_password_hash(user.password, password):
            session["user"] = user.email
            return redirect("/welcome")
        
        flash("Invalid Credentials or OTP not verified")

    return render_template("login.html")

@app.route("/welcome")
def welcome():
    user_email = session.get("user")
    if not user_email:
        return redirect("/login")
    return render_template("welcome.html", email=user_email)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
