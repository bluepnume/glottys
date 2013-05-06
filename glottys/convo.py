from . import AdventureBase
from .event import Event

from .utils import *

class ConversationOver(Exception):
  pass

class Thread(AdventureBase):
  
  callback = None
  
  def __init__(self, query, response, parent=None, persistent=False, character=None, uplevel=False, end=False, auto=False):
    AdventureBase.__init__(self, query)
    
    self.name = self.query = query
    self.response = response
    
    self.threads = {}
    self.parent = parent
    
    if self.parent:
      self.parent.threads[self] = self
      self.character = self.parent.character
    else:
      self.character = character
      self.character.conversation = self
      
    self.persistent = persistent
    self.uplevel = uplevel
    self.end = end
    self.auto = auto
    
    self.onInitiate = Event()
    self.onDialogue = Event()
    self.onEnd      = Event()
    
  def initiate(self):
    if self.onInitiate.trigger():
      self.echo('You: %s' % self.query)
      self.echo('%s: %s' % (self.character, self.response))
      
      if self.onDialogue.trigger():
        try:
          if self.end:
            return self.endconversation()
          
          if self.uplevel:
            return
            
          self.presentoptions()
          
        except ConversationOver:
          self.onEnd.trigger()
          raise
    
  def presentoptions(self):
    
    threads = [thread for thread in self.threads if thread.enabled]
    
    if not threads:
      return

    if self.auto and len(threads) == 1:
      return self.select(threads[0])
      
    self.echogroup('%s: %s' % (i, child.query) for i, child in enumerate(threads, 1))
      
    result = int(self.input(pattern='^\d+$', cond=lambda r: r.isdigit() and int(r) <= len(threads))) - 1
    self.select(threads[result])
    
      
  def select(self, thread):
    
    thread.initiate()
    
    if not thread.persistent:
      self.threads.pop(thread)
      
    self.presentoptions()
      
  def endconversation(self):
    raise ConversationOver
