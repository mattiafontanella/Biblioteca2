from Moduli import modulo_sqlite

NOMI_CATEGORIE = ["Informatica", "Economia", "Giallo", "Thriller", "Horror", "Fantasy", "Gangster", "Romanzo", "Storia", "Biografia", "Fantascienza"]

class Database(modulo_sqlite.Sqlite):
	'''
	select
	count
	insert
	update
	delete
	'''

	# costruttore
	def __init__(self, nomefile_db):
		super().__init__(nomefile_db)

	# metodi
	def schema(self):
		sql = """
CREATE TABLE Utenti(
	id						INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome				TEXT NOT NULL,
	cognome					TEXT NOT NULL,
	data_insert				TIMESTAMP NOT NULL
);

CREATE TABLE Categorie(
	id					INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome				TEXT NOT NULL
);


CREATE TABLE Libri(
	id						INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	autore					TEXT NOT NULL,
	titolo					TEXT NOT NULL,
	numerocopie				INTEGER NOT NULL,
	anno					INTEGER NOT NULL,
	id_categoria INTEGER NOT NULL,
	CONSTRAINT FK_Libri_Categorie FOREIGN KEY(id_categoria) REFERENCES Categorie(id)
	ON UPDATE NO ACTION
	ON DELETE RESTRICT
);

CREATE TABLE Prestiti(
	id						INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	datainizio				TIMESTAMP NOT NULL,
	datascadenza				TIMESTAMP NOT NULL,
	id_utente INTEGER NOT NULL,
	id_libro INTEGER NOT NULL,
	CONSTRAINT FK_Prestiti_Utenti FOREIGN KEY(id_utente) REFERENCES Utenti(id)
	ON UPDATE NO ACTION
	ON DELETE RESTRICT,
	CONSTRAINT FK_Prestiti_Libri FOREIGN KEY(id_libro) REFERENCES Libri(id)
	ON UPDATE NO ACTION
	ON DELETE RESTRICT
	
);

"""
		super().schema(sql)

	##############################################
###############################################################################
	def select_account_biy_status(self, status):
		sql = """
SELECT *
FROM Utenti
WHERE status=:status
;
SELECT *
FROM Categorie
WHERE status=:status
;
SELECT *
FROM Libri
WHERE status=:status
;
SELECT *
FROM Prestiti
WHERE status=:status
;


"""
		self.cursor_db.execute(sql, {
			'status': status
		})
		return self.cursor_db.fetchone()

	#############################################################################################################################
	def insert_categoria(self, nome):
		sql = """
INSERT INTO Categorie(
	nome 
) VALUES (
	:nome
);
"""
		self.cursor_db.execute(sql, {
			'nome': nome
		})

