import main as M


def aggiungiLibro(database):
	print("Inserisci autore del libro: \n")
	autore = input()
	print("Inserisci il titolo:\n ")
	titolo = input()
	print("Inserisci anno di pubblicazione: \n")
	anno = int(input())
	print("Inserisci il numero di copie disponibili: \n")
	numerocopie= int(input())

	rows=database.select_categorie()
	for row in rows:
		print('{0}\t{1}'.format(row['id'],row['nome']))
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
	database.insert_libri(autore,titolo,numerocopie,anno,id_categoria)
	database.conn_db.commit()
	M.menu()


def cancellaLibro(database):
	M.menu()


def visualizzaInventario(database):
	M.menu()


def aggiungiUtente(database):

	print("Inserisci il nome \n")
	nome = input()
	print("Inserisci il cognome \n")
	cognome = input()
	database.insert_utenti(nome,cognome)
	database.conn_db.commit()
	M.menu()


def visualizzaUtenti(database):
	rows = database.select_utenti()
	for row in rows:
		print('{0}\t{1}\t{2}'.format(row['id'],row['nome'],row['cognome']))#Coverte automaticamente il tipo di dato restituito
	M.menu()


def eliminaUtente(database):
	M.menu()
