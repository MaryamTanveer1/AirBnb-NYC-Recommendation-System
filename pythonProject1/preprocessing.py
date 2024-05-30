import pandas as pd

# Read the dataset
df = pd.read_csv('C:\\Users\\Saeed\\Desktop\\modified_dataset5.csv', dtype={'nurl_image': str, 'imagefor_name': str})

# Drop rows where 'availability_365' is 0
df = df[df['availability_365'] != 0]

# Convert 'last_review' column to datetime format
df['last_review'] = pd.to_datetime(df['last_review'])

# Fill missing values in 'last_review' with the latest date
latest_date = df['last_review'].max()
df['last_review'] = df['last_review'].fillna(latest_date)

# Drop the 'reviews_per_month' column
df = df.drop(columns=['reviews_per_month'])

# Extract the column containing image URLs
image_urls = df['nurl_image'].dropna().tolist()

# Calculate the length of the dataset
dataset_length = len(df)

# Repeat the URLs cyclically to match the length of the dataset
repeated_image_urls = (image_urls * (dataset_length // len(image_urls) + 1))[:dataset_length]

# Update the DataFrame with the repeated image URLs
df['imagefor_name'] = repeated_image_urls

# Drop the 'calculated_host_listings_count' column
df = df.drop(columns=['calculated_host_listings_count'])

# Drop rows with duplicate values in the 'id' column
df = df.drop_duplicates(subset=['id'])

# Delete rows where only 2 columns have null or empty values
df = df.dropna(thresh=len(df.columns) - 2)

# Save the modified dataset to a new file
df.to_csv('C:\\Users\\Saeed\\Desktop\\modified_dataset9.csv', index=False)
