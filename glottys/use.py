from . import AdventureBase, Collection
from .event import Event

from .utils import *

class Use(AdventureBase):
  
  combinations = {}
  
  use_text = 'Used {items}'
  combine_text = 'Recieved {result}'
  
  callback = None
  
  def __init__(self, *args, **kwargs):
    self.items = tuple(sorted(set(args)))
    
    AdventureBase.__init__(self, '<Items %s>' % ', '.join(self.items))
    
    self.result = kwargs.get('result', None)
    self.combinations[self.items] = self
    
    self.onUse = Event()

  def __call__(self, callback):
    if self.items:
      self.callback = callback
    return callback
    
  def use(self):
    
    if self.onUse.trigger():
      items = Collection(self.items)
      
      self.echo(self.use_text, mapping=locals())
      
      if self.result:
        result = self.result
        self.echo(self.combine_text, mapping=locals())

      self.call()
      return self.result
    
  def call(self):
    if callable(self.callback):
      self.callback()
