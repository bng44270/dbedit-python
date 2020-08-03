class PageBuilder:
  def __init__(self,title="New Page"):
    self.TITLE = title
    self.ELEMENTS = []
    self.C_ELEMENTS = []
  
  def Header(self,text,tagline=""):
    har = sorted([int(a['id'].replace('header','')) for a in self.ELEMENTS if a['id'].startswith('header')],reverse=True)
    nextid = 0 if len(har) == 0 else har[0]+1
    
    self.ELEMENTS.append({'id':'header{}'.format(str(nextid)),'html':'<div id="header{}"><h1>{}</h1>{}<h3>{}</h3></div>'.format(str(nextid),text,tagline)})
    
    return 'header{}'.format(str(nextid))
  
  def Br(self):
    self.ELEMENTS.append({'html':'<br/>'})
  
  def Table(self,cols,rows, cells = []):
    tar = sorted([int(a['id'].replace('table','')) for a in self.ELEMENTS if a['id'].startswith('table')],reverse=True)
    nextid = 0 if len(tar) == 0 else tar[0]+1
    
    table = ''
    
    for r in range(0,rows):
      table += '<tr id="r{}">'.format(str(r+1))
      for c in range(0,cols):
        table += '<td id="r{}c{}">{}</td>'.format(str(r+1),str(c+1),cells[r][c] if cells else '')
      table += '</tr>'
    
    self.ELEMENTS.append({'id':'table{}'.format(str(nextid)),'html':'<table id="table{}">{}</table>'.format(str(nextid),table)})
    
    return 'table{}'.format(str(nextid))
    
  
  def Link(self,label,href):
    lar = sorted([int(a['id'].replace('link','')) for a in self.ELEMENTS if a['id'].startswith('link')],reverse=True)
    nextid = 0 if len(lar) == 0 else lar[0]+1
    
    self.ELEMENTS.append({'id':'link{}'.format(str(nextid)),'html':'<a href="{}" id="{}">{}</a>'.format(href,str(nextid),label)})
    
    return 'link{}'.format(str(nextid))
  
  def Form(self,method,url,elements=[]):
    far = sorted([int(a['id'].replace('form','')) for a in self.ELEMENTS if a['id'].startswith('form')],reverse=True)
    nextid = 0 if len(far) == 0 else far[0]+1
    
    self.ELEMENTS.append({'id':'form{}'.format(str(nextid)),'html':'<form method="{}" action="{}" id="form{}">{}<input type="submit"></form>'.format(method,url,str(nextid),'<br/>\n'.join(elements))})
    
    return 'form{}'.format(str(nextid))
  
  def LinkHtml(self,label,href):
    return '<a href="{}">{}</a>'.format(href,label)
  
  def ScriptButtonHtml(self,label,click):
    return '<input type="button" value="{}" onClick="{}" />'.format(label,click.replace('\n',''))
  
  def InputHtml(self,label,name):
    return '<label for="{}">{}</label><input type="text" name="{}" id="frm_{}" />'.format(name,label,name,name)
    
  def SelectHtml(self,label,name,choices=[]):
    return '<label for="{}">{}</label><select name="{}" id="frm_{}"/>{}</select>'.format(name,label,name,name,'\n'.join(['<option value="{}">{}</option>'.format(a['value'],a['label']) for a in choices])) if self.__ChoiceValidation(choices) else '<div><span>{}</span><select name="{}" id="frm_{}"/></select></div>'.format(label,name,name)
  
  def RadioHtml(self,label,name,options=[]):
    return '<span>{}</span>{}'.format(label,'\n'.join(['<input type="radio" name="{}" id="frm_{}" value="{}"/><label for="{}">{}</label><br/>'.format(name,name,a['value'],a['value'],a['label']) for a in choices])) if self.__ChoiceValidation(choices) else '<span>{}</span>'.format(label)
  
  def TextAreaHtml(self,label,name,cols,rows):
    return '<label for="{}">{}</label><br/><textarea name="{}" cols="{}" rows="{}"></textarea>'.format(name,label,name,str(cols),str(rows))
  
  def CheckboxHtml(self,label,name,value):
    return '<input type="checkbox" name="{}" id="frm_{}" value="{}" /><label for="{}">{}</label>'.format(name,name,value,name,label)
  
  def RawHtml(self,content):
    return content.replace('\n','')
  
  def __ChoiceValidation(self,choices):
    return False if len([a for a in [('value' in a.keys() and 'label' in a.keys()) for a in choices] if not a]) > 0 else True
  
  def Render(self):
    return '<html><head><title>{}</title></head><body>{}</body></html>'.format(self.TITLE,'\n'.join([a['html'] for a in self.ELEMENTS]))