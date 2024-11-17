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

    self.extraGuest = []
    # Any code you write here will run before the form opens.
    self.drop_down_1.items = anvil.server.call('get_jugendherbergen')
    self.drop_down_3.items = anvil.server.call('get_user')
    self.drop_down_4.items = anvil.server.call('get_preiskategorie')
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)
    self.drop_down_4.selected_value = anvil.server.call('get_preiskategorieUser', self.drop_down_3.selected_value)
    self.drop_down_5.items = anvil.server.call('get_more_user')
    buchungen = anvil.server.call('get_all_buchung')
    self.repeating_panel_1.items = buchungen
    
  
  def drop_down_4_change(self, **event_args):
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)
    
  def drop_down_3_change(self, **event_args):
    self.drop_down_4.selected_value = anvil.server.call('get_preiskategorieUser', self.drop_down_3.selected_value)
    self.drop_down_2.items = anvil.server.call('get_zimmer', self.drop_down_1.selected_value, self.drop_down_4.selected_value)
    self.drop_down_5.selected_value = self.drop_down_3.selected_value
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
    anvil.server.call('probe')
    

  


  
  def buchung(self):
    JID = self.drop_down_1.selected_value
    GID = self.drop_down_3.selected_value
    PID = self.drop_down_4.selected_value
    ZID = self.drop_down_2.selected_value
    start = self.date_picker_1.date
    end = self.date_picker_2.date
    EGID = self.extraGuest
    return [JID, GID, PID, ZID, start, end, EGID]

  def button_2_click(self, **event_args):
    selected_guest = self.drop_down_5.selected_value
    if (selected_guest == self.drop_down_3.selected_value):
      alert("Sie können sich nicht selber hinzufügen!")
      return
    for item in self.extraGuest:
      if (item == selected_guest):
        alert("Dieser User wurde bereits hinzugefügt!")
        return
    self.extraGuest.append(selected_guest)
    alert("Benutzer wurde erfolgreich hinzugefügt!")

  
    

    
    
 
    
    