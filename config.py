import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Application Settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # API Rate Limiting
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', 1.0))
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 60))
    
    # Data Sources Configuration
    USE_GOOGLE_SCHOLAR = os.getenv('USE_GOOGLE_SCHOLAR', 'True').lower() == 'true'
    USE_ARXIV = os.getenv('USE_ARXIV', 'True').lower() == 'true'
    USE_SEMANTIC_SCHOLAR = os.getenv('USE_SEMANTIC_SCHOLAR', 'True').lower() == 'true'
    USE_RESEARCHGATE = os.getenv('USE_RESEARCHGATE', 'True').lower() == 'true'
    
    # Semantic Scholar API (optional)
    SEMANTIC_SCHOLAR_API_KEY = os.getenv('SEMANTIC_SCHOLAR_API_KEY', '')
    
    # Model Configuration
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.7))
    MAX_RESULTS = int(os.getenv('MAX_RESULTS', 50))
    
    # File paths
    UPLOAD_FOLDER = 'uploads'
    RESULTS_FOLDER = 'results'
    
    # Supported export formats
    EXPORT_FORMATS = ['csv', 'json', 'pdf', 'excel'] 