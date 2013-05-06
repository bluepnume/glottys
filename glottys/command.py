from inspect import getargspec

from . import AdventureBase

from .utils import *

class Command(AdventureBase):
  
  commands = {}
  callback = None
  
  conjunctives = ('at', 'with', 'and', 'on', 'to', 'in', 'the', 'a')
  
  def __init__(self, name, callback=None, synonyms=(), options=None, alloptions=(), failure="I can't do this"):
    AdventureBase.__init__(self, name)
    self.callback = callback
    self.commands[self] = self
    self.synonyms = synonyms
    self.options = options
    self.alloptions = alloptions
    self.failure = failure
  
  @classmethod  
  def run_command(cls, commandstring):
    args = commandstring.split()
    command = args.pop(0)
    options = cls.createoptionlist(cls.commands)
    command = closest(command, options)
      
    if command:
      options[command].call(*args)
    else:
      print '\nCommand not found'
    
  @classmethod
  def createoptionlist(self, options):
    optionlist = {} 
    for option in options:
      optionlist[option] = option
      for synonym in option.synonyms:
        optionlist[synonym] = option
    return optionlist

  
    
  def call(self, *args):
    
    args = [arg for arg in args if arg not in self.conjunctives]
    
    if callable(self.options):
      options = self.createoptionlist(self.options())
      
      args = list(args)
      for i, arg in enumerate(args):
        if arg in options:
          args[i] = options[arg]
        else:
          if arg in self.alloptions:
            return self.echo(self.failure, mapping=locals())
          else:
            result = closest(arg, options)
            if result:
              args[i] = options[result]
            else:
              return self.echo(self.failure, mapping=locals())
          
    if len(args) < self.minargs:
      return self.echo('More information needed')
          
    self.callback(*args[:self.maxargs])
      
  def __call__(self, callback):
    self.callback = callback
    return callback
    
  @cacheprop
  def maxargs(self):
    argspec = getargspec(self.callback)
    if argspec.varargs or argspec.keywords:
      return None
    if 'self' in argspec.args:
      argspec.args.remove('self')
    return len(argspec.args)
    
  @cacheprop
  def minargs(self):
    argspec = getargspec(self.callback)
    if 'self' in argspec.args:
      argspec.args.remove('self')
    return len(argspec.args or '') - len(argspec.defaults or '')
