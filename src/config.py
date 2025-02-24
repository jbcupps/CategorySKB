from datetime import datetime

class Config:
    # Dynamic date that updates automatically
    @staticmethod
    def get_display_date():
        return datetime.now().strftime("%B %d, %Y")
    
    # Physics model parameters
    DEFAULT_GAMMA = 313.09
    DEFAULT_DELTA = 0.0
    DEFAULT_EPSILON = 0.511
    
    # Flask configuration
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    
    # Validation settings
    VALID_COLORS = ['red', 'green', 'blue']
    VALID_GENERATIONS = [1, 2, 3]