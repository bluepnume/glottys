from functools import wraps
import sys, time, difflib
  
def closest(name, options):
  matches = difflib.get_close_matches(name, options)
  if matches:
    return matches[0]
  
def optionlist(method):
  
  @wraps(method)
  def createoptionlist():
    options = {} 
    for option in method():
      options[option] = option
      for synonym in option.synonyms:
        options[synonym] = option
    return options
    
  return createoptionlist


def cacheprop(method):
  @wraps(method)
  def cachemethod(self):
    while True:
      try:
        return self.cache[method]
      except AttributeError:
        self.cache = {}
      except KeyError:
        self.cache[method] = method(self)
  return property(cachemethod)

def cachetuple(method):
  @wraps(method)
  def cachemethod(self):
    while True:
      try:
        return self.cache[method]
      except AttributeError:
        self.cache = {}
      except KeyError:
        self.cache[method] = tuple(method(self))
  return property(cachemethod)
