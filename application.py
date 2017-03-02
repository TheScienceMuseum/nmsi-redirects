from flask import Flask 
import csv

# example of old url
# http://collectionsonline.nmsi.ac.uk/detail.php?type=related&kv=66468&t=objects

app = Flask(__name__)

courl = 'https://collection.sciencemuseum.org.uk'
lookup = {}

# load mapping table into a dictonary keyed on kv value
app.logger.info('loading mappings');
f = open('lookup.csv', "r", encoding='latin-1')
try:
  reader = csv.reader(f)
  for row in reader:
    lookup[row[0]] = row[1]
finally:
    f.close()

@app.route('/') 
def index():
  app.logger.info('redirecting to /');
  return redirect(courl);

@app.route('/detail.php') 
def match():
  try:
    return redirect(courl + '/oid/' + lookup[request.args.get('kv')] + "?redirect=true")
  except KeyError:
    return redirect(courl)

if __name__ == '__main__':
  # app.debug = True
  app.run()

