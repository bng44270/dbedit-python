from re import sub as regex_sub
from os import path

class ConfigFile:
  def __init__(self,filename=""):  
    self.CONFIG = {}
    if len(filename) > 0:
      self.FILENAME = filename
      self.Read(filename)
    
  def Read(self,filename):
    if (path.exists(filename) or path.exists(self.FILENAME)) and (len(filename) > 0 or len(self.FILENAME) > 0):
      if filename and not self.FILENAME:
        self.FILENAME = filename
      with open(self.FILENAME,"r") as conffile:
        for line in conffile:
          if line[0] == '#' or len(line) == 0:
            continue
          else:
            self.CONFIG.update({regex_sub('^([^ \t]+).*$','\\1',str(line)).strip():regex_sub('^[^ \t]+[ \t]+(.*)$','\\1',str(line)).strip()})

  def IsNew(self):
    if self.CONFIG:
      return True
    else:
      return False

  def Write(self):
    with open(self.FILENAME,"w") as thisfile:
      for (k,v) in self.CONFIG.items():
        thisfile.write(k + "\t" + v + "\n")

  def Add(self,key,value):
    if len(key) > 0 and len(value) > 0:
      self.CONFIG.update({key:value})

  def Get(self,key):
    if self.CONFIG[key]:
      return self.CONFIG[key]

  def Remove(self,key):
    if self.CONFIG[key]:
      del self.CONFIG[key]