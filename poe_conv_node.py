#!/usr/bin/python 

class poe_conv_node(object):

  def __init__(self, conversation_node, flowchart_node):
    self.node_id      = int(get_text(conversation_node, "ID"))
    self.default_text = get_text(conversation_node, "DefaultText")
    self.female_text  = get_text(conversation_node, "FemaleText")


    self.conv_type = get_attribute(flowchart_node, "xsi:type")

    if self.conv_type == "TalkNode":
      self.not_skippable    = self.get_bool(flowchart_node, "NotSkippable")
      self.is_question_node = self.get_bool(flowchart_node, "IsQuestionNode")
      self.is_temp_text     = self.get_bool(flowchart_node, "IsTempText")
    else:
      self.not_skippable    = None
      self.is_question_node = None
      self.is_temp_text     = None
      

  def get_bool(self, node, entry):
    return self.string_to_bool(get_text(node, entry))

  def string_to_bool(self, value_to_convert):
    if value_to_convert == "false":
      return False
    elif value_to_convert == "true":
      return True
    else:
      return None

  def __str__(self):
    return self.default_text

  def get_list(self):
    """This function returns the conv node information"""
    if len(self.default_text) > 0:
      return [self, None, self.default_text]
    else:
      return [self, None, self.female_text]

def get_attribute(tree, attr):
  attr = attr.replace('xsi:', '{http://www.w3.org/2001/XMLSchema-instance}')
  return tree.attrib[attr]

def get_text(tree, nodeName):
  return tree.find(nodeName).text

def has_entry(tree, nodeName):
  return tree.find(nodeName) != None
