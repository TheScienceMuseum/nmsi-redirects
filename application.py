from flask import Flask 
from flask import redirect 
from flask import request 

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
except OSError as err:
    app.logger.debug("OS error: {0}".format(err))
except ValueError:
    app.logger.debug("Could not convert data")
except:
    app.logger.debug("Unexpected error:", sys.exc_info()[0])
    raise
finally:
    f.close()

@app.route('/') 
def index():
  return redirect(courl);

@app.route('/detail.php') 
def match():
  try:
    return redirect(courl + '/oid/' + lookup[request.args.get('kv')] + "?redirect=true")
  except KeyError:
    app.logger.info("Could not find kv value")
    return redirect(courl)

if __name__ == '__main__':
  app.debug = True
  app.run()

