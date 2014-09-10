#!/usr/bin/python 

class poe_conv_node(object):

  def __init__(self, node_id, default_text, female_text):
    self.node_id = node_id
    self.default_text = default_text
    self.female_text = female_text

  def __str__(self):
    return self.default_text

  def get_list(self):
    """This function returns the conv node information"""
    if len(self.default_text) > 0:
      return [self, None, self.default_text]
    else:
      return [self, None, self.female_text]
