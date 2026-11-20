from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
    from app.routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify(error="Request too large"), 413

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify(error="Internal server error"), 500

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["Cache-Control"] = "no-store"
        return response

    return app
