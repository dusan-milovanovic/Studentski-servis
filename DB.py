import sqlite3
conn = sqlite3.connect('DB.db')
conn.execute("PRAGMA foreign_keys = 1")
print ("Opened database successfully")
conn.execute("DROP TABLE IF EXISTS studenti")
conn.execute('''CREATE TABLE studenti
(ID INT PRIMARY KEY NOT NULL,
IME TEXT NOT NULL,
PREZIME TEXT NOT NULL,
SMER TEXT NOT NULL,
BROJINDEKSA INT NOT NULL,
GODINAUPISA INT NOT NULL,
GODINASTUDIJA INT NOT NULL,
SEMESTAR INT NOT NULL,
FINANSIRANJE CHAR(1) NOT NULL)''')
print ("Table created successfully")
studenti = [(1, 'Dusan', 'Milovanovic', 'ELITE', 70, 20, 3, 6, 'B'), #jedini ima sve sredjeno, test s ovim
(2, 'Ana', 'Djordjevic', 'NRT', 9, 20, 3, 6, 'B'),
(3, 'Dordje', 'Petrovic', 'NRT', 26, 19, 3, 5, 'S')]
conn.executemany('INSERT INTO STUDENTI VALUES (?,?,?,?,?,?,?,?,?)', studenti)
print ("Records created successfully")
cursor = conn.execute("SELECT ID,IME,PREZIME,SMER from STUDENTI")
for row in cursor:
    print ("ID = ", row[0])
    print ("IME = ", row[1])
    print ("PREZIME = ", row[2])
    print ("SMER = ", row[3], "\n")
    print ("Operation done successfully")
conn.execute("DROP TABLE IF EXISTS predmeti")
conn.execute('''CREATE TABLE predmeti
(SIFRAPREDMETA INT PRIMARY KEY NOT NULL,
IMEPREDMETA TEXT NOT NULL,
PROVERA TEXT,
VREME TEXT)''')
predmeti = [(301256, 'Funkcionalno programiranje', '', ''),
(156856, 'Programabilna logicka kola', '', ''),
(204589, 'Digitalna elektronika', '', ''),
(104896, 'Algoritmi i strukture podataka', '', ''),
(305698, 'Veb dizajn', '', ''),
(105869, 'Mikrokontroleri', '', ''),
(201456, 'Internet inteligentnih uredjaja', '', ''),
(301448, 'Telekomunikacioni servisi i tehnologije', '', '')]
conn.executemany('INSERT INTO PREDMETI VALUES (?,?,?,?)', predmeti)
student = "ELITE7020"
conn.execute(f"DROP TABLE IF EXISTS PREDMETI{student}")
conn.execute(f'''CREATE TABLE PREDMETI{student}
(STUDENT INT,
PREDMET INT,
OCENA INT,
STATUS TEXT NOT NULL DEFAULT "Nije polozio",
PRIJAVLJEN INT,
FOREIGN KEY (PREDMET) REFERENCES predmeti(SIFRAPREDMETA),
FOREIGN KEY (STUDENT) REFERENCES studenti(ID))''')
ubaci = [(1, 301256, 5, 'Nije polozio', 0),
(1, 201456, 8, 'Polozio', 0),
(1, 301448, 10, 'Polozio', 0)
(1, 105869, 5, 'Nije polozio', 0)]
conn.executemany(f"INSERT INTO PREDMETI{student} VALUES (?,?,?,?,?)", ubaci)
cursor = conn.execute(f"SELECT * FROM PREDMETIELITE7020")
for row in cursor:
    print ("STUDENT = ", row[0])
    print ("PREDMET = ", row[1])
    print("OCENA = ", row[2], "\n")
conn.commit()
conn.close()

