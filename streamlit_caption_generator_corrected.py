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
def get_suggested_emoji(item_name):
    item_name_lower = item_name.lower()
    for key, emoji in emoji_mapping.items():
        if key in item_name_lower:
            return emoji
    return "🍽️"  # Default emoji

# Store-specific data
store_data = {
    "Ted's Fresh": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    "International Fresh Market": {
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

# Streamlit App Layout
st.set_page_config(page_title="Enhanced Caption Generator", layout="wide")

# Title and columns for square layout
st.title("Enhanced Caption Generator")
col1, col2, col3 = st.columns([1, 1, 1])

# Store selection
with col1:
    store = st.selectbox("Select Store", list(store_data.keys()))

# Item Input and Suggested Emoji
with col2:
    item_name = st.text_input("Item Name")
    suggested_emoji = get_suggested_emoji(item_name)
    st.write(f"Suggested Emoji: {suggested_emoji}")

# Manual Emoji Override
with col3:
    manual_emoji = st.text_input("Choose an Emoji Manually", value=suggested_emoji)

# Price Format and Input
with col1:
    price_format = st.radio("Price Format", ["x lb", "x ea"])
    price = st.text_input("Enter Price", value="") if price_format else ""

# Date Range Picker
with col2:
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.today(), datetime.today() + timedelta(days=6))
    )

    if isinstance(date_range, tuple):
        start_date, end_date = date_range
        formatted_date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"

# Sale Type
with col3:
    sale_type = st.selectbox(
        "Sale Type" if store in ["Ted's Fresh", "International Fresh Market"] else "N/A",
        options=["3 Day Sale", "4 Day Sale"] if store in ["Ted's Fresh", "International Fresh Market"] else []
    )

# Caption Generator
if st.button("Generate Caption"):
    store_info = store_data[store]
    emoji_used = manual_emoji or suggested_emoji
    formatted_price = f"${price} {price_format}" if price else "Price not entered"

    caption = store_info["template"].format(
        emoji=emoji_used,
        item_name=item_name,
        price=formatted_price,
        date_range=formatted_date_range,
        location=store_info["location"],
        hashtags=store_info["hashtags"],
        sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
    )

    st.text_area("Generated Caption", value=caption, height=200)
