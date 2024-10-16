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
def get_jugendherbergen(rows='*'):

  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung2.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {rows} FROM jugendherbergen'))
  print(res)
  return res

def get_zimmer_for_jugendgerberge(jid, columns="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung2.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {columns} FROM zimmer WHERE JID = {jid}'))
  print(res)
  conn.close()
  return res