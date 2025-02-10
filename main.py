# main.py
import csv
import requests
import time
from config import Config

def clean_address(address):
    """Clean and split address into parts."""
    if not address:
        return []
    return [part.strip().lower() for part in address.split() if part.strip()]

def score_result(result, search_parts):
    """Score a result based on how well it matches the search terms."""
    score = result.get('importance', 0)
    display_name = result.get('display_name', '').lower()
    
    if len(search_parts) > 1:
        city = search_parts[0]
        location = search_parts[1]
        
        if city in display_name and location in display_name:
            score += 0.5
        elif city in display_name:
            score += 0.3
        elif location in display_name:
            score += 0.1
    else:
        if search_parts[0] in display_name:
            score += 0.2
    
    if result['class'] == 'place':
        score += 0.3
    elif result['class'] == 'highway':
        score += 0.2
    elif result['class'] == 'amenity':
        score += 0.1
    
    return score

def geocode_address(address):
    """Convert a single address to latitude and longitude."""
    time.sleep(Config.REQUEST_DELAY)
    
    try:
        search_parts = clean_address(address)
        if not search_parts:
            return None, None
            
        params = {
            'q': address,
            'api_key': Config.API_KEY
        }
        
        response = requests.get(Config.BASE_URL, params=params)
        results = response.json()
        
        if not results:
            return None, None
            
        # Score all results but don't print debugging info
        scored_results = [(score_result(result, search_parts), i, result) 
                         for i, result in enumerate(results)]
        
        # Sort by score, then by original order (for equal scores)
        scored_results.sort(key=lambda x: (-x[0], x[1]))
        
        # Take the best result (highest score, or first one if equal scores)
        best_result = scored_results[0][2]
        return best_result['lat'], best_result['lon']
        
    except Exception as e:
        return None, None

def update_coordinates(input_file, output_file):
    """Update coordinates in CSV file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            row_count = sum(1 for _ in f) - 1
            
        if row_count > Config.MAX_ROWS:
            print(f"Error: File has {row_count} rows. Maximum allowed is {Config.MAX_ROWS}")
            return
            
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            if Config.ADDRESS_COLUMN not in fieldnames:
                print(f"Error: Address column '{Config.ADDRESS_COLUMN}' not found in CSV")
                return
                
            if Config.LAT_COLUMN not in fieldnames or Config.LNG_COLUMN not in fieldnames:
                print(f"Error: Latitude/Longitude columns not found in CSV")
                return
            
            rows_processed = 0
            for row in reader:
                if not row[Config.LAT_COLUMN] or not row[Config.LNG_COLUMN]:
                    address = row[Config.ADDRESS_COLUMN]
                    if address:
                        lat, lng = geocode_address(address)
                        if lat and lng:
                            row[Config.LAT_COLUMN] = lat
                            row[Config.LNG_COLUMN] = lng
                
                writer.writerow(row)
                rows_processed += 1
                if rows_processed % 10 == 0:  # Update progress every 10 rows
                    print(f"Processing: {rows_processed}/{row_count} rows", end='\r')
            
            print(f"\nCompleted! Processed {rows_processed} rows")
            
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python main.py input.csv output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    update_coordinates(input_file, output_file)