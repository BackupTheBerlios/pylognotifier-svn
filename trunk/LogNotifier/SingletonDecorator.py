# this code should be public domain, I found it on the web

class SingletonDecorator:
  def __init__(self,klass):
    self.klass = klass
    self.instance = None
  def __call__(self,*args,**kwds):
    if self.instance == None:
      self.instance = self.klass(*args,**kwds)
    return self.instance