#!/usr/bin/env python3
# ^ shebang line for Linux/MacOS

# Import necessary modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import os

# Declare start_time for final calculation of elapsed_time
start_time = time.time()

# Declare url of site to scrape
url = "https://quotes.toscrape.com"

# Set up empty list for scrape results
results = []

# While loop to cycle through pagination
while url:

    # Try-except block to verify successful connection to website
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        break

    # Make delicious data soup!
    soup = BeautifulSoup(response.text, "html.parser")

    # Check that our soup has data by checking the title
    print(soup.title.text)

    # Extract quote blocks from soup
    quotes = soup.find_all("div", class_="quote")

    # Verify count of extracted quote blocks
    print("Quote blocks found:", len(quotes))

    # separate important data from quote blocks and store in 'results' list
    for quote in quotes:

        # Try-except block to make sure html formatting hasn't changed
        try:
            text = quote.find("span", class_="text").get_text(strip=True)

            author = quote.find("small", class_="author").get_text(strip=True)

            tag_elements = quote.find_all("a", class_="tag")

            tags = []        

            for tag in tag_elements:
                tags.append(tag.get_text(strip=True))

        except AttributeError as e:
            print(f"Failed to process quote: {e}")
            continue
    
        row_data = {
            'quote': text,
            'author': author,
            'tags': tags
        }
        results.append(row_data)

    # Extract next button from soup
    next_button = soup.find("li", class_="next")

    # logic: if there is a next button, extract and format the url
    if next_button:
        relative_url = next_button.find("a")["href"]
        next_url = urljoin(url, relative_url)

        print('"Next" button url:', next_url)
        print()

        url = next_url

    # logic: if there is no next button, there is no url
    else:
        print("No 'Next' button found. Scraping complete.")
        url = None


# create dataframe from 'results' list
df = pd.DataFrame(results)

# sanity check dataframe
print()
print(df.info())
print()
print(df.head())

# Show number of quotes scraped
print("\n==========\nTotal quotes scraped:", len(df))

# Clean tags for CSV-friendly formatting
df["tags"] = df["tags"].apply(lambda tags: ", ".join(tags))

# Define filename for CSV output
filename = 'quotes.csv'

# Create CSV file from dataframe
try:
    df.to_csv(filename, index=False)
except OSError as e:
    print(f'Failed to create {filename}: {e}')
else:
    print(f"{filename} successfully created.")

# Check that CSV file exists
if os.path.exists(filename):
    print(f'{filename} existence verified.')
else:
    print(f'Unable to verify existence of {filename}.')

# Declare end time and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Operation completed in {elapsed_time:.2f} seconds.')