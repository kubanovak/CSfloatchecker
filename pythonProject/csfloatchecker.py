import requests
import time
import random

API_KEY = '9oVP1ot5B35fV3VORyiNtjNfC_S813M_'  # Replace with your actual CSFloat API key
API_URL = 'https://csfloat.com/api/v1/listings'
HEADERS = {
    'Authorization': f'{API_KEY}'
}

# Set the filters and parameters
params = {
    'page': 0,
    'limit': 50,  # Max listings per request
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

# Polling loop
while True:
    new_listings = fetch_new_listings()
    if new_listings:
        for listing in new_listings:
            listing_id = listing['id']

            # Safely check if 'min_offer_price' exists in the listing
            if listing_id not in printed_ids and 'min_offer_price' in listing and listing['min_offer_price'] <= 7835:

                # Check if seller stats match the conditions
                seller = listing.get('seller', {})
                statistics = seller.get('statistics', {})
                if statistics.get('total_failed_trades') <= 5 and statistics.get('total_trades') <= 10:

                    # Create the CSFloat link for the listing (using 'asset_id' or other relevant identifiers)
                    asset_id = listing['item'].get('asset_id', 'unknown')
                    csfloat_link = f"https://csfloat.com/item/{listing_id}"

                    # Print out the item details with a clickable link to the CSFloat listing
                    print(f"{listing['item']['market_hash_name']} | Price: {listing['price'] / 100}$ | "
                          f"Float: {listing['item']['float_value']} | Min Offer Price: {listing['min_offer_price'] / 100}$ | "
                          f"Link: {csfloat_link}")

                    # Add the listing ID to avoid duplicates
                    printed_ids.add(listing_id)

    time.sleep(random.uniform(5,10))
