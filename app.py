from flask import Flask, jsonify, render_template
from config import Config
from database.mongo import Database
from routes.generate import generate_bp
import os

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    Database.initialize()

    # Register routes
    app.register_blueprint(generate_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy"
        }), 200

    return app

app = create_app()

if __name__ == '__main__':

    app.run(
        debug=False,
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000))
    )