from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.drop_down_1.items = anvil.server.call('get_jugendherbergen')
    self.drop_down_3.items = anvil.server.call('get_user')
    self.drop_down_4.items = anvil.server.call('get_preiskategorie')
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)
    self.drop_down_4.selected_value = anvil.server.call('get_preiskategorieUser', self.drop_down_3.selected_value)
    

  def drop_down_4_change(self, **event_args):
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)
    
  def drop_down_3_change(self, **event_args):
    self.drop_down_4.selected_value = anvil.server.call('get_preiskategorieUser', self.drop_down_3.selected_value)
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)
  def drop_down_1_change(self, **event_args):
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)

  def date_picker_1_change(self, **event_args):
    self.date_picker_2.min_date = self.date_picker_1.date 
    

  def date_picker_2_change(self, **event_args):
    if (self.date_picker_1.date == None):
      self.date_picker_1.max_date = self.date_picker_2.date
    

  def button_1_click(self, **event_args):
    if (self.date_picker_1.date == None or self.date_picker_2.date == None):
      print("Bitte alle Felder ausfüllen")
    else:
      buchungDaten = self.buchung()
      anvil.server.call('buchung_eintrag',buchungDaten)
    return buchungDaten


  
def buchung(self):
  JID = self.drop_down_1.selected.value
  BID = self.drop_down_3.selected.value
  PKID = self.drop_down_4.selected.value
  ZID = self.drop_down_2.selected.value
  start = self.date_picker_1.date
  end = self.date_picker_2.date
  return [JID, BID, PKID, ZID, start, end]
 
    
    