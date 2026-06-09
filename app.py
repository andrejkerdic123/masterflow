from flask import Flask, render_template, request, redirect, session
import csv
import os

app = Flask(__name__)
app.secret_key = "tajni_kljuc"

# -----------------------
# USERS FILE
# -----------------------
USERS_FILE = "users.csv"

def init_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="") as f:
            pass

def provjeri_login(username, password):
    init_users()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if row[0] == username and row[1] == password:
                return True
    return False

def registriraj(username, password):
    init_users()
    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, password])

# -----------------------
# DATA PER USER
# -----------------------
def file_for_user():
    user = session.get("user")
    return f"data_{user}.csv"

def ucitaj_poslove():
    file = file_for_user()
    if not os.path.exists(file):
        return []
    with open(file, "r", encoding="utf-8") as f:
        return list(csv.reader(f))

def spremi_posao(datum, klijent, opis, iznos):
    file = file_for_user()
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datum, klijent, opis, iznos])

def obrisi_posao(index):
    poslovi = ucitaj_poslove()
    if 0 <= index < len(poslovi):
        poslovi.pop(index)

        with open(file_for_user(), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(poslovi)

def statistika(poslovi):
    total = 0
    for p in poslovi:
        try:
            total += float(p[3])
        except:
            pass
    return total

# -----------------------
# AUTH ROUTES
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if provjeri_login(u, p):
            session["user"] = u
            return redirect("/")
        return "Krivi login"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        registriraj(u, p)
        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# -----------------------
# APP
# -----------------------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    poslovi = ucitaj_poslove()

    q = request.args.get("q", "").lower()
    if q:
        poslovi = [p for p in poslovi if q in p[1].lower()]

    return render_template(
        "index.html",
        poslovi=poslovi,
        zarada=statistika(poslovi),
        broj=len(poslovi),
        user=session["user"]
    )


@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    spremi_posao(
        request.form["datum"],
        request.form["klijent"],
        request.form["opis"],
        request.form["iznos"]
    )
    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):
    if "user" not in session:
        return redirect("/login")

    obrisi_posao(index)
    return redirect("/")


if __name__ == "__main__":
import os

port = int(os.environ.get("PORT", 8080))

app.run(host="0.0.0.0", port=port)
