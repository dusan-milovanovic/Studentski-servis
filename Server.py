import tkinter
from tkinter import *
import sqlite3
import time
import socket
import threading
import json

s = socket.socket()
host = socket.gethostname()
port = 30111
s.bind((host, port))
s.listen(5)

listaKorisnika = [['14588', 'Danijela'], ['98653', 'Marija'], ['54896', 'Jovan'], ['1', 'Dusan']]
fp = open('jsonpodaci.txt', 'w')
for korisnik in listaKorisnika:
    jsovan = '{"broj": ' + f"{korisnik[0]}" + ', "ime": 'f"{korisnik[1]}"'}'
    print(jsovan)
    json.dump(jsovan, fp)
fp.close()

korisnici = {
    "14588": "Danijela",
    "98653": "Marija",
    "54896": "Jovan",
    "1": "Dusan",
    "": "Korisnik"
}


def slanje():
    while True:
        conn, addr = s.accept()
        print('Got connection from', addr)
        poruka = conn.recv(1024).decode()
        print('Poruka je: ', poruka)
        svrha = poruka.split('+')
        if svrha[0] == 'Predmeti':
            lista = map(rastavi(svrha[1]), ['', ''])
            print("indeks je ", lista)
            student = trazi(svrha[1])
            print("student je ", student.__str__())
            predmeti = tekstPredmetiSlanje(student)
            print("predmeti su\n", predmeti)
        if svrha[0] == 'Ispiti':
            baza = sqlite3.connect('DB.db')
            cursor = baza.execute(f'''SELECT imepredmeta, vreme, provera FROM predmeti 
                        INNER JOIN predmetielite7020
                        ON predmeti.sifrapredmeta=predmetielite7020.predmet
                        WHERE provera='Ispit' OR provera = 'Kolokvijum' ''')
            predmeti = ''
            for row in cursor:
                predmet = row[0]
                tip = row[1]
                vreme = row[2]
                jedanPredmet = predmet + "+" + tip + "+" + vreme
                predmeti += jedanPredmet + "_"
        if svrha[0] == 'Prijava':
            poruka2 = conn.recv(1024).decode()
            print("dobijeno dva ", poruka2)
            studentSmer = svrha[1][0:svrha[1].index("/") + 3].split("-")[0]
            studentBrojIndeksa = svrha[1][0:svrha[1].index("/") + 3].split("-")[1].split("/")[0]
            studentGodinaUpisa = svrha[1][0:svrha[1].index("/") + 3].split("-")[1].split("/")[1]
            print("smer ", studentSmer, " indeks ", studentBrojIndeksa, " god ", studentGodinaUpisa)
            baza = sqlite3.connect('DB.db')
            print("ime predmeta je ", poruka2)
            sifra = baza.execute(f'''SELECT sifrapredmeta FROM predmeti WHERE imepredmeta='{poruka2}' ''')
            for row in sifra:
                print("nesto je nesto ", row[0])
                sifrapredmeta = row[0]
            # print("dobijena sifra ", sifra)
            baza.execute(f'''UPDATE PREDMETI{studentSmer + studentBrojIndeksa + studentGodinaUpisa}
                                SET prijavljen=1 WHERE PREDMET='{sifrapredmeta}' ''')
            baza.commit()
            print("promenjena prijava")
        if svrha[0] == 'Labela':
            pass

        conn.send(predmeti.encode())
        conn.close()


def rastavi(string):
    rastavljeno = []
    rastavljeno.insert(0, string[0:string.index("/") + 3].split("-")[0])
    rastavljeno.insert(1, string[0:string.index("/") + 3].split("-")[1].split("/")[0])
    rastavljeno.insert(2, string[0:string.index("/") + 3].split("-")[1].split("/")[1])
    return rastavljeno


class Student:
    def __init__(self, id, ime, prezime, smer, broj_indeksa, godina_upisa, godina_studija, semestar, status, predmeti):
        self.id = id
        self.ime = ime
        self.prezime = prezime
        self.smer = smer
        self.godina_upisa = godina_upisa
        self.broj_indeksa = broj_indeksa
        self.godina = godina_studija
        self.semestar = semestar
        self.status = status
        self.predmeti = predmeti


