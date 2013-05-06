import os, re, time


class Mapping(dict):
  
  def __str__(self):
    return ', '.join(self)
    
    
class Collection(list):
  
  def __str__(self):
    return ', '.join(self)


class AdventureBase(str):
  
  enabled = True
  hidden = False
  locked = False
  
  synonyms = ()
  
  def __new__(self, text, *args, **kwargs):
    return str.__new__(self, text)
      
  def __init__(self, name, *args, **kwargs):
    
    self.name = name
    
    # Events
    self.onEnable  = Event()
    self.onDisable = Event()
    self.onShow    = Event()
    self.onHide    = Event()
    self.onLock    = Event()
    self.onUnlock  = Event()
    
  def echo(self, text, mapping=None, delay=0.00, newline=True):
    if text:
      if mapping is None:
        mapping = self.__dict__
      text = text.format(**mapping)
      if delay:
        for char in '%s%s\n' % ('\n' if newline else '', text):
          sys.stdout.write(char)
          sys.stdout.flush()
          time.sleep(delay)
      else:
        sys.stdout.write('%s%s\n' % ('\n' if newline else '', text))
        
  def echogroup(self, items, mapping=None, delay=0):
    for i, item in enumerate(items):
      self.echo(item, mapping=mapping, delay=delay, newline=not i)
    
  def input(self, text=None, pattern=None, cond=None):
    if text:
      self.echo(text)
    while True:
      result = raw_input('\n: ').strip()
      if (pattern and re.match(pattern, result)) or result:
        if cond and not cond(result):
          continue
        return result
        
  def pause(self, period):
    time.sleep(period)
    
  def cls(self, period=1.5):
    return
    self.pause(period)
    os.system('clear')
    
  @classmethod
  def register(cls, *args, **kwargs):
    return cls(*args, **kwargs)
  
  def enable(self):
    if self.onEnable.trigger():
      self.enabled = True
    
  def disable(self):
    if self.onDisable.trigger():
      self.enabled = False
      
  def show(self):
    if self.onShow.trigger():
      self.hidden = False
    
  def hide(self):
    if self.onHide.trigger():
      self.hidden = True
      
  def lock(self):
    if self.onLock.trigger():
      self.locked = True
    
  def unlock(self):
    if self.onUnlock.trigger():
      self.locked = False
      
  def __hash__(self):
    return hash(str(self).lower())
    
  def __str__(self):
    return self.name
    
  def __repr__(self):
    return str(self).lower()
    
  def __eq__(self, other):
    return str(self).lower() == str(other).lower()
    
  def __lt__(self, other):
    return str(self).lower() < str(other).lower()
    
  def __len__(self):
    return len(str(self).lower())
    
  def __iter__(self):
    return iter(str(self).lower())
    
  def __getitem__(self, index):
    return str(self).lower()[index]
    
    
from .game import *
from .command import *
from .event import *
from .area import *
from .direction import *
from .maincharacter import *
from .character import *
from .item import *
from .use import *
from .convo import *


North = Direction('North', synonyms=('n', 'forward',))
South = Direction('South', opposite=North, synonyms=('s', 'back',))
East  = Direction('East', synonyms=('e', 'left',))
West  = Direction('West', opposite=East, synonyms=('w', 'back',))
Up    = Direction('Up')
Down  = Direction('Down', opposite=Up)
