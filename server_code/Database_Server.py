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
def buchung_eintrag(buchung_daten):
  conn = sqlite3.connect(data_files['datenbank_jugendherbergen.db'])
  cursor = conn.cursor()
  cursor.execute('INSERT INTO tblBuchung (Startzeit, Endzeit, fkZimmer) VALUES (?,?,?)',(buchung_daten[5],buchung_daten[6], buchung_daten[4]))
  conn.commit()
  idBuchung = cursor.fetchone()[0]
  cursor.execute(
      '''
      INSERT INTO tblBuchungBenutzer
      (IDBenutzer, IDBuchung, Benutzerrolle)
      VALUES (?,?,?);
      ''',
    (buchung_daten[0], idBuchung, 'Ersteller')
  )
  conn.commit()
  conn.close()
  