import flask
from flask.helpers import flash
from db import get_db, init

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(init)

@app.route('/',  methods=['GET'])
def index():

    return flask.render_template('webform/index.html')

@app.route('/postregions',  methods=['POST'])
def postregions():

    if flask.request.method == 'POST':

        print(flask.request.json)

        name = flask.request.json['name']
        regions = flask.request.json['regions']

        print(regions)

        sregions = ','.join(str(e) for e in regions)

        error = None

        if not name:
            error = 'Name is Required'

        if error is not None:
            return flask.json.dumps({'Error': error}), 400, {'ContentType':'application/json'} 
        else:
            db = get_db()
            db.execute(
                'INSERT INTO regions (name, regions)'
                'VALUES (?, ?)',
                (name, sregions)
            )
            db.commit()
        
        return flask.json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':

    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    
    app.run(host='0.0.0.0')
