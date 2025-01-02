import streamlit as st
from datetime import datetime, timedelta

# Expanded emoji mapping
emoji_mapping = {
    # Fruits
    "apple": "🍎",
    "banana": "🍌",
    "grape": "🍇",
    "mango": "🥭",
    "watermelon": "🍉",
    "orange": "🍊",
    "pear": "🍐",
    "peach": "🍑",
    "strawberry": "🍓",
    "cherry": "🍒",
    "kiwi": "🥝",
    "pineapple": "🍍",
    "blueberry": "🫐",
    "avocado": "🥑",
    # Vegetables
    "carrot": "🥕",
    "broccoli": "🥦",
    "corn": "🌽",
    "lettuce": "🥬",
    "tomato": "🍅",
    "potato": "🥔",
    "onion": "🧅",
    "garlic": "🧄",
    "pepper": "🌶️",
    "cucumber": "🥒",
    "mushroom": "🍄",
    # Meats
    "beef": "🥩",
    "chicken": "🍗",
    "pork": "🐖",
    "turkey": "🦃",
    "lamb": "🐑",
    # Seafood
    "fish": "🐟",
    "shrimp": "🍤",
    "crab": "🦀",
    "lobster": "🦞",
    "salmon": "🐟",
    "tilapia": "🐟",
    # Dairy
    "milk": "🥛",
    "cheese": "🧀",
    "butter": "🧈",
    "egg": "🥚",
    "yogurt": "🥄",
    # Miscellaneous
    "bread": "🍞",
    "rice": "🍚",
    "pasta": "🍝",
    "pizza": "🍕",
    "burger": "🍔",
    "taco": "🌮",
    "burrito": "🌯",
    "sushi": "🍣",
    "dessert": "🍰",
    "cake": "🎂",
    "cookie": "🍪",
    "ice cream": "🍦",
    "chocolate": "🍫",
}

# Function to fetch emoji
def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"  # Default emoji

# Store-specific data
store_data = {
    "Ted's Fresh": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price} x lb.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    "IFM Market": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price} x lb.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket",
    },
    "Fiesta Market": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "9710 Main St. Lamont, Ca.",
        "hashtags": "#fiestamarket #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Viva": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ Deal from {date_range}\n🌟 Only at Viva Supermarket\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#vivasupermarket #grocerydeals #groceryspecials #weeklysavings #weeklyspecials #grocery #abarrotes #carniceria #mariscos #seafood #produce #frutasyverduras #ahorros #ofertas",
    },
    "La Princesa Watsonville": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "123 Main St. Watsonville, Ca.",
        "hashtags": "#laprincesa #watsonville #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Sam's Food": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location"
