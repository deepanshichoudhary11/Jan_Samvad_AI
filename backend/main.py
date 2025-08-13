from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from api.auth_routes import auth_bp
from api.complaint_routes import complaint_bp
from api.scheme_routes import scheme_bp
from api.helpline_routes import helpline_bp
from api.ai_routes import ai_bp
from api.voice_routes import voice_bp
from api.emergency_routes import emergency_bp
from api.email_service import init_mail

# Load environment variables
load_dotenv()

# Point static_folder to React build
app = Flask(__name__, static_folder='build')
CORS(app)

# Initialize email service with error handling
try:
    init_mail(app)
except Exception as e:
    print(f"⚠️ Email service initialization failed: {e}")
    print("📧 Email features will be disabled. Please check your .env file configuration.")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(complaint_bp, url_prefix='/api/complaint')
app.register_blueprint(scheme_bp, url_prefix='/api/schemes')
app.register_blueprint(helpline_bp, url_prefix='/api/helpline')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(voice_bp, url_prefix='/api/voice')
app.register_blueprint(emergency_bp, url_prefix='/api/emergency')

# Backend API test route
@app.route('/api')
def api_test():
    return {'message': 'JanAI Backend API is running!'}

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    print("🚀 Starting JanAI Fullstack Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
