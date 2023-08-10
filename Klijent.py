import tkinter
from tkinter import *
import threading
import socket
from functools import reduce
import time

def sakrij():
    frameOpcije.grid_forget()
    labelPrijava.configure(text='Niste prijavljeni', bg='red')

def popuniLabelu(srOcena):
    s = socket.socket()
    host = socket.gethostname()
    port = 30111
    s.connect((host, port))
    s.sendto(b'Labela+ELITE-70/20', (host, port))
    poruka = s.recv(1024).decode()
    print('dobijeni podaci su ', poruka)
    labelaPodaci.grid_forget()
    labelaPodaci.configure(text=f"""
        Student: David Milovanovic
        Broj indeksa: ELITE-70/20
        Godina: 3   Semestar: 3
        Status: B
        Srednja ocena: {srOcena.__round__(2)}""")
    labelaPodaci.grid(row=0, column=6, padx=5, pady=10)
def ispis():
    ispisPredmeta.configure(state=NORMAL)
    ispisPredmeta.delete('1.0', END)
    tekst = f"""#   Predmet                                    P/N             Ocena
--------------------------------------------------------------------------------
"""
    s = socket.socket()
    host = socket.gethostname()
    port = 30111
    s.connect((host, port))
    s.sendto(b'Predmeti+ELITE-70/20',(host, port))
    poruka = s.recv(1024).decode()
    print(poruka)
    lista = poruka.split("\n")
    listaOcena = []
    print("lista", lista)
    brojac = 0;
    for element in lista:
        if element == '': break
        if element[-2] == ' ':
            listaOcena += element[-1]
        else:
            prva = element[-2]
            druga = element[-1]
            listaOcena.insert(brojac, prva + druga)
        brojac += 1
        print(listaOcena)
    srednjaocena = reduce((lambda x,y: int(x)+int(y)),listaOcena) / len(listaOcena)
    print(srednjaocena)
    s.close()
    popuniLabelu(srednjaocena)
    tekst+=poruka

    # ╔═════════╦═══════╦═════╗
    # ║ Predmet ║ Ocena ║ P/N ║
    # ╠═════════╬═══════╬═════╣
    # ║         ║       ║     ║
    # ╠═════════╬═══════╬═════╣
    # ║         ║       ║     ║
    # ╠═════════╬═══════╬═════╣
    # ║         ║       ║     ║
    # ╚═════════╩═══════╩═════╝
    ispisPredmeta.insert(INSERT, tekst)
    ispisPredmeta.configure(state=DISABLED)

def prikazi():
    frameOpcije.grid_propagate(False)
    frameOpcije.grid(row=1, columnspan=10, pady=5)
    frameDugmici.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
    framePredmeti.grid(
        row=0,
        column=2,
        padx=10,
        pady=10,
        ipadx=5,
        ipady=5,
    )
    ispis()
    labelPrijava.configure(text='Prijavljeni ste', bg='green')

def prikaziFrejm(broj):
    if broj == 1:
        frameZakazivanje.grid_forget()
        framePrijavljeni.grid_forget()
        framePredmeti.grid(
            row=0,
            column=2
        )
        ispis()
    if broj == 2:
        frameZakazivanje.grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            ipadx=5,
            ipady=5,
        )
        framePrijavljeni.grid(
            row=0,
            column=3,
            padx=10,
            pady=10,
        )
        framePredmeti.grid_forget()
        traziIspite()

def traziIspite():
    s = socket.socket()
    host = socket.gethostname()
    port = 30111
    s.connect((host, port))
    s.sendto(b'Ispiti+ELITE-70/20', (host, port))
    poruka = s.recv(1024).decode()
    neprijavljeniPredmeti.grid_forget()
    broj = 0
    neprijavljeniPredmeti.delete(0,neprijavljeniPredmeti.size())
    lista = razvrstaj(poruka)
    for item in lista:
        neprijavljeniPredmeti.insert(broj, item)
        broj += 1
        if len(poruka.split("_")) - 1 == broj: break
    neprijavljeniPredmeti.grid(row=1, column=0, columnspan=2, padx=5, sticky="w")
