from abc import ABC, abstractmethod
import sqlite3



TIMEOUT_CONNECTION=20

DATE_TIME_NOW="datetime('now','localtime')"
DATE_TIME_NOW_MILLIS="strftime('%Y-%m-%d %H:%M:%f', 'now')"

class Sqlite(ABC):
	#costruttore
	def __init__(self,nomefile_db,show_sql=False):
		#apro la connessione col db
		self.conn_db=sqlite3.connect(nomefile_db, detect_types=sqlite3.PARSE_DECLTYPES, timeout=TIMEOUT_CONNECTION)
		#Modifica row factory per usare Row
		self.conn_db.row_factory=sqlite3.Row
		#creo il cursore
		self.cursor_db=self.conn_db.cursor()
		#setup iniziale
		self.cursor_db.executescript('''PRAGMA foreign_keys=ON;''')#non puoi cancellare un record se e' referenziato da un'altra tabella
		self.conn_db.commit()
		#mostra i comandi sql eseguiti
		if show_sql is True:
			self.conn_db.set_trace_callback(print)
		super().__init__()
	
	@abstractmethod
	def schema(self,sql_str):
		"""
		Inserire le istruzioni sql contenenti la dichiarazione delle tabelle (DDL)
		"""
		self.cursor_db.executescript(sql_str)
		self.conn_db.commit()
	
	def close_conn(self):
		self.cursor_db.close()
		self.conn_db.close()
	
def paginazione(first_result,num_results):
	sql=("LIMIT "+str(num_results) if num_results is not None else "")
	sql+=(" OFFSET "+str(first_result) if first_result is not None else "")
	return sql


def add_param_list(lista,prefix):
	params={}
	for index,elem in enumerate(lista):
		params[prefix+str(index)]=elem
	return params
