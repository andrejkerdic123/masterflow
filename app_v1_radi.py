from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

DATOTEKA = "poslovi.csv"


def ucitaj_poslove():
    if not os.path.exists(DATOTEKA):
        return []

    with open(DATOTEKA, "r", encoding="utf-8") as f:
        return list(csv.reader(f))


def obrisi_posao(index):
    poslovi = ucitaj_poslove()

    if 0 <= index < len(poslovi):
        poslovi.pop(index)

        with open(DATOTEKA, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(poslovi)


def statistika(poslovi):
    ukupno = 0

    for p in poslovi:
        try:
            ukupno += float(p[3])
        except:
            pass

    return ukupno


@app.route("/")
def index():
    poslovi = ucitaj_poslove()

    q = request.args.get("q", "").lower()

    if q:
        poslovi = [p for p in poslovi if q in p[1].lower()]

    return render_template(
        "index.html",
        poslovi=poslovi,
        zarada=statistika(poslovi),
        broj=len(poslovi)
    )


@app.route("/add", methods=["POST"])
def add():
    datum = request.form["datum"]
    klijent = request.form["klijent"]
    opis = request.form["opis"]
    iznos = request.form["iznos"]

    with open(DATOTEKA, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datum, klijent, opis, iznos])

    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):
    obrisi_posao(index)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)