def prijava(sifra):
    for key in korisnici:
        if sifra == key:
            frameOpcije.grid(row=1, columnspan=10, pady=5)
            labelPrijava.configure(text=f'Prijavljen je korisnik: {korisnici.get(key)}', bg='green')
            entryIme.delete(0, END)


def odjava():
    frameOpcije.grid_forget()
    labelPrijava.configure(text='Niste prijavljeni', bg='red')


def prikaziFrejm():
    if izbor.get() == 1:
        frameZakazivanje.grid(
            row=1,
            columnspan=4,
            padx=10,
            pady=10,
            ipadx=5,
            ipady=5
        )
        # frameKlk.grid_forget()
        frameStatus.grid_forget()
        frameOcena.grid_forget()
    if izbor.get() == 2:
        frameZakazivanje.grid_forget()
        # frameKlk.grid_forget()
        frameStatus.grid(
            row=1,
            columnspan=4,
            padx=10,
            pady=10,
            ipadx=5,
            ipady=5
        )
        frameOcena.grid_forget()
    if izbor.get() == 3:
        frameZakazivanje.grid_forget()
        # frameKlk.grid_forget()
        frameStatus.grid_forget()
        frameOcena.grid(
            row=1,
            columnspan=4,
            padx=10,
            pady=10,
            ipadx=5,
            ipady=5
        )


def zakazivanje():
    predmet = unosPredmet.get()
    unetiDatum = unosDatum.get()
    unetoVreme = unosVreme.get()
    datumIvreme = time.strptime(f'{unetiDatum} {unetoVreme}',
                                '%d/%m/%Y %H:%M')
    conn = sqlite3.connect('DB.db')
    if izborIspitKlk.get() == 1:
        izabrano = 'Ispit'
    if izborIspitKlk.get() == 2:
        izabrano = 'Kolokvijum'
    conn.execute(f'''UPDATE predmeti SET PROVERA = '{izabrano}' WHERE SIFRAPREDMETA = {predmet}''')
    conn.execute(
        f'''UPDATE predmeti SET VREME = '{time.strftime('%d/%m/%Y %H:%M', datumIvreme)}' WHERE SIFRAPREDMETA = {predmet}''')
    conn.commit()


def ispis():
    student = trazi(unosStudenta.get())
    ispisStatusa.configure(state=NORMAL)
    tekst(student)
    ispisStatusa.configure(state=DISABLED)


def trazi(unetiStudent):
    studentSmer = unetiStudent.split("-")[0]
    studentBrojIndeksa = unetiStudent.split("-")[1].split("/")[0]
    studentGodinaUpisa = unetiStudent.split("-")[1].split("/")[1]
    # print(f'''Dobijeno: smer = {studentSmer} | broj = {studentBrojIndeksa} | god = {studentGodinaUpisa}''')
    conn = sqlite3.connect('DB.db')
    cursor = conn.execute(f'''SELECT * FROM STUDENTI WHERE SMER LIKE '{studentSmer}' 
    AND GODINAUPISA LIKE '{studentGodinaUpisa}' AND BROJINDEKSA LIKE '{studentBrojIndeksa}' ''')
    for row in cursor:
        studentID = row[0]
        studentIme = row[1]
        studentPrezime = row[2]
        studentGodinaStudija = row[6]
        studentSemestar = row[7]
        studentStatus = row[8]
        # print("ID = ", row[0])
        # print("IME = ", row[1])
        # print("PREZIME = ", row[2])
        # print("SMER = ", row[3], "\n")
        # print("GODINA = ", studentGodinaStudija)
        # print("SEMESTAR = ", studentSemestar)
        # print("STATUS = ", studentStatus)
        # print("Operation done successfully")
    cursor = conn.execute(f'SELECT * FROM PREDMETI{studentSmer + studentBrojIndeksa + studentGodinaUpisa}')
    studentPredmeti = []
    for row in cursor:
        studentPredmeti.append(
            [conn.execute(f'SELECT IMEPREDMETA FROM PREDMETI WHERE SIFRAPREDMETA={row[1]}').fetchone(),
             row[2], row[3]])
    student = Student(
        studentID,
        studentIme,
        studentPrezime,
        studentSmer,
        studentBrojIndeksa,
        studentGodinaUpisa,
        studentGodinaStudija,
        studentSemestar,
        studentStatus,
        studentPredmeti
    )
    return student


