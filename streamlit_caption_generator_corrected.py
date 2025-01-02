import streamlit as st
from datetime import datetime, timedelta
import re
from langdetect import detect

# Expanded emoji mapping for both English and Spanish
emoji_mapping = {
    # Fruits
    "apple": "🍎", "manzana": "🍎", "red apple": "🍎", "green apple": "🍏", 
    "banana": "🍌", "plátano": "🍌", "mango": "🥭", "mangoes": "🥭", 
    "watermelon": "🍉", "sandía": "🍉", "orange": "🍊", "naranja": "🍊", 
    "pear": "🍐", "pera": "🍐", "peach": "🍑", "durazno": "🍑", 
    "strawberry": "🍓", "fresa": "🍓", "cherry": "🍒", "cereza": "🍒", 
    "kiwi": "🥝", "kiwis": "🥝", "pineapple": "🍍", "piña": "🍍", 
    "blueberry": "🫐", "arándano": "🫐", "avocado": "🥑", "aguacate": "🥑", 

    # Vegetables
    "carrot": "🥕", "zanahoria": "🥕", "broccoli": "🥦", "brócoli": "🥦", 
    "corn": "🌽", "maíz": "🌽", "lettuce": "🥬", "lechuga": "🥬", 
    "tomato": "🍅", "jitomate": "🍅", "potato": "🥔", "papa": "🥔", 
    "onion": "🧅", "cebolla": "🧅", "garlic": "🧄", "ajo": "🧄", 

    # Meats
    "beef": "🥩", "carne de res": "🥩", "chicken": "🍗", "pollo": "🍗", 
    "pork": "🐖", "cerdo": "🐖", "turkey": "🦃", "pavo": "🦃", 
    "lamb": "🐑", "cordero": "🐑", "fish": "🐟", "pescado": "🐟", 
    "shrimp": "🍤", "camarón": "🍤", "crab": "🦀", "cangrejo": "🦀", 
    "lobster": "🦞", "langosta": "🦞", "salmon": "🐟", "salmón": "🐟", 
    "tilapia": "🐟", "tilapia": "🐟", 

    # Dairy
    "milk": "🥛", "leche": "🥛", "cheese": "🧀", "queso": "🧀", 
    "butter": "🧈", "mantequilla": "🧈", "egg": "🥚", "huevo": "🥚", 
    "yogurt": "🥄", "yogur": "🥄", 

    # Bakery
    "bread": "🍞", "pan": "🍞", "rice": "🍚", "arroz": "🍚", 
    "pasta": "🍝", "espaguetis": "🍝", "pizza": "🍕", "pizza": "🍕", 
    "burger": "🍔", "hamburguesa": "🍔", "taco": "🌮", "burrito": "🌯", 
    "sushi": "🍣", "sushi": "🍣", 

    # Sweets
    "dessert": "🍰", "pastel": "🍰", "cake": "🎂", "torta": "🎂", 
    "cookie": "🍪", "galleta": "🍪", "ice cream": "🍦", "helado": "🍦", 
    "chocolate": "🍫", "chocolate": "🍫",
}

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

# Detect language (English or Spanish)
def detect_language(text):
    try:
        return detect(text)  # Detects the language
    except:
        return "en"  # Default to English if detection fails

# Function to fetch emoji with language detection and regex matching
def get_emoji(item_name):
    language = detect_language(item_name)  # Detect language ('en' or 'es')
    item_name = item_name.lower()

    if language == "es":
        # Match against Spanish terms in the emoji_mapping
        for key in emoji_mapping:
            if re.search(r'\b' + re.escape(key) + r'\b', item_name):  # Word boundary for exact match
                return emoji_mapping[key]
    else:
        # Match against English terms
        for key in emoji_mapping:
            if re.search(r'\b' + re.escape(key) + r'\b', item_name):  # Word boundary for exact match
                return emoji_mapping[key]
    
    return "🍽️"  # Default emoji

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
    emoji = get_emoji(item_name)  # Get emoji based on item name

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
