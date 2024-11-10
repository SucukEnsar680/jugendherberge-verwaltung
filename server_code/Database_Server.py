import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def get_jugendherbergen():

  conn = sqlite3.connect(data_files['datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Name, IDJugendherberge from tblJugendherberge'))
  print(res)
  return res

@anvil.server.callable
def get_user():
  conn = sqlite3.connect(data_files['datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Vorname || " " || Nachname, IDBenutzer from tblBenutzer'))
  print(res)
  return res

@anvil.server.callable
def get_preiskategorie():
  conn = sqlite3.connect(data_files['datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Preis || "€" as Label, IDPreiskategorie from tblPreiskategorie'))
  print(res)
  return res

@anvil.server.callable
def get_zimmer(JID, Pk):
  conn = sqlite3.connect(data_files['datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT "Zimmernummer: " || IDZimmer || "Bettenanzahl: " || MaxBettenanzahl as label, IDZimmer from tblZimmer WHERE  fkJugendherberge = ? AND fkPreiskategorie = ?', (str(JID), str(Pk))))
  print(res)
  return res

@anvil.server.callable
def get_preiskategorieUser(id):
  conn = sqlite3.connect(data_files['datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT fkPreiskategorie from tblBenutzer WHERE IDBenutzer = ?', (str(id))))
  item = res[0][0]
  print(item)
  return item

@anvil.server.callable
def get_user2(id):
  conn = sqlite3.connect(data_files['datenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Vorname || " " || Nachname, IDBenutzer from tblBenutzer WHERE IDBenutzer != ? ', (str(id))))
  print(res)
  return res

