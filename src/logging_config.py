import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(app):
    # Create logs directory if it doesn't exist
    log_dir = Path(app.instance_path) / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    # Set up file handler
    file_handler = RotatingFileHandler(
        log_dir / 'skb.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))
    console_handler.setLevel(logging.INFO)

    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info('SKB startup') 