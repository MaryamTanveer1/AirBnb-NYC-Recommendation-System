from google_images_search import GoogleImagesSearch
import pandas as pd

# Replace 'YOUR_GOOGLE_API_KEY' and 'YOUR_GOOGLE_SEARCH_ENGINE_ID' with your actual Google API key and search engine ID
API_KEY = 'AIzaSyBNP4UwLrO4Oy0zXVuRh69CkpJsRQR_-5k'
SEARCH_ENGINE_ID = '04adc926e357f4879'

# Categories to search for images
categories = ['Brooklyn', 'Manhattan', 'Bronx', 'Queens', 'Staten Island']

# Initialize GoogleImagesSearch object
gis = GoogleImagesSearch(API_KEY, SEARCH_ENGINE_ID)

# Load existing dataset containing 'neighbourhood_group' column
existing_data_df = pd.read_csv('C:\\Users\\Saeed\\Desktop\\airbnb.csv')

# Create empty list to store dictionaries of data
data_list = []

# Perform Google Images search for each category
for category in categories:
    # Perform search
    gis.search({'q': f'{category} cityscape', 'num': 1})  # Searching for cityscape images of each category

    # Get search results
    results = gis.results()

    # Check if there are any results
    if results:
        result = results[0]
        # Extract image URL
        image_url = result.url
    else:
        # If no results found, set image URL to None
        image_url = None

    # Append dictionary containing 'neighbourhood_group' and 'image_url' to the list
    data_list.append({'neighbourhood_group': category, 'image_url': image_url})

# Create DataFrame from the list of dictionaries
image_urls_df = pd.DataFrame(data_list)

# Merge the existing data with image URLs DataFrame on 'neighbourhood_group' column
merged_data_df = pd.merge(existing_data_df, image_urls_df, on='neighbourhood_group', how='left')

# Print DataFrame containing merged data
print("Merged Data:")
print(merged_data_df.to_string(index=False))

merged_data_df.to_csv("C:\\Users\\Saeed\\Desktop\\merged_data1.csv")