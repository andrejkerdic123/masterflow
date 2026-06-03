import csv
import os

DATOTEKA = "poslovi.csv"


def dodaj_posao():

    datum = input("Datum: ")
    klijent = input("Klijent: ")
    opis = input("Opis posla: ")
    iznos = float(input("Iznos EUR: "))

    with open(DATOTEKA, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            datum,
            klijent,
            opis,
            iznos
        ])

    print("\nPosao spremljen.\n")


def prikazi_poslove():

    if not os.path.exists(DATOTEKA):
        print("\nNema spremljenih poslova.\n")
        return

    with open(DATOTEKA, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        print()

        for red in reader:

            print(
                f"Datum: {red[0]} | "
                f"Klijent: {red[1]} | "
                f"Opis: {red[2]} | "
                f"Iznos: {red[3]} EUR"
            )

        print()


def prikazi_zaradu():

    if not os.path.exists(DATOTEKA):
        print("\nNema spremljenih poslova.\n")
        return

    ukupna_zarada = 0
    broj_poslova = 0

    with open(DATOTEKA, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for red in reader:

            ukupna_zarada += float(red[3])
            broj_poslova += 1

    print()
    print(f"Ukupno poslova: {broj_poslova}")
    print(f"Ukupna zarada: {ukupna_zarada:.2f} EUR")

    if broj_poslova > 0:
        prosjek = ukupna_zarada / broj_poslova
        print(f"Prosjek po poslu: {prosjek:.2f} EUR")

    print()


while True:

    print("=== EVIDENCIJA POSLOVA ===")
    print("1 - Dodaj posao")
    print("2 - Prikaži sve poslove")
    print("3 - Prikaži zaradu")
    print("4 - Izlaz")

    izbor = input("\nOdaberi opciju: ")

    if izbor == "1":
        dodaj_posao()

    elif izbor == "2":
        prikazi_poslove()

    elif izbor == "3":
        prikazi_zaradu()

    elif izbor == "4":
        print("\nDoviđenja.")
        break

    else:
        print("\nPogrešan unos.\n")