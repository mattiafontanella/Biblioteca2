import main as M
import Funzioni as F


def stampaMenu():
	print("Seleziona una voce del menu: \n"
		  "1- Prestito/Restituzione libro \n"
		  "2- Aggiungi/Cancella Categoria \n"
		  "3- Aggiungi/Cancella Utente\n"
		  "4- Aggiungi/Cancella Libro\n"
		  "5- Inventario\n"
		  "6- Esci\n")


def scelta1(database):
	print("che operazione devi eseguire? \n"
		  "1- Richiedi un prestito un libro \n"
		  "2- Restituisci un libro \n"
		  "3- Torna al menù principale\n")
	scelta = input()
	while (scelta != '1' and scelta != '2' and scelta != '3'):
		print("che operazione devi eseguire? \n"
			  "1- Richiedi un prestito un libro \n"
			  "2- Restituisci un libro \n"
			  "3- Torna al menù principale\n")
		scelta = input()

	if (scelta == '1'):
		F.effettuaPrestito(database)
	if (scelta == '2'):
		print("Funzione 2 attivata")
	if (scelta == '3'):
		M.menu(database)


def scelta2(database):
	print("che operazione devi eseguire? \n"
		  "1- Aggiungi categoria \n"
		  "2- Cancella categoria \n"
		  "3- Torna al menù principale\n")
	scelta = input()
	while (scelta != '1' and scelta != '2' and scelta != '3'):
		print("che operazione devi eseguire? \n"
			  "1- Aggiungi categoria \n"
			  "2- Cancella categoria \n"
			  "3- Torna al menù principale\n")
		scelta = input()

	if (scelta == '1'):
		print("Funzione 1 attivata")
	if (scelta == '2'):
		print("Funzione 2 attivata")
	if (scelta == '3'):
		M.menu(database)


def scelta3(database):
	print("che operazione devi eseguire? \n"
		  "1- Aggiungi utente \n"
		  "2- Cancella utente\n"
		  "3- visualizza utenti registrati\n"
		  "4- Torna al menù principale\n")
	scelta = input()
	while (scelta != '1' and scelta != '2' and scelta != '3'):
		print("che operazione devi eseguire? \n"
			  "1- Aggiungi utente \n"
			  "2- Cancella utente\n"
			  "3- visualizza utenti registrati\n"
			  "4- Torna al menù principale\n")
		scelta = input()

	if (scelta == '1'):
		F.aggiungiUtente(database)
	if (scelta == '2'):
		F.eliminaUtente(database)
	if (scelta == '3'):
		F.visualizzaUtenti(database)
	if (scelta == '4'):
		M.menu(database)


def scelta4(database):
	print("che operazione devi eseguire? \n"
		  "1- Aggiungi libro\n"
		  "2- Cancella libro\n"
		  "3- Torna al menù principale\n")
	scelta = input()
	while scelta != '1' and scelta != '2' and scelta != '3':
		print("che operazione devi eseguire? \n"
			  "1- Aggiungi libro\n"
			  "2- Cancella libro\n"
			  "3- Torna al menù principale\n")
		scelta = input()

	if scelta == '1':
		F.aggiungiLibro(database)

	if scelta == '2':
		F.cancellaLibro(database)
	if scelta == '3':
		M.menu(database)


def scelta5(database):
	print("Inventario biblioteca: ")
	F.visualizzaInventario(database)


def scelta6(database):
	print("Grazie di aver utilizzato il programma")
	database.close_conn()
	exit()
