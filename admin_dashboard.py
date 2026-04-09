from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os

def create_admin_app():
    app = Flask(__name__, 
                template_folder='admin_dashboard/templates',
                static_folder='admin_dashboard/static')
    
    CORS(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login.html')
    def login_page():
        return render_template('login.html')
    
    @app.route('/user_dashboard.html')
    def user_dashboard():
        return render_template('user_dashboard.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('admin_dashboard/static', filename)
    
    return app

if __name__ == '__main__':
    app = create_admin_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
