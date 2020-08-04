from flask import Flask, send_file, make_response, redirect, request
from ezmysql import TableDef
from configfile import ConfigFile
from requests import post as http_post

CONFIG = ConfigFile('./itapps.cfg')

DB_server = CONFIG.Get('DBServer')
DB_user = CONFIG.Get('DBUser')
DB_password = CONFIG.Get('DBPassword')
TABLES = Config.Get('DBTables').split(',')

# Configure table objects
TABLES = [{"name" : a,"def" : TableDef(DB_server,DB_user,DB_password,a)} for a in TABLES]

# Pull schema
for thisTable in DB_tables:
  thisTable['schema'] = thisTable['def'].Schema()

ROOT = '/var/www/python/dbedit'

app = Flask(__name__)

@app.route('/')
def getroot():
  return render_template('{}/templates/show_tables.html'.format(ROOT),tables=[a['name'] for a in DB_tables])

@app.routes('/<table>/list')
def TableList(table):
  tableAr = [a for a in DB_tables if a['name'] == table]
  if len(tableAr) == 1:
    return render_template('{}/templates/list_table.html'.format(ROOT),config = {'data': tableAr[0].Select(),'schema':tableAr[0].Schema(), 'tablename':table)

@app.route('/<table>/view/<id>')
def ViewRecord(table,id):
  tableAr = [a for a in DB_tables if a['name'] == table]
  if len(tableAr) == 1:
    result = tableAr[0].Select([],[('id',id)])
    if len(result) == 1:
      return render_template('{}/templates/view_record.html'.format(ROOT),config = {'data':result[0],'schema':tableAr[0].Schema(),'tablename':table,'id':id})
    else:
      return make_response('Record id {} not found'.format(id),200)
  else:
    return make_response('Table {} not found'.format(table),200)
  
@app.route('/<table>/edit/<id>')
def EditRecord(table):
  tableAr = [a for a in DB_tables if a['name'] == table]
  if len(tableAr) == 1:
    result = tableAr[0].Select([],[('id',id)])
    if len(result) == 1:
      return render_template('{}/templates/edit_record.html'.format(ROOT),config = {'data':result[0],'schema':tableAr[0].Schema(),'tablename':table,'id':id})
    else:
      return make_response('Record id {} not found'.format(id),200)
  else:
    return make_response('Table {} not found'.format(table),200)
  
@app.route('/<table>/new')
def NewRecord(table):
  tableAr = [a for a in DB_tables if a['name'] == table]
  if len(tableAr) == 1:
    CONFIG = {'tablename':table}
    Q_params = [{a.split('=')[0]:a.split('=')[1]} for a in request.query_string.split('&')]
    if len(Q_params) > 0:
      CONFIG['tempdata'] = Q_params
    
    return render_template('{}/templates/new_record.html'.format(ROOT),config = CONFIG)

@app.route('/<table>/insert',methods=['POST'])
def InsertRecord(table):
  tableAr = [a for a in DB_tables if a['name'] == D_POST['table']]
  if len(tableAr) == 1:
    T_schema = tableAr[0].Schema()
    D_POST = request.get_json()
    
    fields = []
    values = []
    
    for thisKey in D_POST['data'].keys():
      if thisKey in [a['name'] for a in T_schema]:
        fields.append(thisKey)
        thisValue = D_POST['data'][thisKey]
        values.append(int(thisValue) if thisKey in [a['name'] for a in T_schema if a['type'] == 'int'] else thisValue)
    
    if tableAr[0].Insert(fields,values):
      return redirect('/{}/view/{}'.format(table,D_POST['data']['id']))
    else:
      return redirect('/{}/new?{}'.format(table,'&'.join(['{}={}'.format(a[0],a[1]) for a in D_POST['data'].items()])))

@app.route('/<table>/update',methods=['POST'])
def UpdateRecord(table):
  tableAr = [a for a in DB_tables if a['name'] == D_POST['table']]
  if len(tableAr) == 1:
    D_POST = request.get_json()
    if 'id' in D_POST['data'].keys():
      

@app.route('/scripts/<script>')
def getscript(script):
  returnValue = None
  if file_path.exists('%s/scripts/%s' % (ROOT,script)):
    returnValue = send_file('%s/scripts/%s' % (ROOT,script))
  else:
    returnValue = make_response('File %s not found' % script,200)

  return returnValue
