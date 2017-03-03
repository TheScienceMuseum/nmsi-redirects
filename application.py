from flask import Flask 
from flask import redirect 
from flask import request 

import csv
import urllib.parse

# example of old url
# http://collectionsonline.nmsi.ac.uk/detail.php?type=related&kv=66468&t=objects

application = Flask(__name__)

courl = 'https://collection.sciencemuseum.org.uk'
lookup = {}

# load mapping table into a dictonary keyed on kv value
application.logger.info('loading mappings');
f = open('lookup.csv', "r", encoding='latin-1')
try:
  reader = csv.reader(f)
  for row in reader:
    lookup[row[0]] = row[1]
except OSError as err:
    application.logger.debug("OS error: {0}".format(err))
except ValueError:
    application.logger.debug("Could not convert data")
except:
    application.logger.debug("Unexpected error:", sys.exc_info()[0])
    raise
finally:
    f.close()

@application.route('/') 
def index():
  return redirect(courl, code=301);

@application.route('/detail.php') 
def match():
  if request.args.get('t') == 'people':
    return redirect(courl + '/search/people', code=301)
  else:
    try:
      return redirect(courl + '/oid/' + urllib.parse.quote(lookup[request.args.get('kv')], safe='') + "?redirect=true")
    except KeyError:
      application.logger.info("Could not find kv value")
      return redirect(courl, code=301)

@application.errorhandler(404)
def not_found(error):
  return redirect(courl, code=301)

if __name__ == '__main__':
  # application.debug = True
  application.run()

