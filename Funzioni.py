import DB as DB
import main as M
import time
import sqlite3


def aggiungiLibro () :
    conn = sqlite3.connect("DB\Biblioteca.db")
    print("Inserisci ISBN del libro: \n")
    ISBN=input()
    print("Inserisci il titolo:\n ")
    Titolo = input()
    print("Inserisci anno di pubblicazione: \n")
    AnnoProduzione=input()
    print("Inserisci il numero di copie disponibili: \n")
    Copie = input()
    print("Inserisci autore del libro: \n")
    Autore = input()
    cur = conn.cursor()
    conn.execute("SELECT * FROM Categoria ")
    rows=conn.fetchall()
    for row in rows:
        print(row)
    print("Inserisci la categoria del libro tra quelle presenti nel elenco: \n"
          "Se non è presente premi invio\n ")

    scelta= input()



    if (scelta=="") :
        print("Inserisci il nome della categoria da aggiungere: \n")
        scelta=input()
        sql = "INSERT INTO Categoria(Nome) " \
              "VALUES(Diritto)"
        conn.execute(sql)

    cur.execute("SELECT IDCategoria FROM Categoria WHERE Nome =?",(scelta,))
    IDCategoria= cur.fetchall()
    sql = "INSERT INTO Libro(ISBN, IDCategoria, Autore, Titolo, AnnoProduzione, NumeroCopie) " \
          "VALUES()"
    conn.execute("INSERT INTO Libro(ISBN, IDCategoria, Autore, Titolo, AnnoProduzione, NumeroCopie) VALUES"),(ISBN,IDCategoria,Autore,Titolo,AnnoProduzione,Copie)

    M.menu()

def cancellaLibro () :
    M.menu()


def visualizzaInventario () :
    M.menu()

def aggiungiUtente():
    global utentiAggiunti
    print("Inserisci il nome \n")
    nome=input()
    print("Inserisci il cognome \n")
    cognome=input()
    M.menu()

def visualizzaUtenti():
    M.menu()
def eliminaUtente():
    M.menu()
