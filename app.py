import json
import requests
import os
import time
import argparse

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def fetch_price(item_id):
    url = f"https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}"
    headers = {'User-Agent': 'profit tracking by recipe'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching data for item ID {item_id}. Status code: {response.status_code}")
        return None
    
    data = response.json()
    return data['data'][str(item_id)]

def load_and_validate_recipes(directory):
    recipes = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            recipe_path = os.path.join(directory, filename)
            try:
                recipe = load_json(recipe_path)
                
                # Validate required keys
                required_keys = ['input-item-id', 'output-item-id', 'output-per-input', 'processed-per-hour']
                if all(key in recipe for key in required_keys):
                    recipe_name = filename[:-5]  # Remove the .json extension for naming
                    recipes[recipe_name] = recipe
                else:
                    print(f"Warning: Recipe '{filename}' is missing required keys.")
            except json.JSONDecodeError:
                print(f"Error reading JSON file: '{filename}'")
    return recipes

def calculate_profit(recipe, config):
    input_id = recipe['input-item-id']
    output_id = recipe['output-item-id']
    output_per_input = recipe['output-per-input']
    processed_per_hour = recipe['processed-per-hour']

    input_price_data = fetch_price(input_id)
    output_price_data = fetch_price(output_id)

    taxed_multiplier = 1 - config['tax-rate']

    if input_price_data is None or output_price_data is None:
        return None

    input_price = input_price_data['low']
    effective_output_price = output_price_data['high'] * output_per_input * taxed_multiplier

    profit_per_input = effective_output_price - input_price
    profit_per_hour = profit_per_input * processed_per_hour

    return profit_per_hour

def main():
    # Load and validate all recipes
    recipes = load_and_validate_recipes('recipes/')
    config = load_json('config.json')

    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Profit Tracker for OSRS Recipes')
    recipe_options = list(recipes.keys())
    
    parser.add_argument('--recipe', type=str, choices=recipe_options, default=config['default-recipe'],
                        help='Specify the recipe to track')
    parser.add_argument('--interval', type=int, help='Set the polling interval in seconds')
    args = parser.parse_args()

    polling_interval = args.interval if args.interval else config['polling-interval']

    while True:
        recipe = recipes.get(args.recipe)
        
        if recipe:
            profit = calculate_profit(recipe, config)
            if profit is not None:
                print(f"Estimated profit per hour for {args.recipe}: {profit:.2f} coins per hour.")
            else:
                print(f"Failed to calculate profit for {args.recipe}.")
        else:
            print(f"Recipe '{args.recipe}' not found.")

        time.sleep(polling_interval)

if __name__ == "__main__":
    main()
