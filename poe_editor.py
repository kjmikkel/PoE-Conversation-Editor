#!/usr/bin/python

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

import gobject
import pango
import os
import re
import time
import sys
import xml.etree.ElementTree as etree

from __init__ import GnomeConfig
from conv_tree import ConvTree

class GUI(object):

  def __init__(self):
    self.__init_gui()
    gtk.main()

  def __init_gui(self):
    self.__init__aliases()
    self.__init__basic_setup()
    self.__init__connections()

  def __init__aliases(self):
    self.builder = gtk.Builder()
    self.builder.add_from_file(GnomeConfig.main_gui)
    self.gui = self.builder.get_object('main_window')
    self.conv_area = self.builder.get_object('conv_area')

    # The expanded fields
    self.default_text = self.builder.get_object('default_text')
    self.female_text  = self.builder.get_object('female_text')

    # The checkboxes
    self.skippable_check    = self.builder.get_object('skippable_check')
    self.question_check    = self.builder.get_object('question_check')
    self.persistence_check = self.builder.get_object('persistence_check')
    self.display_check     = self.builder.get_object('display_check')


  def __init__basic_setup(self):
    conversation = gtk.TreeStore(object, object, str)
    self.conv_tree = ConvTree(self, conversation)
    self.conv_area.add(self.conv_tree)

  def __init__connections(self):
    SIGNAL_CONNECTIONS_DIC = {
      "on_destroy": self.destroy,
      "on_load": self.on_load,
      "button-press-event": self.button_press
                              }
    self.builder.connect_signals(SIGNAL_CONNECTIONS_DIC)
    
    # Add listeners   
    self.gui.connect("key-press-event", self.button_press)
    self.conv_tree.connect("cursor-changed", self.cursor_changed, None)

  def line_selected(self):
    tree_store, tree_iter = self.conv_tree.get_selection().get_selected()
    model = self.conv_tree.get_model()

    if tree_iter:
      return model.get_path(tree_iter) 
    else:
      return None

  def button_press(self, widget, ev):
    try:
      selected = self.line_selected()
      if ev.keyval == 65361L and selected:
        self.conv_tree.collapse_row(selected)
      
      elif ev.keyval == 65363L and selected:
        self.conv_tree.expand_to_path(selected)
    except AttributeError:
      pass

  def cursor_changed(self, conv_tree, user_data):
    if conv_tree:
      selection = conv_tree.get_selection()
      if selection:
        tree_store, tree_iter = selection.get_selected()
        model = conv_tree.get_model()

        if tree_iter:
          value = model.get_value(tree_iter, GnomeConfig.OBJECT_POSITION)
          self.set_field_value(value)
        else:
          self.reset_field_value()
      else:
        self.reset_field_value()
    else:
      self.reset_field_value()
          # We set the values

  def set_textview_text(self, textview, text):
    text_buffer = textview.get_buffer()
    if text:
      text_buffer.set_text(text)
    else:
      text_buffer.set_text('')

  def reset_field_value(self):
    self.set_textview_text(self.default_text, '')
    self.set_textview_text(self.female_text,'')

    self.default_text.set_sensitive(False)
    self.female_text.set_sensitive(False)

    self.active_check_set(self.skippable_check, None)
    self.active_check_set(self.question_check, None)
    self.active_check_set(self.persistence_check, None)
    self.active_check_set(self.display_check, None)

  def set_field_value(self, value):
    self.set_textview_text(self.default_text, value.default_text)
    self.set_textview_text(self.female_text, value.female_text)

    self.default_text.set_sensitive(True)
    self.female_text.set_sensitive(True)

    self.active_check_set(self.skippable_check, value.not_skippable)
    self.active_check_set(self.question_check, value.is_question_node)
   # self.active_check_set(self.is_temp
    

  def destroy(self, widget):
    gtk.main_quit()
    return 0

  # The methods used for interacting with the system
  def on_load(self, widget):
   conv = os.path.dirname(os.path.realpath(__file__)) + "/00_cv_lord_harond.stringtable"
   self.conv_tree.load_conversation_file(conv)

  def active_check_set(self, check_box, value):
    if value != None:
      check_box.set_sensitive(True)
      check_box.set_active(value)
    else: 
      check_box.set_sensitive(False)
      check_box.set_active(False)
#try:
  #GUI())
#except KeyboardInterrupt:
#  sys.exit(1)
GUI()
