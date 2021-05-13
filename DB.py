from Moduli import modulo_sqlite

NOMI_CATEGORIE = ["Informatica", "Economia", "Giallo", "Thriller", "Horror", "Fantasy", "Gangster", "Romanzo", "Storia",
				"Biografia", "Fantascienza"]


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
	nome				    TEXT NOT NULL,
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
	def select_categorie(self):
		sql = """
SELECT *
FROM Categorie
;
"""
		self.cursor_db.execute(sql, {
		})
		return self.cursor_db.fetchall()

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

	##############################################################################################################
	def select_utenti(self):
		sql = """
SELECT *
FROM Utenti
;		
		"""
		self.cursor_db.execute(sql, {
		})
		return self.cursor_db.fetchall()

	########################################################
	def insert_utenti(self, nome, cognome):
		#DATE_TIME_NOW serve per restituire la data e ore corrente in base al fuso orario
		sql = """
		INSERT INTO Utenti(
			nome,cognome,data_insert
		) VALUES (
			:nome,
			:cognome,
			"""+modulo_sqlite.DATE_TIME_NOW+"""
		);
		"""
		self.cursor_db.execute(sql, {
			'nome': nome,
			'cognome':cognome

		})

################################################################
	def select_libri(self):
		sql="""SELECT l.id,l.autore,l.titolo,l.numerocopie,l.anno,c.nome
FROM Libri l,Categorie c 
WHERE l.id_categoria =c.id;"""
		self.cursor_db.execute(sql, {
		})
		return self.cursor_db.fetchall()

###########################################################################
	def insert_libri(self,autore,titolo,numerocopie,anno,id_categoria):
		sql = """INSERT INTO Libri(autore,titolo,numerocopie,anno,id_categoria) 
			  VALUES(
			  :autore,:titolo,:numerocopie,:anno,:id_categoria
			);"""
		# Esegue la query
		self.cursor_db.execute(sql, {
			'autore': autore,
			'titolo':titolo,
			'numerocopie':numerocopie,
			'anno':anno,
			'id_categoria':id_categoria

		})
#####################################################################################################