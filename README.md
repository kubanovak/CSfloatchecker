# CSFloat Filtering Program

A Python script that checks recent listings on CSFloat for inexperienced traders and filters items based on specified criteria. The program analyzes listings and highlights important details like item name, price, float value, and seller stats.

## Features
- Filters listings based on price, float value, and seller trade statistics.
- Highlights items such as ★ (knives) and StatTrak with color-coded output.
- Fetches percentage differences between predicted and actual prices.
- Avoids duplicates by tracking processed listing IDs.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/csfloatchecker.git
   cd csfloatchecker
   ```
2. Install required dependencies:
   ```bash
   pip install requests
   ```

## Configuration
1. Replace the placeholder API key (`API_KEY`) in the script with your CSFloat API key:
   ```python
   API_KEY = 'your_api_key_here'
   ```
2. Adjust filters (e.g., price range, float range) in the `params` dictionary within the script:
   ```python
   params = {
       'min_price': 3000,
       'max_price': 40000,
       'min_float': 0.01,
       'max_float': 0.8
   }
   ```

## Usage
Run the script:
```bash
python csfloatchecker.py
```
The script will fetch and display filtered listings in real-time.

## Example Output
```
Searching for listings...
★ Karambit | Price: 500.00$ | Float: 0.015 | Min Offer Price: 490.00$ | N/A | https://csfloat.com/item/987654321
```

## Key Features in Output
- **Colored highlights**: Knives (★) in purple, StatTrak items in orange.
- **Percentage difference**: Color-coded (green for < 0%, red for > 0%).

## Notes
- Listings are fetched using the CSFloat API.
- The script runs continuously and checks for new listings every 5-10 seconds.

## Dependencies
- Python 3.8+
- `requests` library
