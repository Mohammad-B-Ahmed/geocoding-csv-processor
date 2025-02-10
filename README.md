# Address Geocoding Tool

A Python tool to automatically geocode addresses from CSV files and update their latitude/longitude coordinates.

## Available Approaches

This tool offers two different approaches for geocoding:

1. **Simple Approach** (`main_first.py`):
   - Uses basic importance scoring from the API
   - Takes the first result with highest importance
   - Lighter and simpler implementation

2. **Smart Approach** (`main.py`):
   - Smarter address matching
   - Handles city names and locations separately (e.g., "Erbil Brayaty")
   - Better scoring system considering place types and address components
   - Recommended for addresses with city names

To switch between approaches:
1. Delete or rename the current `main.py`
2. Rename your chosen approach file to `main.py`

## Features

- Processes CSV files containing addresses
- Automatically fetches coordinates using geocoding API
- Skips addresses that already have coordinates
- Rate limiting to respect API constraints
- Progress tracking during processing
- File size validation (max 3000 rows)
- Smart address matching (in main.py)
- City-location recognition (in main.py)

## Prerequisites

- Python 3.6 or higher
- Internet connection for API access
- Geocoding API key from [geocode.maps.co](https://geocode.maps.co)

## Installation

1. Clone or download this repository
2. Install required packages:
```bash
pip install python-dotenv requests
```
3. Choose your approach (main.py or main_first.py)

## Configuration

1. Create a `.env` file in the project directory
2. Add the following configuration (modify as needed):
```env
# Your API key from geocode.maps.co
GEOCODING_API_KEY=your_api_key_here

# CSV column names
CSV_ADDRESS_COLUMN=address
CSV_LAT_COLUMN=lat
CSV_LNG_COLUMN=lng

# Processing limits
MAX_ROWS=3000
REQUEST_DELAY=1
```

### Configuration Options

- `GEOCODING_API_KEY`: Your API key from geocode.maps.co
- `CSV_ADDRESS_COLUMN`: Name of the column containing addresses
- `CSV_LAT_COLUMN`: Name of the column for latitude values
- `CSV_LNG_COLUMN`: Name of the column for longitude values
- `MAX_ROWS`: Maximum number of rows to process
- `REQUEST_DELAY`: Delay between API requests in seconds

## Usage

Run the script with input and output file paths:
```bash
python main.py input.csv output.csv
```

### Examples:

Using files in the same directory:
```bash
python main.py addresses.csv results.csv
```

Using full file paths:
```bash
python main.py C:/Data/addresses.csv C:/Data/processed_addresses.csv
```

## CSV File Requirements

Your input CSV file should:
- Have the column names specified in your .env file
- Not exceed the MAX_ROWS limit (default 3000)
- Be properly formatted CSV

Example CSV format:
```csv
address,lat,lng,name,phone
"123 Main St, City, Country",,,"John Doe","123-456-7890"
"Erbil Brayaty",,,"Jane Smith","456-789-0123"
```

## How It Works

### Simple Approach (main_first.py)
- Uses the API's importance score directly
- Selects the result with highest importance score
- Good for simple address lookups

### Smart Approach (main.py)
- Analyzes address components (city, location)
- Higher score for matching city names
- Considers place types (city, street, amenity)
- Better for addresses with city names (e.g., "Erbil Brayaty")

## Error Handling

The script will show error messages for:
- Missing required columns
- Files exceeding size limit
- API request failures
- Invalid addresses

## Rate Limiting

- Default delay is 1 second between requests
- Adjust REQUEST_DELAY in .env if needed
- Be mindful of API provider's rate limits

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)
