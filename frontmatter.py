import math
import os
import json
import yaml
from datetime import date, datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

def extract_frontmatter(mdx_file_path):
    with open(mdx_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract the frontmatter section
    frontmatter_parts = content.split('---')
    if len(frontmatter_parts) > 1:
        frontmatter = frontmatter_parts[1].strip()
        # Parse the YAML frontmatter
        frontmatter_data = yaml.safe_load(frontmatter)
        
        return frontmatter_data
    else:
        return None
    
def calculate_reading_time(mdx_file_path):
    words_per_minute = 150
    
    try:
        with open(mdx_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Removing frontmatter (if present)
            if content.startswith('---'):
                content = content.split('---', 2)[2]
            
            words = content.split()
            num_words = len(words)
            reading_time_minutes = num_words / words_per_minute
            
            return math.ceil(reading_time_minutes)  # Returning reading time rounded to 2 decimal places
    except FileNotFoundError:
        print(f"File not found: {mdx_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def convert_all_mdx_to_json(mdx_directory, output_json_path):
    frontmatter_collection = []

    # Traverse the directory to find all MDX files
    for root, _, files in os.walk(mdx_directory):
        for file in files:
            if file.endswith('.mdx'):
                file_path = os.path.join(root, file)
                frontmatter_data = extract_frontmatter(file_path)
                if frontmatter_data and frontmatter_data['published']:
                    # Use the file name (without extension) as the key
                    file_name = os.path.splitext(file)[0]
                    frontmatter_data['slug'] = file_name
                    frontmatter_data['readingTime'] = calculate_reading_time(file_path)
                    frontmatter_collection.append(frontmatter_data)
                    
    # sort the collection by date here
    frontmatter_collection.sort(key=lambda x: x['date'], reverse=True)

    # Write the collection of frontmatter to a single JSON file
    with open(output_json_path, 'w', encoding='utf-8') as output_file:
        json.dump(frontmatter_collection, output_file, indent=4, cls=CustomJSONEncoder)


# Usage example
mdx_directory = './'
output_json_path = './frontmatters.json'
convert_all_mdx_to_json(mdx_directory, output_json_path)
print(f"Frontmatter data from all MDX files has been written to {output_json_path}")
