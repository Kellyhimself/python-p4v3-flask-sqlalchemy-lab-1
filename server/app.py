# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)

    if earthquake is not None:
        body = earthquake.to_dict()
        body['year'] = int(body['year'])  # Convert year from string to int
        return make_response(body, 200)
    else:
        body = {'message': f'Earthquake {id} not found.'}
        return make_response(body, 404)

@app.route('/earthquakes/magnitude/<float:Emagnitude>')
def earthquake(Emagnitude):
    
    earthquakes =[]
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= Emagnitude).all():
        earthquake = earthquake.to_dict()
        earthquake['year'] = int(earthquake['year'])  # Convert year from string to int
        earthquakes.append(earthquake)      
    body = {'count': len(earthquakes),
            'quakes': earthquakes
            }
    return make_response(body, 200)




if __name__ == '__main__':
    app.run(port=5555, debug=True)