def tekstPredmeti(student: Student):
    tekstPredmeti = ''
    redniBroj = 1
    for lista in student.predmeti:
        predmet = lista[0][0] + " " * (39 - len(lista[0][0]))
        if lista[2] == 'Polozio':
            PN = lista[2] + " " * 5
        else:
            PN = lista[2]
        jednaLinija = f'    {redniBroj}   {predmet}    {PN}    {lista[1]}\n'
        redniBroj += 1
        tekstPredmeti += jednaLinija
    return tekstPredmeti


def tekstPredmetiSlanje(student: Student):
    tekstPredmeti = ''
    redniBroj = 1
    for lista in student.predmeti:
        predmet = lista[0][0] + " " * (39 - len(lista[0][0]))
        if lista[2] == 'Polozio':
            PN = lista[2] + " " * 5
        else:
            PN = lista[2]
        jednaLinija = f'{redniBroj}   {predmet}    {PN}    {lista[1]}\n'
        redniBroj += 1
        tekstPredmeti += jednaLinija
    return tekstPredmeti


def tekst(student: Student):
    tekst = f"""
    Student: {student.ime + " " + student.prezime}
    Broj indeksa: {student.smer + "-" + student.godina_upisa + "/" + student.broj_indeksa}
    Godina: {student.godina}   Semestar: {student.semestar}
    Status: {student.status}
    
    #   Predmet                                    P/N             Ocena
    ---------------------------------------------------------------------\n"""
    tekst += tekstPredmeti(student)

    """
    1   Osnovi elektronike             nepolozen
    2   Digitalna televizija           polozen           6
    3   Funkcionalno programiranje     polozen           6
    4   Telekomunikacioni servisi      polozen           9
        i tehnologije
    5   Programabilna logicka kola     polozen           9
    """
    # ╔═════════╦═══════╦═════╗
    # ║ Predmet ║ Ocena ║ P/N ║
    # ╠═════════╬═══════╬═════╣
    # ║         ║       ║     ║
    # ╠═════════╬═══════╬═════╣
    # ║         ║       ║     ║
    # ╠═════════╬═══════╬═════╣
    # ║         ║       ║     ║
    # ╚═════════╩═══════╩═════╝
    ispisStatusa.delete('1.0', END)
    ispisStatusa.insert(INSERT, tekst)


def izmenaOcene():
    unetiBrojIndeksa = unosOceneStudent.get()
    smer = unetiBrojIndeksa.split("-")[0]
    brojIndeksa = unetiBrojIndeksa.split("-")[1].split("/")[0]
    godinaUpisa = unetiBrojIndeksa.split("-")[1].split("/")[1]
    predmet = unosOcenePredmet.get()
    ocena = unosOcene.get()
    conn = sqlite3.connect('DB.db')
    conn.execute(f'''UPDATE PREDMETI{smer + brojIndeksa + godinaUpisa} 
                SET OCENA={ocena} WHERE PREDMET={predmet}''')
    if int(ocena) > 5:
        conn.execute(f'''UPDATE PREDMETI{smer + brojIndeksa + godinaUpisa} 
                    SET STATUS='Polozio' WHERE PREDMET={predmet}''')
    else:
        conn.execute(f'''UPDATE PREDMETI{smer + brojIndeksa + godinaUpisa} 
                    SET STATUS='Nije polozio' WHERE PREDMET={predmet}''')
    conn.commit()


prozor = tkinter.Tk()
prozor.title("Server")
prozor.geometry("700x600")
threadSlanje = threading.Thread(target=slanje)
threadSlanje.start()
frameKomande = Frame(prozor, bd=10)
frameKomande.grid(row=0, column=1)

# gornji frejm sa prijavom
frameIme = LabelFrame(frameKomande)
frameIme.grid(row=0, columnspan=5, sticky="w")
labelaEntry = Label(frameIme, text='Unesite vase ime: ')
labelaEntry.grid(row=0, column=0)
entryIme = Entry(frameIme)
entryIme.grid(row=0, column=1)
dugmePrijavi = Button(frameIme, text='Prijavi se', command=lambda: prijava(entryIme.get()), width=10)
dugmePrijavi.grid(row=0, column=2, padx=5, pady=5)
dugmeOdjavi = Button(frameIme, text='Odjavi se', command=odjava, width=10)
dugmeOdjavi.grid(row=0, column=3, padx=5)
labelPrijava = Label(frameIme, text='Niste prijavljeni', bg='red', fg="white")
labelPrijava.grid(row=1, columnspan=5, pady=3)

