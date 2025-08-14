import os

API_KEY = os.environ.get('AMADEUS_API_KEY')
API_SECRET = os.environ.get('AMADEUS_API_SECRET')

if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY and API_SECRET must be set in environment variables.")
