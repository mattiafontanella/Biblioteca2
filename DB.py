from Moduli import modulo_sqlite

NOMI_CATEGORIE = ["Informatica", "Economia", "Giallo", "Thriller", "Horror", "Fantasy", "Gangster", "Romanzo", "Storia",
				  "Biografia", "Fantascienza"]
UTENTE_STATO_ATTIVO = "AT"
UTENTE_STATO_BLOCCATO = "BL"


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
	data_insert				TIMESTAMP NOT NULL,
	stato  				     TEXT NOT NULL
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
	datarestituzione		TIMESTAMP,
	datascadenza 			TIMESTAMP NOT NULL,
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
############################################################################################################
	def delete_categoria(self, id):
		sql = """DELETE FROM Categorie
				WHERE id=:id;	
		"""
		self.cursor_db.execute(sql, {
			'id': id
		})

	##############################################################################################################
	def select_utenti(self, id):
		add_id = (id != None)
#Se il valore di id è uguale None restituisce l'intero elenco degli utenti altrimenti se viene inserito un id valido restituisce il singolo utente
		sql = """
SELECT *
FROM Utenti
WHERE 1=1

""" + ('AND id=:id' if add_id is True else '') + """ 
;		
		"""
		params = {}
		if add_id is True:
			params['id'] = id

		self.cursor_db.execute(sql, params)
		return self.cursor_db.fetchall()

	########################################################
	def insert_utenti(self, nome, cognome, stato):
		# DATE_TIME_NOW serve per restituire la data e ore corrente in base al fuso orario
		sql = """
		INSERT INTO Utenti(
			nome,cognome,data_insert,stato
		) VALUES (
			:nome,
			:cognome,
			""" + modulo_sqlite.DATE_TIME_NOW + """,
			:stato
		);
		"""
		self.cursor_db.execute(sql, {
			'nome': nome,
			'cognome': cognome,
			'stato': stato

		})

	################################################################
	def select_libri_categorie(self,id):
		add_id = (id != None)
		sql = """SELECT l.id,l.autore,l.titolo,numerocopie,l.anno,c.nome
FROM Libri l,Categorie c 
WHERE l.id_categoria =c.id 
""" + ('AND l.id=:id' if add_id is True else '') + """ ;"""
		params = {}
		if add_id is True:
			params['id'] = id

		self.cursor_db.execute(sql, params)
		return self.cursor_db.fetchall()
	##############################################################################
	def insert_libri(self, autore, titolo, numerocopie, anno, id_categoria):
		sql = """INSERT INTO Libri(autore,titolo,numerocopie,anno,id_categoria) 
			  VALUES(
			  :autore,:titolo,:numerocopie,:anno,:id_categoria
			);"""
		# Esegue la query
		self.cursor_db.execute(sql, {
			'autore': autore,
			'titolo': titolo,
			'numerocopie': numerocopie,
			'anno': anno,
			'id_categoria': id_categoria
		})

	###################################################################################################
	def select_prestiti_utenti(self, id_utente):
		sql = """
		SELECT *
		FROM Prestiti
		WHERE id_utente=:id_utente;
		"""
		self.cursor_db.execute(sql, {
			'id_utente': id_utente
		})
		return self.cursor_db.fetchall()

	#####################################################################################################
	def delete_libri(self, idLibro):
		sql = """DELETE FROM Libri
						WHERE id=:idLibro ;

				"""
		self.cursor_db.execute(sql, {
			'idLibro': idLibro
		})

	###################################################################################################
	def delete_utenti(self, idUtente):
		sql = """DELETE FROM Utenti
				WHERE id=:idUtente;
		
		"""
		self.cursor_db.execute(sql, {
			'idUtente': idUtente
		})

	###########################################################################################################
	def insert_prestiti(self, datascadenza, id_utente, id_libro):
		sql = """INSERT INTO Prestiti(datainizio,datarestituzione,datascadenza,id_utente,id_libro) 
				  VALUES(
				  """ + modulo_sqlite.DATE_TIME_NOW + """,:datarestituzione,:datascadenza,:id_utente,:id_libro
				);"""
		# Esegue la query
		self.cursor_db.execute(sql, {
			'datarestituzione': None,
			'datascadenza': datascadenza,
			'id_utente': id_utente,
			'id_libro': id_libro

		})

	####################################################################################################################à
	def update_libri_numlibri(self, id_libro, numerocopie):
		sql = """UPDATE Libri
		SET numerocopie=:numerocopie
		WHERE id =:id_libro;
		
		"""
		self.cursor_db.execute(sql, {
			'numerocopie': numerocopie,
			'id_libro': id_libro
		})

	###################################################################################################################à
	def update_utenti(self, id_utente, stato):
		sql = """UPDATE Utenti
		SET stato=:stato
		WHERE id=:id_utente;
		"""
		self.cursor_db.execute(sql, {
			'stato': stato,
			'id_utente': id_utente
		})

	#################################################################################################################
	def select_prestiti_daRestituire(self, id):
		add_id = (id != None)
		sql = """
		SELECT DISTINCT p.id,p.datainizio,p.datarestituzione,p.datascadenza,id_utente,u.nome,u.cognome,id_libro,l.titolo
		FROM Prestiti p,Libri l,Utenti u
		WHERE datarestituzione IS NULL 
		""" + ('AND id=:id' if add_id is True else '') + """
		;		
				"""
		params = {}
		if add_id is True:
			params['id'] = id
		self.cursor_db.execute(sql, params)
		return self.cursor_db.fetchall()


	#####################################################################################################
	def update_prestiti(self, id):
		sql = """UPDATE Prestiti
		SET datarestituzione=""" + modulo_sqlite.DATE_TIME_NOW + """
		WHERE id=:id
		
		"""
		self.cursor_db.execute(sql, {
			'id': id
		})

	#######################################################################################
	def select_prestiti_utenti_libri(self):
		#ORDER BY datarestituzione ISNULL ordina i prestiti mettendo in cima quelli con la datarestituzioe=None
		sql = """
		SELECT p.id,p.datainizio,p.datarestituzione,p.datascadenza,u.id,u.nome,u.cognome,l.id,l.titolo
		FROM Prestiti p,Libri l,Utenti u
		WHERE p.id_utente =u.id
		AND p.id_libro =l.id
		ORDER BY datarestituzione ASC;
		"""
		self.cursor_db.execute(sql, {
		})
		return self.cursor_db.fetchall()
	###################################################################################
	# Restituisce il numero di prestiti ancora da resitutire da un utente
	def select_NumPrestiti(self, id_utente):
		sql = """
		SELECT COUNT(*)
		FROM Prestiti
		WHERE id_utente=:id_utente AND datarestituzione ISNULL ;
		"""
		self.cursor_db.execute(sql, {
			'id_utente': id_utente
		})
		return self.cursor_db.fetchall()