# donji frejm sa opcijama
frameOpcije = LabelFrame(frameKomande)
izbor = IntVar()
Radiobutton(
    frameOpcije,
    variable=izbor,
    value=1,
    text='Zakazivanje ispita/kolokvijuma',
    command=prikaziFrejm
).grid(row=0, column=0)
# Radiobutton(
#     frameOpcije,
#     variable=izbor,
#     value=2,
#     text='Zakazivanje kolokvijuma',
#     command=prikaziFrejm
# ).grid(row=0, column=1)
Radiobutton(
    frameOpcije,
    variable=izbor,
    value=2,
    text='Provera statusa studenta',
    command=prikaziFrejm
).grid(row=0, column=2)
Radiobutton(
    frameOpcije,
    variable=izbor,
    value=3,
    text='Izmena ocene studenta',
    command=prikaziFrejm
).grid(row=0, column=3)

# frejm koji se prikaze kad je selektovan RB za zakazivanje
frameZakazivanje = LabelFrame(frameOpcije)
Label(
    frameZakazivanje,
    text='Naziv/sifra predmeta:'
).grid(row=0, column=0, pady=10, sticky="w")
unosPredmet = Entry(frameZakazivanje)
unosPredmet.grid(row=0, column=1)
Label(
    frameZakazivanje,
    text='Datum (DD/MM/YYYY):'
).grid(row=1, column=0, pady=10, sticky="w")
unosDatum = Entry(frameZakazivanje)
unosDatum.grid(row=1, column=1)
Label(
    frameZakazivanje,
    text='Vreme (HH:MM):'
).grid(row=2, column=0, pady=10, sticky="w")
unosVreme = Entry(frameZakazivanje)
unosVreme.grid(row=2, column=1)
izborIspitKlk = IntVar()
Radiobutton(
    frameZakazivanje,
    variable=izborIspitKlk,
    text='Ispit',
    value=1
).grid(row=3, column=0)
Radiobutton(
    frameZakazivanje,
    variable=izborIspitKlk,
    text='Kolokvijum',
    value=2
).grid(row=3, column=1)
Button(
    frameZakazivanje,
    command=zakazivanje,
    text='Potvrdi',
    width=20
).grid(row=4, columnspan=2, pady=5)

# frejm koji se prikaze kad je selektovan RB za informacije o studentu
frameStatus = LabelFrame(frameOpcije)
Label(
    frameStatus,
    text='Unesite broj indeksa studenta: '
).grid(row=0, column=0, pady=10)
unosStudenta = Entry(frameStatus)
unosStudenta.grid(row=0, column=1)
Button(
    frameStatus,
    command=ispis,
    text='Trazi',
    width=20
).grid(row=0, column=2)
ispisStatusa = Text(frameStatus, state=DISABLED)
ispisStatusa.grid(row=1, columnspan=3)
# DODAJ CHECKBOX ZA FILTRITANJE SAMO NEPOLOZENIH PREDMETA

# frejm koji se prikaze kad je selektovan RB za unos ocene
frameOcena = LabelFrame(frameOpcije)
Label(
    frameOcena,
    text='Broj indeksa:'
).grid(row=0, column=0, pady=10, sticky="w")
unosOceneStudent = Entry(frameOcena)
unosOceneStudent.grid(row=0, column=1)
Label(
    frameOcena,
    text='Predmet:'
).grid(row=1, column=0, pady=10, sticky="w")
unosOcenePredmet = Entry(frameOcena)
unosOcenePredmet.grid(row=1, column=1)
Label(
    frameOcena,
    text='Ocena:'
).grid(row=2, column=0, pady=10, sticky="w")
unosOcene = Entry(frameOcena)
unosOcene.grid(row=2, column=1)
Button(
    frameOcena,
    command=izmenaOcene,
    text='Potvrdi',
    width=20
).grid(row=3, columnspan=2)

prozor.mainloop()
