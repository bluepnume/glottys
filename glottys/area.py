from itertools import chain

from . import AdventureBase, Collection, Mapping
from .event import Event

from .utils import *

class Area(AdventureBase):
  
  entered = False
  
  first_enter_text = None
  enter_text = 'You enter {self}'
  enter_fail_text = 'You can not currently enter {self}'
  
  look_area_text = 'You are in {self}'
  look_inventory_text = 'You can see the following items: {items}'
  look_character_text = 'You can see the following people: {self.characters}'
  look_direction_text = 'To the {direction} is {location}'
  
  def __init__(self, name):
    
    AdventureBase.__init__(self, name)
    
    self.name = name
    self.directions = Mapping()
    
    # Items
    self.inventory = Mapping()
    self.staticitems = Mapping()
    
    self.characters = Mapping()
    
    # Events
    self.onLook = Event()
    self.onFirstEnter = Event()
    self.onEnter = Event()
    self.onExit = Event()
    
  def add_path(self, direction, area):
    self.directions[direction] = area
    area.directions[direction.opposite] = self
    
  def look(self, item=None):
    if self.onLook.trigger(item):
      if item:
        item.look()
      else:
        self.echo(self.look_area_text, mapping=locals())
        items = Collection(i for i in chain(self.inventory.keys(), self.staticitems.keys()) if not i.hidden)
        if items:
          self.echo(self.look_inventory_text, mapping=locals())
        if self.characters:
          self.echo(self.look_character_text, mapping=locals())
          
        first = True
        for n, (direction, location) in enumerate(self.directions.iteritems()):
          if not location.hidden:
            self.echo(location.look_direction_text, mapping=locals(), newline=first)
            first = False
    
  def enter(self, character):
    if self.enabled:
      if self.onEnter.trigger():
        if not self.entered:
          if self.onFirstEnter.trigger():
            self.entered = True
            self.echo(self.first_enter_text or self.enter_text, mapping=locals())
        else:
          self.echo(self.enter_text, mapping=locals())
        character.location = self
    else:
      self.echo(self.enter_fail_text, mapping=locals())
