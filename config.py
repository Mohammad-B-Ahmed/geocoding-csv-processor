from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_KEY = os.getenv('GEOCODING_API_KEY')
    ADDRESS_COLUMN = os.getenv('CSV_ADDRESS_COLUMN', 'address')
    LAT_COLUMN = os.getenv('CSV_LAT_COLUMN', 'lat')
    LNG_COLUMN = os.getenv('CSV_LNG_COLUMN', 'lng')
    MAX_ROWS = int(os.getenv('MAX_ROWS', 3000))
    REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', 1))
    BASE_URL = "https://geocode.maps.co/search"