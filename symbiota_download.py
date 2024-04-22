
"""
Retrieve CSV/ZIP dataset from a Symbiota portal

This script downloads botanical specimen data from data portals which are based
on the Symbiota web application.

The search and download process generally starts at the collection search interface:
https://portal.torcherbaria.org/portal/collections/list.php
This is where the collection(s) is/are selected which provide the db value(s) which 
are hidden in the download form.
The search criteria form:
https://portal.torcherbaria.org/portal/collections/harvestparams.php
is where other parameters are input (taxonomy, geography, etc)
The results page:
https://portal.torcherbaria.org/portal/collections/list.php
displays a list of the matches. On this page is the download link which opens
the download form and the form handler which is used by this script.

"""
import requests
import urllib.parse

# Query parameters
# db=370 specifies the BRIT dataset, this can be changed to specify other datasets
rsa_bryo = '68'
rsa_vasc = '17'
rsa_wood = '105'

db_list = [rsa_bryo, rsa_vasc, rsa_wood]
#db_list = [370]
db = ','.join([str(db_id) for db_id in db_list])
#state = 'Texas'
state = ''
#county = 'Scurry'
county = ''
hasimages = '0'
includecult = '1' # include cultivated
collector = 'Carlquist'
#search_params = {'db': db, 'state': state, 'county': county, 'hasimages': hasimages}
search_params = {'db': db, 'hasimages': hasimages, 'includecult': includecult, 'collector': collector}

#searchvar = urllib.parse.urlencode(search_params)
#searchvar = 'db=68,17,105&collector=Carlquist&includecult=1'
#print(db)
#print(searchvar)
#searchvar = 'db=370&state=Texas&county=Tarrant&hasimages=1'

# Download format parameters
#url = 'https://portal.torcherbaria.org/portal/collections/download/downloadhandler.php'
url = 'https://www.cch2.org/portal/collections/download/downloadhandler.php'
schema = 'dwc' # Darwin Core
file_format = 'csv' #form field name is 'format'
cset = 'utf-8'
#publicsearch = '1'
publicsearch = '1'
taxonFilterCode = '0'
sourcepage = 'specimen'
images = '0' # include images - 1, only includes image records
zip_file = '0' # form field name is zip, default to not zip file
if images == '1': # results must be zipped to get both specimen and image records
  zip_file = '1' # form field name is zip

# download params
download_params={'schema': schema, 'format': file_format, 
    'cset': cset, 'publicsearch': publicsearch, 
    'taxonFilterCode': taxonFilterCode, 
    'images': images, 'zip':zip_file,
    'sourcepage': sourcepage}

# combine parameters
data = search_params | download_params

r = requests.post(url, 
    data=data,
    stream=True)

print(r.url)

# Save data
if zip_file == '0':
  #Save CSV
  filename = 'symbiota_data.csv'
  with open(filename, 'w') as data_file:
    data_file.write(r.text)
  print(f'File {filename} saved.')

if zip_file =='1':
  # Save ZIP
  filename = 'symbiota_data.zip'
  with open(filename, 'wb') as zip_file:
    for chunk in r.iter_content(chunk_size=128):
      zip_file.write(chunk)
  print(f'File {filename} saved.')


  