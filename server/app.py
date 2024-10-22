##done
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
       messages = Message.query.order_by(Message.created_at.asc()).all()
       return ([{'id': message.id, 'body': message.body, 'created_at': message.created_at} for message in messages])
    elif request.method == 'POST':
        if 'body' not in request.get_json() or 'username' not in request.get_json():
            return jsonify({'message': 'Body and username are required'}), 400
        new_message = Message(body=request.get_json()['body'], username=request.get_json()['username'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'id': new_message.id, 'body': new_message.body, 'username': new_message.username, 'created_at': new_message.created_at}), 201

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if message is None:
        return jsonify({'message': 'Message not found'}), 404
    if request.method == 'GET':
        return jsonify({'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at})
    elif request.method == 'PATCH':
        if 'body' in request.json:
            message.body = request.json['body']
        db.session.commit()
        return jsonify({'id': message.id, 'body': message.body, 'username': message.username, 'created_at': message.created_at})
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully', 'id': id}), 200

if __name__ == '__main__':
    app.run(port=5555)