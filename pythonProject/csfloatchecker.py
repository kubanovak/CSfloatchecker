import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

API_KEY = 'xxx' 
API_URL = 'https://csfloat.com/api/v1/listings'
HEADERS = {
    'Authorization': f'{API_KEY}'
}

# Set the filters and parameters
params = {
    'page': 0,
    'limit': 50 ,#ax listings per request
    'sort_by': 'most_recent',  # Sort by most recent listings
    'category': 0,  # 0 for any, 1 for normal, 2 for stattrak, 3 for souvenir
    'min_price': 3000,  # Minimum price in cents (e.g., 1000 = $10)
    'max_price': 40000,  # Maximum price in cents
    'min_float': 0.01,  # Minimum float value
    'max_float': 0.8,  # Maximum float value
    'type': 'buy_now'
}

# Set to keep track of already printed listings by their ID
printed_ids = set()

# Define color codes
PURPLE = '\033[95m'
ORANGE = '\033[93m'
GREEN = '\033[92m'  # Green for percentage < 0
RED = '\033[91m'    # Red for percentage > 0
RESET = '\033[0m'

def fetch_percentage_from_api(csfloat_link):
    try:
        response = requests.get(csfloat_link)
        if response.status_code == 200:
            dict_dump = response.json()
            predicted = dict_dump["reference"]["predicted_price"]
            actual = dict_dump["price"]

            # Calculate the percentage difference
            percentage = round(((actual / predicted) - 1) * 100, 1)
            return percentage
        else:
            print(f"Error fetching data from {csfloat_link}: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while fetching percentage: {e}")
    return "N/A"

def fetch_new_listings():
    try:
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            listings = response.json()
            return listings
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return None

# Function to process each listing
def process_listing(listing):
    listing_id = listing['id']

    # Safely check if 'min_offer_price' exists in the listing
    if listing_id not in printed_ids and 'min_offer_price' in listing and listing['min_offer_price'] <= 40000:
        # Check if seller stats match the conditions
        seller = listing.get('seller', {})
        statistics = seller.get('statistics', {})
        if statistics.get('total_failed_trades') <= 5 and statistics.get('total_trades') <= 10:
            # Create the CSFloat link for the listing
            csfloat_link = f"https://csfloat.com/item/{listing_id}"

            # Retrieve item name for highlighting
            item_name = listing['item']['market_hash_name']

            # Check if '★' or 'stattrak' is in the item name
            if '★' in item_name.lower():
                item_name = f"{PURPLE}{item_name}{RESET}"
            elif 'stattrak' in item_name.lower():
                item_name = f"{ORANGE}{item_name}{RESET}"

            # Fetch the percentage using the simplified API call
            percentage = fetch_percentage_from_api(f"https://csfloat.com/api/v1/listings/{listing_id}")

            # Color code the percentage based on its value
            if percentage != "N/A":
                if percentage < 0:
                    colored_percentage = f"{GREEN}{percentage}%{RESET}"  # Green for < 0
                elif percentage > 0:
                    colored_percentage = f"{RED}{percentage}%{RESET}"    # Red for > 0
                else:
                    colored_percentage = f"{percentage}%"  # No color for 0
            else:
                colored_percentage = "N/A"  # In case of an issue

            # Print out the item details with a clickable link to the CSFloat listing
            print(f"{item_name} | Price: {listing['price'] / 100}$ | "
                  f"Float: {listing['item']['float_value']} | Min Offer Price: {listing['min_offer_price'] / 100}$ | "
                  f"{colored_percentage} | "
                  f"{csfloat_link}")

            # Add the listing ID to avoid duplicates
            printed_ids.add(listing_id)

# Polling loop
while True:
    new_listings = fetch_new_listings()
    if new_listings:
        print("Searching for listings...")
        with ThreadPoolExecutor(max_workers=10) as executor:
            for listing in new_listings:
                executor.submit(process_listing, listing)

    time.sleep(random.uniform(5, 10))  # Reduced sleep time to speed up requests
