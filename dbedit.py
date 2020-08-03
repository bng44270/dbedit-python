from flask import Flask, send_file, make_response, redirect, request
from ezmysql import TableDef
from configfile import ConfigFile

CONFIG = ConfigFile('./itapps.cfg')

DB_server = CONFIG.Get('DBServer')
DB_user = CONFIG.Get('DBUser')
DB_password = CONFIG.Get('DBPassword')
DB_tables = Config.Get('DBTables').split(',')

# Configure table objects
TABLES = [{"name":a,"def" : TableDef(DB_server,DB_user,DB_password,a)} for a in DB_tables]

# Pull schema
for thisTable in TABLES:
  thisTable['schema'] = thisTable['def'].Schema()

ROOT = '/var/www/python/itapps'

app = Flask(__name__)

@app.route('/')
def getroot():
  return render_template('{}/templates/show_tables.html'.format(ROOT),tables=[a['name'] for a in TABLES])

@app.routes('/<table>/list')
def TableList(table):
  tableAr = [a for a in TABLES where a['name'] == table]
  if len(tableAr) == 1:
    return render_template('{}/templates/list_table.html'.format(ROOT),config = {'data': tableAr[0].Select(),'schema':tableAr[0].Schema(), 'tablename':table)

@app.route('/<table>/view/<id>')
def ViewRecord(table,id):
  tableAr = [a for a in TABLES where a['name'] == table]
  if len(tableAr) == 1:
    result = tableAr[0].Select([],[('id',id)])
    if len(result) == 1:
      return render_template('{}/templates/view_record.html'.format(ROOT),config = {'data':result[0],'schema':tableAr[0].Schema(),'tablename':table,'id':id})
    else:
      return make_response('Record id {} not found'.format(id),200)
  else:
    return make_response('Table {} not found'.format(table),200)
  
@app.route('/<table>/edit')
def EditRecord(table):
  
@app.route('/<table>/new')
def NewRecord(table):

@app.route('/<table>/insert',methods=['POST'])
def InsertRecord(table):

@app.route('/<table>/update',methods=['POST'])
def UpdateRecord(table):
  

@app.route('/scripts/<script>')
def getscript(script):
  returnValue = None
  if file_path.exists('%s/scripts/%s' % (ROOT,script)):
    returnValue = send_file('%s/scripts/%s' % (ROOT,script))
  else:
    returnValue = make_response('File %s not found' % script,200)

  return returnValue
