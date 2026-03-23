import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import blueprints
from interfaces.api.chat import chat_bp
from interfaces.api.payments import payments_bp

app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(payments_bp, url_prefix='/api/payments')

@socketio.on('message')
def handle_message(data):
    # Process voice/text from frontend
    from core.brain import Brain
    from core.personality import Personality
    brain = Brain(Personality())
    response = brain.generate(data['message'])
    socketio.emit('response', {'reply': response})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