def razvrstaj(poruka):
    datumi = []
    broj = 0
    for item in poruka.split("_"):
        if item == '': break
        print("item je ", item)
        datum = time.strptime(item.split("+")[1],"%d/%m/%Y %H:%M")
        print(datum)
        datumi.insert(broj, datum)
        broj += 1
    print("datumi pre sortiranje ", datumi)
    datumi.sort()
    print("datumi posle sort ", datumi)
    lista = []
    for datum in datumi:
        for item in poruka.split("_"):
            if item == '': break
            print("trenutni datum ", datum)
            print("trenutni string ", time.strptime(item.split("+")[1],"%d/%m/%Y %H:%M"))
            if datum == time.strptime(item.split("+")[1],"%d/%m/%Y %H:%M"):
                lista.append(f'{item.split("+")[0]} {item.split("+")[1]} {item.split("+")[2]}')
    print("konacna lista: ", lista)
    return lista


def zakaziIspit():
    izabrano = str(neprijavljeniPredmeti.get(ACTIVE))
    izabrano = izabrano[0:izabrano.index("/")-3]
    print(izabrano)
    s = socket.socket()
    host = socket.gethostname()
    port = 30256
    s.connect((host, port))
    s.sendto(b'Prijava+ELITE-70/20', (host, port))
    s.send(izabrano.encode())

prozor = tkinter.Tk()
prozor.title("Klijent")
prozor.geometry("700x600")
frameKomande = Frame(prozor, bd=10)
frameKomande.grid(row=0, column=10)

# gornji frejm sa prijavom
frameIme = LabelFrame(frameKomande, text='Prijave')
frameIme.grid(row=0, columnspan=5, sticky="w")
labelaEntry = Label(frameIme, text='Unesite vas broj indeksa: ')
labelaEntry.grid(row=0, column=0)
entryIme = Entry(frameIme)
entryIme.grid(row=0, column=1)
dugmePrijavi = Button(frameIme, text='Prijavi', command=prikazi, width=10)
dugmePrijavi.grid(row=0, column=2, padx=5, pady=5)
dugmeOdjavi = Button(frameIme, text='Odjavi', command=sakrij, width=10)
dugmeOdjavi.grid(row=0, column=3, padx=5)
labelPrijava = Label(frameIme, text='Niste prijavljeni', bg='red', fg="white")
labelPrijava.grid(row=1, columnspan=5, pady=3)

labelaPodaci = Label(frameKomande)
labelaPodaci.configure(text="""
    Student: 
    Broj indeksa: 
    Godina:    Semestar: 
    Status: 
    Srednja ocena: """, justify=LEFT)
labelaPodaci.grid(row=0, column=6, padx=5, pady=10)

# donji frejm sa opcijama
frameOpcije = LabelFrame(frameKomande, width=680, height=400)
frameDugmici = Frame(frameOpcije)
izbor = IntVar()
Button(
    frameDugmici,
    width=17,
    text='Predmeti',
    command=lambda: prikaziFrejm(1)
)
Button(
    frameDugmici,
    width=17,
    text='Ispiti | Kolokvijumi',
    command=lambda: prikaziFrejm(2)
)

# frejm za prijavu ispita
frameZakazivanje = LabelFrame(frameOpcije, text='Prijava ispita')
neprijavljeniPredmeti = Listbox(
    frameZakazivanje,
    relief=FLAT,
    width=50,
    height=13
)#.grid(row=1, column=0, columnspan=2, padx=5, sticky="w")
Button(
    frameZakazivanje,
    command=zakaziIspit,
    text='Prijavi ispit',
    width=20,
).grid(row=4, columnspan=2, pady=5)
#frejm predstojeci ispiti i kolokvijumi
framePrijavljeni = LabelFrame(frameOpcije, text='Predstojeci ispiti i kolokvijumi')
predstojeci = Text(framePrijavljeni, height=18, width=32, relief=FLAT)
predstojeci.grid()
Button(
    frameZakazivanje,
    text='Otkazi',
    width=20,
    command=lambda: prikaziFrejm(1)).grid(row=5, columnspan=2)


#frejm za pregled svih predmeta
framePredmeti = Frame(frameOpcije)
ispisPredmeta = Text(framePredmeti, height=20, width=80, state=DISABLED)
ispisPredmeta.grid(row=0, columnspan=2, pady=5)
Button(
    framePredmeti,
    text="Ispiti | Kolokvijumi",
    command=lambda: prikaziFrejm(2)
).grid(row=1, column=1, pady=5, sticky="e")

prozor.mainloop()