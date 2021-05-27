import Menu as M
import DB as DB
import os
from Moduli import modulo_funzioni


def apri_connessione_db():
	# ABSpath serve ad avere il percorso assoluto del file corrente
	# dirname serve a fare riferimento alla cartella corrente del file
	path_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DB", "Biblioteca.db")
	is_db_new = modulo_funzioni.dimensione_file(path_db) <= 0
	database = DB.Database(path_db)
	if is_db_new:
		database.schema()
		# Inserisco le categorie
		for nome in DB.NOMI_CATEGORIE:
			database.insert_categoria(nome)
		database.conn_db.commit()
	return database


def menu(database):
	M.stampaMenu()

	scelta = input()
	while (scelta != '1' and scelta != '2' and scelta != '3' and scelta != '4' and scelta != '5' and scelta != '6'):
		M.stampaMenu()
		scelta = input()

	if (scelta == '1'):
		M.scelta1(database)
	if (scelta == '2'):
		M.scelta2(database)
	if (scelta == '3'):
		M.scelta3(database)
	if (scelta == '4'):
		M.scelta4(database)
	if (scelta == '5'):
		M.scelta5(database)
	if (scelta == '6'):
		M.scelta6(database)


if __name__ == '__main__':
	database = apri_connessione_db()
	menu(database)
