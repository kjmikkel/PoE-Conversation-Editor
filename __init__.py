import os

class GnomeConfig:
  
  OBJECT_POSITION = 0
  LINK_POSITION = 1
  TEXT_POSITION = 2
  SPEAKER_POSITION = 3
  

  current_rep = os.path.dirname(os.path.abspath(__file__))
  current_rep = os.path.join(current_rep, "gui")
  main_gui    = os.path.join(current_rep, "main_editor.glade")
