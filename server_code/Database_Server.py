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

  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Name, JID from tblJugendherberge'))
  print(res)
  return res

@anvil.server.callable
def get_user():
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Vorname || " " || Nachname, GID from tblGast'))
  print(res)
  return res

@anvil.server.callable
def get_preiskategorie():
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Name , PID from tblPreiskategorie'))
  print(res)
  return res

@anvil.server.callable
def get_zimmer(JID, Pk):
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT "Zimmernummer: " || ZID || "Bettenanzahl: " || Schlafplaetze as label, ZID from tblZimmer WHERE  fkJID = ? AND fkPID = ?', (str(JID), str(Pk))))
  print(res)
  return res

@anvil.server.callable
def get_preiskategorieUser(id):
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT fkPID from tblGast WHERE GID = ?', (str(id))))
  item = res[0][0]
  print(item)
  return item

@anvil.server.callable
def get_more_user():
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Vorname || " " || Nachname, GID from tblGast'))
  return res

@anvil.server.callable
def buchung_eintrag(buchung_daten):
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  cursor.execute('INSERT INTO tblBucht (fkGID, fkZID, fkJID, fkPID, DatumStart, DatumEnde) VALUES (?,?,?,?,?,?)',(buchung_daten[1],buchung_daten[3], buchung_daten[0], buchung_daten[2], buchung_daten[4], buchung_daten[5]))
  conn.commit()
  bid = cursor.lastrowid
  for item in buchung_daten[6]:
    cursor.execute('INSERT INTO tblBuchtMIT (fkGID, fkBID) VALUES (?,?)', (item,bid))
  conn.commit()
  conn.close()

@anvil.server.callable
def get_view():
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM BuchungsAnzeige')
  rows = cursor.fetchall()
  conn.close()
  return rows
  
  
  
  
  