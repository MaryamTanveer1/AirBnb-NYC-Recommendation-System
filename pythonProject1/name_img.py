from google_images_search import GoogleImagesSearch
import pandas as pd

API_KEY = 'AIzaSyB7CcF4xiZqKE3yAmjBDZct4_HHs27gL7Y'
SEARCH_ENGINE_ID = 'd7e74b48d90e7441c'

# Initialize GoogleImagesSearch object
gis = GoogleImagesSearch(API_KEY, SEARCH_ENGINE_ID)

# Load existing dataset containing 'name' column
existing_data_df = pd.read_csv('C:\\Users\\Saeed\\Desktop\\modified_dataset62.csv')

# Fetch only the first 4000 rows
existing_data_df = existing_data_df.iloc[:100]

# Create empty list to store dictionaries of data
data_list = []

# Iterate through the 'name' column values
for name in existing_data_df['name']:
    # Perform Google Images search for the name
    gis.search({'q': f'{name}', 'num': 1})  # Searching for images related to the name

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

    # Append dictionary containing 'name' and 'image_url' to the list
    data_list.append({'name': name, 'nurl_image': image_url})

# Create DataFrame from the list of dictionaries
image_urls_df = pd.DataFrame(data_list)

# Merge the existing data with image URLs DataFrame on 'name' column
merged_data_df = pd.merge(existing_data_df, image_urls_df, on='name', how='left')

# Print DataFrame containing merged data
print("Merged Data:")
print(merged_data_df.to_string(index=False))

# Save the merged data to a new CSV file
merged_data_df.to_csv("C:\\Users\\Saeed\\Desktop\\modified_dataset7.csv.csv")
