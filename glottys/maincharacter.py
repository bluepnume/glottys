from itertools import chain

from . import AdventureBase, Collection, Mapping
from .event import Event
from .command import Command
from .direction import Direction
from .use import Use

from .utils import *

class MainCharacter(AdventureBase):
  
  move_text = 'You move {direction}'
  inventory_text = "I'm carrying {items}"
  
  def __init__(self, name, game, startlocation):
    self.name = name
    self.game = game
    self.game.maincharacter = self
    self.location = startlocation
    self.inventory = Mapping()
    
    # Events
    self.onMove = Event()
    self.onPickup = Event()
    self.onLook = Event()
    self.onOpen = Event()
    self.onCheckInv = Event()
    self.onUse = Event()
    self.onDiscard = Event()
    
    # Commands
    self.doMove     = Command('move',
                              self.move,
                              synonyms=('go', 'travel', 'walk'),
                              options=lambda: self.location.directions,
                              alloptions=Direction.alldirections,
                              failure="I can't go {arg}"
                      )
                      
    self.doLook     = Command('look',
                              self.look,
                              synonyms=('see', 'observe'),
                              options=lambda: chain(self.inventory, self.location.inventory, self.location.staticitems, self.location.characters)
                      )
                      
    self.doGet      = Command('get',
                              self.pickup,
                              synonyms=('pickup', 'take'),
                              options=lambda: self.location.inventory,
                              failure="I can't pick up {arg}"
                      )
                      
    self.doOpen     = Command('open',
                              self.open,
                              options=lambda: chain(self.inventory, self.location.inventory, self.location.staticitems),
                              failure="I can't open {arg}"
                      )
                      
    self.doCheckInv = Command('inventory',
                              self.checkinv
                      )
                      
    self.doUse      = Command('use',
                              self.use,
                              options=lambda: chain(self.inventory, self.location.staticitems),
                              failure="I can't find {arg}"
                      )
                      
    self.doDrop     = Command('drop',
                              self.discard,
                              synonyms=('discard', 'leave'),
                              options=lambda: self.inventory,
                              failure="I don't have that item"
                      )
                      
    self.doTalk     = Command('talk',
                              self.talk,
                              options=lambda: self.location.characters,
                              failure="I can't find them"
                      )
                      
    self.doHelp     = Command('help',
                              self.game.help,
                      )
                             
    for direction in Direction.directions:
      Command.register(direction.name.lower(), lambda direction=direction: Command.run_command('move %s' % direction.name.lower()), synonyms=direction.synonyms)
    
  def move(self, direction):
    if self.onMove.trigger(direction):
      if self.location.onExit.trigger():
        self.echo(self.move_text, mapping=locals())
        location = self.location.directions[direction]
        location.enter(self)
      
  def pickup(self, item):
    if self.onPickup.trigger(item):
      item.pickup(self.location, self.inventory)
        
  def open(self, item):
    if self.onOpen.trigger(item):
      item.open(self.inventory if item in self.inventory else self.location.inventory, self.location.staticitems)
      
  def look(self, item=None):
    if self.onLook.trigger():
      self.location.look(item=item)
      
  def talk(self, character):
    character.talk()
    
  def checkinv(self):
    if self.onCheckInv.trigger():
      items = self.inventory or 'nothing'
      self.echo(self.inventory_text, mapping=locals())
        
  def discard(self, item):
    if self.onDiscard.trigger():
      item.discard()
      self.drop(item)
      
  def has(self, item):
    return item in self.inventory
    
  def drop(self, item):
    if item in self.inventory:
      self.inventory.pop(item)
      
  def give(self, item):
    self.inventory[item] = item
      
  def use(self, *items):
    
    items = tuple(sorted(set(items)))
    
    '''for item in items:
      if item in self.location.inventory:
        self.pickup(item)'''
  
    if items in Use.combinations:
      
      result = Use.combinations[items].use()
      if result:
        for item in items:
          if item in self.inventory:
            self.inventory.pop(item)
            
        self.inventory[result] = result
      
    elif len(items) == 1:
      items[0].use()
      
    else:
      self.echo("I can't use these things together")
