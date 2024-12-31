
import streamlit as st

# Store-specific data
store_data = {
    "Mi Rancho": {
        "template": "{emoji} {item_name} {price} x lb.\n⏰ {date_range}\n{location}\n.\n.\n{hashtags}",
        "location": "400 W. Perkins, McFarland, California",
        "hashtags": "#miranchomarketmcfarland #miranchomarket #mcfarlandca #mcfarland #ahorrosdelasemana #ahorrosdeabarrotes #freshproduce #freshmeats #carniceria #frutasyverduras",
    },
    "International Fresh Market": {
        "template": "🌟 {sale_type} ⏰ {date_range}\n{emoji} {item_name} {price} x lb.\n.\n.\n{hashtags}",
        "location": "1234 Fresh Ave, Naperville, Illinois",
        "hashtags": "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket",
    },
}

# Function to get emoji based on item name
def get_emoji(item_name):
    emoji_map = {"pear": "🍐", "orange": "🍊", "fish": "🐟", "beef": "🥩"}
    for keyword, emoji in emoji_map.items():
        if keyword.lower() in item_name.lower():
            return emoji
    return "🍽️"

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
    caption = store_info["template"].format(
        emoji=emoji,
        item_name=item_name,
        price=price,
        date_range=date_range,
        location=store_info["location"],
        hashtags=store_info["hashtags"],
        sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
    )
    st.text_area("Generated Caption", value=caption, height=150)
