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
		anno = int(anno)
	except ValueError:
		print("Errore nel inserimento del anno ")
		Menu.scelta4(database)

	print("Inserisci il numero di copie disponibili: \n")
	numerocopie = input()
	try:
		numerocopie = int(numerocopie)
	except ValueError:
		print("Errore nel inserimento del numero delle copie ")
		Menu.scelta4(database)

	rows = database.select_categorie()
	for row in rows:
		print('{0}\t{1}'.format(row['id'], row['nome']))
	print("""Inserisci la categoria del libro tra quelle presenti nel elenco: \n Se non è presente premi invio""")

	id_categoria = input()
	if (id_categoria == ""):
		print("Inserisci il nome della categoria da aggiungere: \n")
		nome_categoria = input()
		database.insert_categoria(nome_categoria)
		database.conn_db.commit()
		id_categoria = database.cursor_db.lastrowid
	try:
		id_categoria = int(id_categoria)
	except ValueError:
		print("Errore nel inserimento del id categoria ")
		Menu.scelta4(database)
	database.insert_libri(autore, titolo, numerocopie, anno, id_categoria)
	database.conn_db.commit()
	M.menu(database)


def cancellaLibro(database):
	print("Seleziona dal elenco il libro da eliminare: ")
	rows = database.select_libri_categorie(None)
	# tabulete crea una tabella per migliorare la visulizzazione dei nostri dati
	print(tabulate(rows, headers=["ID", "autore", "titolo", "Numero copie", "Anno produzione", "Categoria"],
				   tablefmt="github"))
	id = input()
	# controllo che il numero inserito sia un intero altrimenti genero un errore
	try:

		id = int(id)
	except ValueError:
		print("Errore inserirsci un id corretto! ")
		Menu.scelta4(database)
	try:
		database.delete_libri(id)
	except:
		print("Impossibile eliminare la categoria perchè è già stata utilizzata in un altra tabella ")
		Menu.scelta2(database)
	database.conn_db.commit()
	M.menu(database)


def visualizzaInventario(database):
	rows = database.select_libri_categorie(None)
	print(tabulate(rows, headers=["ID", "autore", "titolo", "Numero copie", "Anno produzione", "Categoria"], tablefmt="github"))
	M.menu(database)


def aggiungiUtente(database):
	print("Inserisci il nome \n")
	nome = input()
	print("Inserisci il cognome \n")
	cognome = input()
	database.insert_utenti(nome, cognome, DB.UTENTE_STATO_ATTIVO)
	database.conn_db.commit()
	M.menu(database)


def visualizzaUtenti(database):
	rows = database.select_utenti(None)
	# tabulete crea una tabella per migliorare la visulizzazione dei nostri dati
	print(tabulate(rows, headers=["ID", "Nome", "Cognome", "Data registrazione", "Bloccato"], tablefmt="github"))
	M.menu(database)


def eliminaUtente(database):
	rows = database.select_utenti(None)
	print("Quali tra i seguenti utenti vuoi eliminare? ")
	print(tabulate(rows, headers=["ID", "Nome", "Cognome", "Data registrazione", "Stato"], tablefmt="github"))
	id = input()
	# controllo che il numero inserito sia un intero altrimenti genero un errore
	try:
		id = int(id)
	except ValueError:
		print("Errore inserirsci un id corretto! ")
		Menu.scelta3(database)

	try:
		database.delete_utenti(id)
	except:
		print("Impossibile eliminare utente perchè è già stato utilizzato in un altra tabella ")
		Menu.scelta2(database)
	database.conn_db.commit()
	M.menu(database)


