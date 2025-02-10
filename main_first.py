# main.py
import csv
import requests
import time
from config import Config

def geocode_address(address):
    """Convert a single address to latitude and longitude."""
    # Wait 1 second before making request (API limit)
    time.sleep(1)
    
    try:
        # Make request to geocoding API
        url = Config.BASE_URL
        params = {
            'q': address,
            'api_key': Config.API_KEY
        }
        
        response = requests.get(url, params=params)
        results = response.json()
        
        if not results:
            print(f"No results found for: {address}")
            return None, None
            
        # Take the first result (usually most relevant)
        best_result = results[0]
        return best_result['lat'], best_result['lon']
        
    except Exception as e:
        print(f"Error with address '{address}': {e}")
        return None, None

def update_coordinates(input_file, output_file):
    """Update coordinates in CSV file."""
    try:
        # First, count rows to check file size
        with open(input_file, 'r', encoding='utf-8') as f:
            row_count = sum(1 for _ in f) - 1  # Subtract 1 for header
            
        if row_count > Config.MAX_ROWS:
            print(f"Error: File has {row_count} rows. Maximum allowed is {Config.MAX_ROWS}")
            return
            
        # Process the file
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            # Set up CSV reading and writing
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Check if required columns exist
            if Config.ADDRESS_COLUMN not in fieldnames:
                print(f"Error: Address column '{Config.ADDRESS_COLUMN}' not found in CSV")
                return
                
            if Config.LAT_COLUMN not in fieldnames or Config.LNG_COLUMN not in fieldnames:
                print(f"Error: Latitude column '{Config.LAT_COLUMN}' or Longitude column '{Config.LNG_COLUMN}' not found in CSV")
                return
            
            # Process each row
            rows_processed = 0
            for row in reader:
                # Only process if coordinates are missing
                if not row[Config.LAT_COLUMN] or not row[Config.LNG_COLUMN]:
                    address = row[Config.ADDRESS_COLUMN]
                    if address:
                        lat, lng = geocode_address(address)
                        if lat and lng:
                            row[Config.LAT_COLUMN] = lat
                            row[Config.LNG_COLUMN] = lng
                
                writer.writerow(row)
                rows_processed += 1
                print(f"Processed {rows_processed} of {row_count} rows", end='\r')
            
            print(f"\nFinished! Processed {rows_processed} rows")
            
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    import sys
    
    # Show usage if no arguments provided
    if len(sys.argv) != 3:
        print("Usage:")
        print("python main.py input.csv output.csv")
        print("\nExample:")
        print("python main.py addresses.csv updated_addresses.csv")
        sys.exit(1)
    
    # Get input and output filenames from command line
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Run the update
    update_coordinates(input_file, output_file)