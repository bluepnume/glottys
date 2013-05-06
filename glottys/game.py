try:
  import readline
except ImportError:
  pass

from . import AdventureBase
from .command import Command
from .event import Event

from .utils import *

class EndGame(Exception):
  pass

class Game(AdventureBase):
  
  intro_text = 'Welcome to... {self}'
  end_text = 'End of game {self}'
  
  command_not_found = 'Command not found'
  
  maincharacter = None
  
  def __init__(self, name):
    self.name = name
    
    self.doExit = Command('exit', self.exit)
    
    try:
      readline.parse_and_bind("tab: complete")
      readline.set_completer(self.complete)
    except NameError:
      pass
      
    # Events
    
    self.onRun = Event()
    self.onExit = Event()
    self.onEndGame = Event()

  def run(self):
    
    if self.onRun.trigger():
    
      self.cls()
      
      try:
      
        self.echo(self.intro_text, mapping=locals())
        self.maincharacter.look()
      
        while True:
          
          commandstring = raw_input('\n> ').lower().strip()
          
          if not commandstring:
            continue
          
          Command.run_command(commandstring)
          
      except KeyboardInterrupt:
        self.exit()
        
      except EndGame:
        self.exit()
      
        
  def exit(self):
    if self.onExit.trigger():
      print
      sys.exit()
    
  def help(self):
    self.echo('Commands: %s' % ', '.join(Command.commands))
    
  def complete(self, text, state):
    for command in Command.commands:
      if command.startswith(text):
        return command
        
  def endgame(self):
    if self.onEndGame.trigger():
      self.echo(self.end_text, mapping=locals())
      raise EndGame
