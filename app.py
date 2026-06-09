from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

FILE = "poslovi.csv"


def ucitaj_poslove():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def spremi_poslove(poslovi):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(poslovi)


@app.route("/")
def index():
    poslovi = ucitaj_poslove()

    zarada = sum(float(p[3]) for p in poslovi) if poslovi else 0
    broj = len(poslovi)

    return render_template("index.html", poslovi=poslovi, zarada=zarada, broj=broj)


@app.route("/add", methods=["POST"])
def add():
    poslovi = ucitaj_poslove()

    novi = [
        request.form["datum"],
        request.form["klijent"],
        request.form["opis"],
        request.form["iznos"]
    ]

    poslovi.append(novi)
    spremi_poslove(poslovi)

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    poslovi = ucitaj_poslove()

    if 0 <= id < len(poslovi):
        poslovi.pop(id)

    spremi_poslove(poslovi)

    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)