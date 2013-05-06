from . import AdventureBase
from .event import Event
from .command import Command

from .utils import *

class Direction(AdventureBase):
  
  opposite = None
  directions = {}
  alldirections = {}
  
  def __init__(self, name, opposite=None, synonyms=tuple()):
    self.name = name
    
    if opposite:
      self.opposite = opposite
      opposite.opposite = self
      
    self.synonyms = synonyms
    
    self.directions[self] = self
    
    self.alldirections[self] = self
    for synonym in self.synonyms:
      self.alldirections[synonym] = self
          
  def __str__(self):
    return self.name
