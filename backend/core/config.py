import os

class Settings:
    PROJECT_NAME: str = "GalaxEye System"
    
    # Security: Use an environment variable, or a secure default
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Paths
    MODEL_PATH: str = "model_artifacts/astro_classifier_model.pkl"
    DATA_PATH: str = "cleaned_star_galaxy_quasar_data.csv"
    
    # API URL for Frontend
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://backend:8000")

settings = Settings()