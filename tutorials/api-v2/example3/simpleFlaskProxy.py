#based on this code: https://medium.com/@zwork101/making-a-flask-proxy-server-online-in-10-lines-of-code-44b8721bca6

#run with this command: flask --app simpleFlaskProxy run

#dst: https://images.metmuseum.org/

from flask import Flask, Response
from flask_cors import CORS
from requests import get

app = Flask(__name__)
CORS(app)
SITE_NAME = 'https://images.metmuseum.org/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
  
  if 'jpg' in path:
    mt = 'image/jpg'
  elif 'png' in path:
    mt = 'image/png'

  #print(f'{SITE_NAME}{path}')
  image = get(f'{SITE_NAME}{path}').content
  return Response(image,mimetype=mt)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)