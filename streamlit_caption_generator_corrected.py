import streamlit as st

# Store-specific data with updated captions
store_data = {
    "Ted's Fresh": {
        "template": "3 DAYS ONLY ⏰\n{emoji} {item_name} {price} x lb.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    "IFM Market": {
        "template": "🌟 {sale_type} ⏰ {date_range}\n{emoji} {item_name} {price} x lb.\n.\n.\n{hashtags}",
        "location": "234 IFM Rd, Naperville, Illinois",
        "hashtags": "#IFMMarket #Naperville #FreshProduce #FreshMeats #Market",
    },
    "Mi Tiendita": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n{location}\n.\n.\n{hashtags}",
        "location": "890 Mi Tiendita Ln, Houston, Texas",
        "hashtags": "#MiTiendita #Houston #FreshProduce #Carniceria #FreshMeats",
    },
    "Sam's Food": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n{location}\n.\n.\n{hashtags}",
        "location": "123 Sam's Food St, Miami, Florida",
        "hashtags": "#SamsFood #Miami #FreshProduce #Carniceria #FreshMeats",
    },
    "Viva": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ Deal until {date_range}\n🌟 Only at Viva Supermarket\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#vivasupermarket #grocerydeals #groceryspecials #weeklysavings #weeklyspecials #grocery #abarrotes #carniceria #mariscos #seafood #produce #frutasyverduras #ahorros #ofertas",
    },
    "La Princesa Watsonville": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n{location}\n.\n.\n{hashtags}",
        "location": "789 La Princesa, Watsonville, California",
        "hashtags": "#LaPrincesaWatsonville #Watsonville #FreshProduce #FreshMeats #Carniceria",
    },
    "Rranch": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n{location}\n.\n.\n{hashtags}",
        "location": "101 Rranch Blvd, Los Angeles, California",
        "hashtags": "#Rranch #LosAngeles #FreshProduce #FreshMeats #Carniceria",
    },
    "Puesto Market": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n{location}\n.\n.\n{hashtags}",
        "location": "202 Puesto Rd, San Diego, California",
        "hashtags": "#PuestoMarket #SanDiego #FreshProduce #FreshMeats #Carniceria",
    },
    "Fiesta Market": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "9710 Main St. Lamont, Ca.",
        "hashtags": "#FiestaMarket #Lamont #FreshProduce #Carniceria #FreshMeats",
    },
}

# Function to get emoji based on item name
def get_emoji(item_name):
    # Define categories with keywords and corresponding emojis
    emoji_map = {
        "fish": ["tilapia", "salmon", "tuna", "cod", "trout"],
        "meat": ["beef", "chicken", "pork", "lamb", "steak"],
        "fruit": ["apple", "pear", "orange", "banana", "grape", "watermelon"],
        "vegetable": ["carrot", "potato", "onion", "broccoli", "spinach"],
        "seafood": ["shrimp", "lobster", "crab", "scallops"],
    }

    # Check for matching category keywords in item name
    for category, keywords in emoji_map.items():
        for keyword in keywords:
            if keyword.lower() in item_name.lower():
                # Return appropriate emoji based on category
                if category == "fish":
                    return "🐟"  # Fish emoji
                elif category == "meat":
                    return "🥩"  # Meat emoji
                elif category == "fruit":
                    return "🍎"  # Apple emoji (can be generalized for fruits)
                elif category == "vegetable":
                    return "🥕"  # Carrot emoji
                elif category == "seafood":
                    return "🦀"  # Crab emoji (generalized for seafood)
    return "🍽️"  # Default emoji if no match

# Streamlit App
st.title("Caption Generator for Social Media")
store = st.selectbox("Select Store", list(store_data.keys()))
item_name = st.text_input("Item Name")
price = st.text_input("Price")
date_range = st.text_input("Date Range")
sale_type = st.text_input("Sale Type (if applicable)")

if st.button("Generate Caption"):
    store_info = store_data[store]
    emoji = get_emoji(item_name)
    
    # Adjusting the format to match the example with line breaks between sections
    caption = store_info["template"].format(
        emoji=emoji,
        item_name=item_name,
        price=price,
        date_range=date_range,
        location=store_info["location"] if store_info["location"] else "",
        hashtags=store_info["hashtags"],
        sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
    )
    
    # Display the caption with proper line breaks
    st.text_area("Generated Caption", value=caption, height=200)