#!/usr/bin/python

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from __init__ import GnomeConfig

from poe_conv_node import poe_conv_node
import pango
import xml.etree.ElementTree as etree
import os

class ConvTree(gtk.TreeView):

  def __init__(self, gui,  model=None):
    gtk.TreeView.__init__(self)
    self.__init__connections()
    self.columns = []
    self.gui = gui
    self.set_reorderable(False)
    self.clear()

    #Create the columns
    conv_col = self.create_column("Conversation Text", GnomeConfig.TEXT_POSITION)
    conv_col.set_resizable(True)
    conv_col.set_clickable(True)
    conv_col.set_expand(False)

    self.show()

  def __init__connections(self):
    self.connect("row-activated", self.goto_link, None)

  def goto_link(self, conv_tree, tree_iter, path, user_data):
    # Get the iter 
    tree_store, tree_iter = conv_tree.get_selection().get_selected()

    # Get the link itself
    model = conv_tree.get_model()    
    possible_link = model.get_value(tree_iter, GnomeConfig.LINK_POSITION)
    possible_text = model.get_value(tree_iter, GnomeConfig.TEXT_POSITION)
    
    if possible_link:
      path_to_link = model.get_path(possible_link)
      conv_tree.expand_to_path(path_to_link)
      conv_tree.set_cursor(path_to_link)

  def clear(self):
    self.conversations = gtk.TreeStore(object, object, str)
    self.set_model(self.conversations)

  def load_conversation_file(self, conv_file):
    self.clear()
    loc_tree = etree.parse(conv_file)

    self.loc_conv_file = conv_file
    self.loc_name = get_text(loc_tree, "Name")
    self.loc_next_entry_id = get_text(loc_tree, "NextEntryID")
    self.loc_entry_count = get_text(loc_tree, "EntryCount")

    loc_entries = {}
    loc_node_entries = loc_tree.find("Entries")
    for loc_entry in loc_node_entries:
      node_id = int(get_text(loc_entry, "ID"))
      default_text = get_text(loc_entry, "DefaultText")
      female_text = get_text(loc_entry, "FemaleText")

      new_node = poe_conv_node(node_id, default_text, female_text)
      # Only add if it has not already been added
      if not node_id in loc_entries:
        loc_entries[node_id] = new_node

    # Create the  that contains the structure
    #data_index = conv_file.index('\\data\\') + len('\\data\\')
    #control_name = conv_file[:data_index] + self.loc_name + ".conversation"
    control_name = os.path.dirname(os.path.realpath(__file__)) + '/00_cv_lord_harond.conversation'

    # The conversation tree itself
    conv_tree = etree.parse(control_name)
    
    # The directory that keeps tabs on where everything is
    self.iter_dict = {}
    
    # Now we begin to load in the conversation nodes
    
    # We need to make sure we do not add nodes whoose parents have not yet been added, so first we need to find all the conversation roots, and then all their children
    links_dict = {}
    for flowchart_node in conv_tree.find("Nodes"):
      parent_id = int(get_text(flowchart_node, "NodeID"))
      link_node_list = []
      for link_node in flowchart_node.find("Links"):
        link_node_from = int(get_text(link_node, "FromNodeID"))
        
        link_node_to   = get_text(link_node, "ToNodeID")
        if link_node_to: 
          link_node_to   = int(link_node_to)
        
        link_node_list.append((link_node_from, link_node_to,link_node))
             
      links_dict[parent_id] = link_node_list
      print(link_node_list)

    # We get the keys, and we make the list that is safe to work on
    self.safe_add(links_dict, 0, {}, loc_entries)
 
  """ We use a recursive function to safely add the conversation nodes  """
  def safe_add(self, links_dict, new_node_id, used_ids, loc_entries):   
    list_to_add = links_dict[new_node_id]
    keys_dict   = {}

    for item in list_to_add:
      link_node_from = item[0]
      link_node_to   = item[1]
 
      # We use the old uniqueness trick to only add the new ones
      if link_node_to and not link_node_to in used_ids:
        keys_dict[link_node_to] = 1
        
      iter_link = None
      if link_node_to in used_ids:
        linked_to = loc_entries[link_node_to]
        iter_link = self.iter_dict[linked_to]   

      entry = loc_entries[link_node_to]
  
      if new_node_id != 0:
        self.add_node(loc_entries[link_node_to], loc_entries[link_node_from], iter_link)
      else:
        self.add_node(loc_entries[link_node_to], None, iter_link)

      # We ensure we never use the same id again
      used_ids[link_node_to] = 1
    
    for new_id in keys_dict.keys():
      self.safe_add(links_dict, new_id, used_ids, loc_entries)
    

  def add_node(self, node, parent = None, iter_link=None):
    insert_node = node.get_list()

    if iter_link:
      insert_node[GnomeConfig.LINK_POSITION] = iter_link

    if parent == None:
      local_iter = self.conversations.append(None, insert_node)
      self.iter_dict[insert_node[0]] = local_iter
    else:
      parent_list = parent.get_list()
      parent_iter = self.iter_dict[parent_list[0]]
      local_iter = self.conversations.append(parent_iter, insert_node)
      self.iter_dict[insert_node[0]] = local_iter

  def create_column(self, label, place):
    title_col = gtk.TreeViewColumn()
    render_text = gtk.CellRendererText()
    render_text.set_property("ellipsize", pango.ELLIPSIZE_END)
    title_col.set_title(label)
    title_col.pack_start(render_text, expand=True)
    title_col.add_attribute(render_text, "markup", place)
    title_col.set_resizable(True)
    title_col.set_expand(True)    
    title_col.set_sort_column_id(place)
    self.append_column(title_col)
    self.columns.insert(place, title_col)
    return title_col

def get_text(tree, nodeName):
  return tree.find(nodeName).text
