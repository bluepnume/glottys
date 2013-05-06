class Event(object):
  
  def __init__(self):
    self.callbacks = []
    self.aftercallbacks = []
    
  def __call__(self, callback):
    self.callbacks.append(callback)
    return callback
    
  def after(self, callback):
    self.aftercallbacks.append(callback)
    return callback
    
  def trigger(self, *args, **kwargs):
    for callback in self.callbacks:
      if callback(*args, **kwargs) is False:
        return False
    return True
    
  def done(self):
    for callback in self.aftercallbacks:
      callback()
