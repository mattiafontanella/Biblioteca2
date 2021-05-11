import DB as DB
import main as M
import time
import sqlite3


def aggiungiLibro(database):
	print("Inserisci ISBN del libro: \n")
	ISBN = input()
	print("Inserisci il titolo:\n ")
	Titolo = input()
	print("Inserisci anno di pubblicazione: \n")
	AnnoProduzione = input()
	print("Inserisci il numero di copie disponibili: \n")
	Copie = input()
	print("Inserisci autore del libro: \n")
	Autore = input()
	rows=database.select_categorie()
	for row in rows:
		print(row['id']+" \t" + row['nome'])
	print("""Inserisci la categoria del libro tra quelle presenti nel elenco:
			Se non è presente premi invio""")

	id_categoria = input()

	if (id_categoria == ""):
		print("Inserisci il nome della categoria da aggiungere: \n")
		nome_categoria = input()
		database.insert_categoria(nome_categoria)
		database.conn_db.commit()
		id_categoria = database.cursor_db.lastrowid
	id_categoria=int(id_categoria)
	sql = "INSERT INTO Libro(ISBN, IDCategoria, Autore, Titolo, AnnoProduzione, NumeroCopie) " \
		  "VALUES()"
	conn.execute("INSERT INTO Libro(ISBN, IDCategoria, Autore, Titolo, AnnoProduzione, NumeroCopie) VALUES"), (
	ISBN, IDCategoria, Autore, Titolo, AnnoProduzione, Copie)

	M.menu()


def cancellaLibro():
	M.menu()


def visualizzaInventario():
	M.menu()


def aggiungiUtente():
	global utentiAggiunti
	print("Inserisci il nome \n")
	nome = input()
	print("Inserisci il cognome \n")
	cognome = input()
	M.menu()


def visualizzaUtenti():
	M.menu()


def eliminaUtente():
	M.menu()
