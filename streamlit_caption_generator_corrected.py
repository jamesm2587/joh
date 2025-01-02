import streamlit as st
from datetime import datetime, timedelta

# Expanded emoji mapping
emoji_mapping = {
    "apple": "🍎", "banana": "🍌", "grape": "🍇", "mango": "🥭", "watermelon": "🍉",
    "orange": "🍊", "pear": "🍐", "peach": "🍑", "strawberry": "🍓", "cherry": "🍒",
    "kiwi": "🥝", "pineapple": "🍍", "blueberry": "🫐", "avocado": "🥑",
    "carrot": "🥕", "broccoli": "🥦", "corn": "🌽", "lettuce": "🥬", "tomato": "🍅",
    "potato": "🥔", "onion": "🧅", "garlic": "🧄", "pepper": "🌶️", "cucumber": "🥒",
    "mushroom": "🍄", "beef": "🥩", "chicken": "🍗", "pork": "🐖", "turkey": "🦃",
    "lamb": "🐑", "fish": "🐟", "shrimp": "🍤", "crab": "🦀", "lobster": "🦞",
    "salmon": "🐟", "tilapia": "🐟", "milk": "🥛", "cheese": "🧀", "butter": "🧈",
    "egg": "🥚", "yogurt": "🥄", "bread": "🍞", "rice": "🍚", "pasta": "🍝",
    "pizza": "🍕", "burger": "🍔", "taco": "🌮", "burrito": "🌯", "sushi": "🍣",
    "dessert": "🍰", "cake": "🎂", "cookie": "🍪", "ice cream": "🍦", "chocolate": "🍫"
}

# Function to fetch emoji based on item name
def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"  # Default emoji

# Simple Language Detection (based on keywords)
def detect_language(text):
    spanish_keywords = ["el", "la", "de", "y", "es", "en", "para", "un", "una", "con"]
    english_keywords = ["the", "and", "is", "in", "for", "a", "with"]
    
    # Check for Spanish or English keywords
    if any(keyword in text.lower() for keyword in spanish_keywords):
        return "spanish"
    elif any(keyword in text.lower() for keyword in english_keywords):
        return "english"
    return "english"  # Default to English if no keywords match

# Store-specific data
store_data = {
    "Ted's Fresh": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    "IFM Market": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket",
    },
    "Fiesta Market": {
        "template": "{emoji} {item_name} {price}.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "9710 Main St. Lamont, Ca.",
        "hashtags": "#fiestamarket #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Viva": {
        "template": "{emoji} {item_name} {price}.\n⏰ Deal from {date_range}\n🌟 Only at Viva Supermarket\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#vivasupermarket #grocerydeals #groceryspecials #weeklysavings #weeklyspecials #grocery #abarrotes #carniceria #mariscos #seafood #produce #frutasyverduras #ahorros #ofertas",
    },
    "La Princesa Watsonville": {
        "template": "{emoji} {item_name} {price}.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "123 Main St. Watsonville, Ca.",
        "hashtags": "#laprincesa #watsonville #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Sam's Food": {
        "template": "{emoji} {item_name} {price}.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "456 Elm St. Fresno, Ca.",
        "hashtags": "#samsfood #fresno #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Puesto Market": {
        "template": "{emoji} {item_name} {price}.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "789 Oak St. Bakersfield, Ca.",
        "hashtags": "#puestomarket #bakersfield #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Rranch": {
        "template": "{emoji} {item_name} {price}.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "987 Pine St. Sacramento, Ca.",
        "hashtags": "#rranch #sacramento #grocerydeals #weeklyspecials #freshproduce #meats",
    }
}

# Streamlit App
st.title("Enhanced Caption Generator")

# Store Selection
store = st.selectbox("Select Store", list(store_data.keys()))

# Item Input
item_name = st.text_input("Item Name")

# Price Format Selection (Radio buttons for per lb or per each)
price_format = st.radio("Select Price Format", ("x lb", "x ea"))

# Price Input (activates after choosing price format)
price = None
if price_format:
    price = st.text_input(f"Enter price {price_format}")

# Date range picker
st.write("Select Date Range")
start_date = st.date_input("Start Date", datetime.today())
end_date = st.date_input("End Date", start_date + timedelta(days=6))
date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"

# Sale type dropdown for specific stores
sale_type = ""
if store in ["Ted's Fresh", "IFM Market"]:
    sale_type = st.selectbox("Select Sale Type", ["3 Day Sale", "4 Day Sale"])

# Generate caption
if st.button("Generate Caption"):
    store_info = store_data[store]
    emoji = get_emoji(item_name)
    
    # Detect language for emoji mapping
    language = detect_language(item_name)
    if language == "spanish":
        emoji = "🇲🇽"  # Adjust this based on Spanish preference if needed
    
    # Ensure price format reflects correctly in the caption
    formatted_price = f"${price} {price_format}" if price else "Price not entered"

    caption = store_info["template"].format(
        emoji=emoji,
        item_name=item_name,
        price=formatted_price,
        date_range=date_range,
        location=store_info["location"] if store_info["location"] else "",
        hashtags=store_info["hashtags"],
        sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
    )

    st.text_area("Generated Caption", value=caption, height=200)
