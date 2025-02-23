from flask import jsonify
from werkzeug.exceptions import HTTPException

class SKBError(Exception):
    """Base exception for SKB application"""
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            'error': self.message,
            'status_code': self.status_code
        }

class ValidationError(SKBError):
    """Raised when SKB validation fails"""
    pass

class IntegrationError(SKBError):
    """Raised when quark integration fails"""
    pass

class AnalysisError(SKBError):
    """Raised when SKB analysis fails"""
    pass

def register_error_handlers(app):
    @app.errorhandler(SKBError)
    def handle_skb_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        response = jsonify({
            'error': error.description,
            'status_code': error.code
        })
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        response = jsonify({
            'error': str(error),
            'status_code': 500
        })
        response.status_code = 500
        return response 