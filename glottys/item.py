from . import AdventureBase, Collection
from .event import Event

from .utils import *

class AbstractItem(AdventureBase):
  
  description = 'This is a {self}'
  
  use_text = 'You can not use {self}'
  
  pickup_text = 'You pick up {self}'
  pickup_fail_text = 'You can not pick up {self}'
  
  open_text = 'You open {self}'
  locked_text = '{self} is locked'
  empty_text = '{self} is empty '
  not_container_text = '{self} is not a container'
  
  contains_text = '{self} contains {items}'
  
  discard_text = 'You discard {self}'
  discard_fail_text = 'You might need the {self}, probably best to keep it for now'
  
  lookedat = False

  def __init__(self, name, owner=None, synonyms=(), container=False):
    
    AdventureBase.__init__(self, name)
    
    self.inventory = {}
    self.staticitems = {}
    
    self.name = name
      
    self.synonyms = synonyms
    self.container = container
      
    # Events
    
    self.onPickup  = Event()
    self.onLook    = Event()
    self.onFirstLook    = Event()
    self.onUse     = Event()
    self.onOpen    = Event()
    self.onDiscard = Event()
      
  def look(self):
    
    if self.onLook.trigger():
      if not self.lookedat:
        self.lookedat = True
        self.onFirstLook.trigger()
      
      self.echo(self.description, mapping=locals())
      
  def open(self, inventory, staticitems):
    if self.onOpen.trigger():
      if self.container:
        if self.locked:
          self.echo(self.locked_text, mapping=locals())
        else:
          self.echo(self.open_text, mapping=locals())
          if self.inventory or self.staticitems:
            items = Collection(self.inventory.keys() + self.staticitems.keys())
            self.echo(self.contains_text, mapping=locals())
            
            for subitem in self.inventory:
              inventory[subitem] = subitem
              
            for subitem in self.staticitems:
              staticitems[subitem] = subitem
              
            self.inventory.clear()
            self.staticitems.clear()
          else:
            self.echo(self.empty_text, mapping=locals())
      else:
        self.echo(self.not_container_text, mapping=locals())
        
  def pickup(self, location, inventory):
    if self.hidden:
      self.echo(self.pickup_fail_text, mapping=locals())
    elif self.onPickup.trigger():
      self.echo(self.pickup_text, mapping=locals())
      inventory[self] = location.inventory.pop(self)
      
  def discard(self):
    
    if self.discardable:
      if self.onDiscard.trigger():
        self.echo(self.discard_text, mapping=locals())
    else:
     self.echo(self.discard_fail_text, mapping=locals())
      
  def use(self):
    if self.onUse.trigger():
      self.echo(self.use_text, mapping=locals())
  

class InventoryItem(AbstractItem):
  
  discardable = False
  
  def __init__(self, name, owner=None, synonyms=(), container=False):
    
    AbstractItem.__init__(self, name, owner, synonyms, container)
    
    if owner:
      owner.inventory[self] = self

      
class StaticItem(AbstractItem):
  
  def __init__(self, name, owner, synonyms=(), container=False):
    
    AbstractItem.__init__(self, name, owner, synonyms, container)
    owner.staticitems[self] = self