def effettuaPrestito(database):
	print("Quale utente deve effettuare il prestito:\n")
	rows = database.select_utenti(None)
	# tabulete crea una tabella per migliorare la visulizzazione dei nostri dati
	print(tabulate(rows, headers=["ID", "Nome", "Cognome", "Data registrazione", "stato"], tablefmt="github"))
	idUtente = input()
	print("Quale libro deve essere preso in prestito: \n")
	rows = database.select_libri_categorie(None)
	print(tabulate(rows, headers=["ID", "autore", "titolo", "Numero copie", "Anno produzione", "Categoria"],tablefmt="github"))
	idLibro = input()
	try:
		idLibro = int(idLibro)
		idUtente = int(idUtente)
	except ValueError:
		print("Errore inserirsci un id corretto! \n")
		Menu.scelta3(database)
	UtenteIsbloccato(database, idUtente)
	rows = database.select_libri_categorie(idLibro)
	numeroCopie = 0
	for row in rows:
		numeroCopie = row['numerocopie']
	rows = database.select_utenti(idUtente)
	stato = None
	NumPrenotazioniAttive = None
	for row in rows:
		stato = row['stato']
	rows = database.select_NumPrestiti(idUtente)
	for row in rows:
		NumPrenotazioniAttive = row[0]
	if numeroCopie > 0 and stato == DB.UTENTE_STATO_ATTIVO and NumPrenotazioniAttive < 5:
		database.update_libri_numlibri(idLibro, numeroCopie - 1)
		database.insert_prestiti(__calcola_data_scadenza_prestito(), idUtente, idLibro)
		#Mantiene in memoria i dati nel database
		database.conn_db.commit()
	if numeroCopie <= 0:
		print("Non sono più disponibili copie per questo libro\n")
	if stato == DB.UTENTE_STATO_BLOCCATO:
		print("Non è stato possibile effettuare il prestito perchè l'utente è stato bloccato\n")
	if NumPrenotazioniAttive == 5:
		print("è stato superato il numero massimo di libri presi in presitito\n")

	M.menu(database)


def __calcola_data_scadenza_prestito():
	# Calcolo la data di scadenza basandomi sulla data attuale e sommando due giorni
	dataScadenza = datetime.datetime.now() + datetime.timedelta(days=30)
	return dataScadenza


# Con questa funzione verifico se un utente debba essere bloccato
def UtenteIsbloccato(database, idUtente):
	rows = database.select_prestiti_utenti(idUtente)
	datascadenza = None
	datarestituzione = None
	for row in rows:
		datascadenza = row['datascadenza']
		datarestituzione = row['datarestituzione']
		# Controllo che non sia ancora stato restituito un libro
		if datarestituzione == None:
			if datascadenza < datetime.datetime.now():
				database.update_utenti(idUtente, DB.UTENTE_STATO_BLOCCATO)
				database.conn_db.commit()


def restituzione(database):
	rows = database.select_prestiti_daRestituire(None)
	for row in rows:
		id_utente = row['id_utente']
		id_libro = row['id_libro']
		UtenteIsbloccato(database, id_utente)

	print(tabulate(rows, headers=["ID", "Data inizio", "Data Restituzione", "Data scedenza", "ID utente", "Nome","Cognome","ID Libro","Titolo"],tablefmt="github"))

	print("Inserisci il libro da restituire:")
	ID = input()
	rows= database.select_libri_categorie(id_libro)
	numerocopie=0
	for row in rows:
		numerocopie=row['numerocopie']
	database.update_libri_numlibri(id_libro,numerocopie+1)
	database.update_prestiti(ID)
	database.conn_db.commit()
	M.menu(database)


def storicoPresitti(database):
	rows = database.select_prestiti_utenti_libri()
	print(tabulate(rows, headers=["ID", "Data inizio", "Data Restituzione", "Data scedenza", "ID utente", "Nome","Cognome","ID Libro","Titolo"],tablefmt="github"))
	M.menu(database)


def aggiungiCategoria(database):
	print("Inserisci il nome della categoria da aggiungere")
	categoria = input()
	database.insert_categoria(categoria)
	database.conn_db.commit()
	M.menu(database)


def cancellaCategoria(database):
	rows = database.select_categorie()
	for row in rows:
		print('{0}\t{1}'.format(row['id'], row['nome']))
	print("""Inserisci id della categoria da cancellare :""")
	id = input()
	try:
		id = int(id)
	except ValueError:
		print("Errore nel inserimento del id categoria ")
		Menu.scelta2(database)
	try:
		database.delete_categoria(id)
	except:
		print("Impossibile eliminare la categoria perchè è già stata utilizzata in un altra tabella ")
		Menu.scelta2(database)
	M.menu(database)