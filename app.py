from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postges:abed11@10.0.0.31/mydatabase'

# Create the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define the model for the database table
class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Example %r>' % self.email

# Define a route to return a JSON response when a GET request is made
@app.route('/api/get', methods=['GET'])
def example_api():
    examples = Example.query.all()
    response = []
    for example in examples:
        response.append({
            'id': example.id,
            'email': example.email,
            'password': example.password
        })
    return jsonify(response)

# Define a route to handle a POST request
@app.route('/api/post', methods=['POST'])
def add_example():
    email = request.json['email']
    password = request.json['password']
    example = Example(email, password)
    db.session.add(example)
    db.session.commit()
    return jsonify({'message': 'Example added successfully!'})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)