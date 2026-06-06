from flask import Flask, render_template_string, request, redirect
import csv
import os

app = Flask(__name__)

DATOTEKA = "poslovi.csv"


# -----------------------
# UČITAVANJE PODATAKA
# -----------------------
def ucitaj_poslove():
    if not os.path.exists(DATOTEKA):
        return []

    with open(DATOTEKA, "r", encoding="utf-8") as f:
        return list(csv.reader(f))


# -----------------------
# BRISANJE POSLA
# -----------------------
def obrisi_posao(index):
    poslovi = ucitaj_poslove()

    if 0 <= index < len(poslovi):
        poslovi.pop(index)

        with open(DATOTEKA, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(poslovi)


# -----------------------
# STATISTIKA
# -----------------------
def statistika(poslovi):
    ukupno = 0
    for p in poslovi:
        try:
            ukupno += float(p[3])
        except:
            pass
    return ukupno


# -----------------------
# UI
# -----------------------
HTML = """
<style>
body {
    font-family: Arial, sans-serif;
    max-width: 1000px;
    margin: auto;
    padding: 20px;
}

h1, h2 {
    color: #333;
}

input {
    padding: 8px;
    margin: 4px;
}

button {
    padding: 8px 12px;
    cursor: pointer;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
}

th {
    background: #f0f0f0;
}
</style>
<h1>📋 Evidencija poslova</h1>

<form method="POST" action="/add">
  Datum: <input name="datum" required>
  Klijent: <input name="klijent" required>
  Opis: <input name="opis" required>
  Iznos: <input name="iznos" required>
  <button type="submit">➕ Dodaj posao</button>
</form>

<hr>

<h2>📊 Statistika</h2>
<p><b>Ukupna zarada:</b> {{zarada}} EUR</p>
<p><b>Broj poslova:</b> {{broj}}</p>

<hr>

<h2>🧾 Poslovi</h2>

<table border="1" cellpadding="5">
<tr>
  <th>#</th>
  <th>Datum</th>
  <th>Klijent</th>
  <th>Opis</th>
  <th>Iznos</th>
  <th>Akcija</th>
</tr>

{% for p in poslovi %}
<tr>
  <td>{{loop.index0}}</td>
  <td>{{p[0]}}</td>
  <td>{{p[1]}}</td>
  <td>{{p[2]}}</td>
  <td>{{p[3]}} EUR</td>
  <td>
    <a href="/delete/{{loop.index0}}">❌ Obriši</a>
  </td>
</tr>
{% endfor %}

</table>
"""


# -----------------------
# ROUTES
# -----------------------
@app.route("/")
def index():
    poslovi = ucitaj_poslove()
    return render_template_string(
        HTML,
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


# -----------------------
# START
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)