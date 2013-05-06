from . import AdventureBase
from .event import Event
from .convo import ConversationOver

class Character(AdventureBase):
  
  conversation = None
  description = "It's {self}"
  talk_fail = "I don't think I want to talk to {self}"
  
  def __init__(self, name, location):
    
    AdventureBase.__init__(self, name)
    
    self.location = location
    self.location.characters[self] = self
    
    self.onLook = Event()
    self.onTalk = Event()
    
  def talk(self):
    if self.onTalk.trigger():
      if self.conversation:
        try:
          self.conversation.initiate()
        except ConversationOver:
          pass
      else:
        self.echo(self.talk_fail, mapping=locals())
      
  def look(self):
    if self.onLook.trigger():
      self.echo(self.description, mapping=locals())
  
