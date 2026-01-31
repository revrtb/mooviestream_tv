"""
Configuration settings for the Flask application.
"""

class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = 'your-secret-key-here'  # Change this in production!
    DEBUG = True
    TESTING = False
    
    # Application settings
    APP_NAME = 'Movie Website'
    ADMIN_EMAIL = 'admin@example.com'
    
    # Database settings (if needed)
    # DATABASE_URI = 'sqlite:///site.db'
    
    # API keys and external services
    # NOTE: You need to get a valid API key from https://www.themoviedb.org/settings/api
    # and replace the placeholder below with your actual key for the application to work.
    TMDB_API_KEY = '7045bc4055c6293e84534dd8f6dbb024'  # Replace with your actual TMDB API key
    TMDB_API_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/'
    VIDSRC_BASE_URL = 'https://vidsrc.to/embed/movie/'
    EMBESS_BASE_URL = 'https://api.embess.ws/embed/imdb/'
    
    # File upload settings (if needed)
    # UPLOAD_FOLDER = 'static/uploads'
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Use a strong secret key in production
    SECRET_KEY = 'production-secret-key'  # Change this!

# Set the active configuration
Config = DevelopmentConfig  # Change to ProductionConfig for production