from flask import Flask, render_template, send_from_directory
from pathlib import Path
import os
from dotenv import load_dotenv
from .errors import register_error_handlers
from .logging_config import setup_logging

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__,
                static_url_path='',
                static_folder=Path(__file__).parent / 'static',
                template_folder=Path(__file__).parent / 'templates')

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'skb.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up logging
    setup_logging(app)

    # Register error handlers
    register_error_handlers(app)

    @app.route('/')
    def intro():
        app.logger.info('Serving intro page')
        return render_template('index.html')

    @app.route('/modeler')
    def modeler():
        app.logger.info('Serving modeler page')
        return render_template('modeler.html')

    @app.route('/analysis')
    def analysis():
        app.logger.info('Serving analysis page')
        return render_template('analysis.html')

    # Register blueprints here
    from . import skb
    app.register_blueprint(skb.bp)
    app.logger.info('Registered SKB blueprint')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)