import datetime
import main as M
from tabulate import tabulate
import Menu as Menu
import DB


def aggiungiLibro(database):
	print("Inserisci autore del libro: \n")
	autore = input()
	print("Inserisci il titolo:\n ")
	titolo = input()
	print("Inserisci anno di pubblicazione: \n")
	anno = input()
	try:
		int(anno)
	except ValueError:
		print("Errore nel inserimento del anno ")
		Menu.scelta4(database)

	print("Inserisci il numero di copie disponibili: \n")
	numerocopie= input()
	try:
		int(numerocopie)
	except ValueError:
		print("Errore nel inserimento del numero delle copie ")
		Menu.scelta4(database)

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
	M.menu(database)


def cancellaLibro(database):
	print("Seleziona dal elenco il libro da eliminare: ")
	rows= database.select_libri_categorie()
	#tabulete crea una tabella per migliorare la visulizzazione dei nostri dati
	print(tabulate(rows,headers=["ID", "autore","titolo","Numero copie","Anno produzione","Categoria"], tablefmt="github"))
	id = input()
	# controllo che il numero inserito sia un intero altrimenti genero un errore
	try:
		int(id)
	except ValueError:
		print("Errore inserirsci un id corretto! ")
		Menu.scelta4(database)
	database.delete_libri(id)
	database.conn_db.commit()
	M.menu(database)


def visualizzaInventario(database):
	rows= database.select_libri_categorie()
	print(tabulate(rows,headers=["ID", "autore","titolo","Numero copie","Anno produzione","Categoria"], tablefmt="github"))
	M.menu(database)


def aggiungiUtente(database):

	print("Inserisci il nome \n")
	nome = input()
	print("Inserisci il cognome \n")
	cognome = input()
	database.insert_utenti(nome,cognome)
	database.conn_db.commit()
	M.menu(database)


def visualizzaUtenti(database):
	rows = database.select_utenti()
	# tabulete crea una tabella per migliorare la visulizzazione dei nostri dati
	print(tabulate(rows,headers=["ID","Nome","Cognome","Data registrazione", "Bloccato"],tablefmt="github"))
	M.menu(database)


def eliminaUtente(database):
	rows = database.select_utenti()
	print("Quali tra i seguenti utenti vuoi eliminare? ")
	print(tabulate(rows,headers=["ID","Nome","Cognome","Data registrazione", "Stato"],tablefmt="github"))
	id=input()
	#controllo che il numero inserito sia un intero altrimenti genero un errore
	try:
		int(id)
	except ValueError:
		print("Errore inserirsci un id corretto! ")
		Menu.scelta3(database)
	database.delete_utenti(id)
	database.conn_db.commit()

def effettuaPrestito(database):
	print("Quale utente deve effettuare il prestito:\n")
	rows = database.select_utenti()
	# tabulete crea una tabella per migliorare la visulizzazione dei nostri dati
	print(tabulate(rows, headers=["ID", "Nome", "Cognome", "Data registrazione", "stato"], tablefmt="github"))
	idUtente = input()
	print("Quale libro deve essere preso in prestito: \n")
	rows= database.select_libri_categorie()
	print(tabulate(rows,headers=["ID", "autore","titolo","Numero copie","Anno produzione","Categoria"], tablefmt="github"))
	idLibro = input()
	try:
		int(idLibro)
		int(idUtente)
	except ValueError:
		print("Errore inserirsci un id corretto! \n")
		Menu.scelta3(database)
	rows= database.select_libri(idLibro)
	numeroCopie=0
	for row in rows:
		numeroCopie=row['numerocopie']
	rows= database.select_utenti(idUtente)
	stato=None
	for row in rows:
		stato=row['stato']

	if numeroCopie>0 and stato==DB.UTENTE_STATO_ATTIVO:
		database.update_libri_numlibri(idLibro,numeroCopie-1)
		database.insert_prestiti(__calcola_data_scadenza_prestito(),idUtente,idLibro)
	else:
		print("Non è stato possibile eseguire il presito\n")

	M.menu(database)

def __calcola_data_scadenza_prestito():
	# Calcolo la data di scadenza basandomi sulla data attuale e sommando due giorni
	dataScadenza = datetime.datetime.now() + datetime.timedelta(days=5)
	return dataScadenza