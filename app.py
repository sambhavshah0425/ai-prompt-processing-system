from flask import Flask, jsonify, render_template
from config import Config
from database.mongo import Database
from routes.generate import generate_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database
    Database.initialize()

    # Register Blueprints
    app.register_blueprint(generate_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    # Custom Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
