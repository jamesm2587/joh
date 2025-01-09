import streamlit as st
from datetime import datetime, timedelta

# Custom CSS for enhanced visuals
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #eef2f3, #8e9eab);
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff7eb3, #ff758c);
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, background 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #ff5e95, #ff456e);
    }
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 10px;
        color: #333;
    }
    .input-wrapper {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .input-icon {
        width: 24px;
        height: 24px;
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Expanded emoji mapping
emoji_mapping = {
    "apple": "🍎", "banana": "🍌", "grape": "🍇", "mango": "🥭", "watermelon": "🍉",
    "orange": "🍊", "pear": "🍐", "peach": "🍑", "strawberry": "🍓", "cherry": "🍒",
    "kiwi": "🥝", "pineapple": "🍍", "blueberry": "🫐", "avocado": "🥑",
    "carrot": "🥕", "broccoli": "🥦", "corn": "🌽", "lettuce": "🥬", "tomato": "🍅",
    "potato": "🥔", "onion": "🧅", "garlic": "🧄", "pepper": "🌶️", "cucumber": "🥒",
    "mushroom": "🍄", "beef": "🥩", "chicken": "🍗", "pork": "🐖", "turkey": "🦃",
    "lamb": "🐑", "fish": "🐟", "shrimp": "🍤", "crab": "🦀", "lobster": "🦞",
    "salmon": "🐟", "milk": "🥛", "cheese": "🧀", "butter": "🧈", "egg": "🥚",
    "yogurt": "🥄", "bread": "🍞", "rice": "🍚", "pasta": "🍝", "pizza": "🍕",
    "burger": "🍔", "taco": "🌮", "burrito": "🌯", "sushi": "🍣", "dessert": "🍰",
    "cake": "🎂", "cookie": "🍪", "ice cream": "🍦", "chocolate": "🍫"
}

# Function to fetch emoji
def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"

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
        "template": "{emoji} {item_name} {price}.\n⏰ Hasta {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "1260 Main St. ↔️ 1424 Freedom Blvd.",
        "hashtags": "#laprincesawatsonville #ahorrosdelasemana #ahorrosdeabarrotes #freshproduce #freshmeats #carniceria #frutasyverduras",
    },
    "Mi Rancho": {
        "template": "{emoji} {item_name} {price}.\n⏰ {date_range}\n📍 {location}\n.\n.\n{hashtags}",
        "location": "400 W. Perkins, McFarland, California",
        "hashtags": "#miranchomarketmcfarland #miranchomarket #mcfarlandca #mcfarland #ahorrosdelasemana #ahorrosdeabarrotes #freshproduce #freshmeats #carniceria #frutasyverduras",
    },
    "Mi Tiendita": {
        "template": "{emoji} {item_name} {price}.\n⏰ Ahorros {date_range}\n📍 {location}\n.\n.\n{hashtags}",
        "location": "3145 Payne Ave. San Jose, CA 95117",
        "hashtags": "#OfertasDeLaSemana #MiTiendita #Ahorra #Sabor #Carne #Verduras #ahorros #grocerydeal #weeklysavings #weeklydeals",
    },
    "Sam's Food": {
        "template": "{emoji} {item_name} {price}.\n⏰ Pricing {date_range}\n📍 {location}\n.\n.\n{hashtags}",
        "location": "1805 Dairy Ave. Corcoran, CA.",
        "hashtags": "#samsfood #corcoranca #grocerydeals #weeklyspecials #freshproduce #meats",
    },
}

# Streamlit app content
st.title("Enhanced Caption Generator")

# Layout
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/store.png" class="input-icon" />', unsafe_allow_html=True)
    store = st.selectbox("Store", list(store_data.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/product.png" class="input-icon" />', unsafe_allow_html=True)
    item_name = st.text_input("Item Name")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/price-tag.png" class="input-icon" />', unsafe_allow_html=True)
    price = st.text_input("Price")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    selected_dates = st.date_input(
        "Select Start and End Dates",
        [datetime.today(), datetime.today() + timedelta(days=6)],
    )
    if len(selected_dates) == 2:
        date_range = f"{selected_dates[0].strftime('%m/%d')} - {selected_dates[1].strftime('%m/%d')}"
    else:
        date_range = "Select both dates"

    sale_type = ""
    if store in ["Ted's Fresh", "IFM Market"]:
        sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"])

# Generate caption
if st.button("Generate Caption"):
    store_info = store_data[store]
    emoji = get_emoji(item_name)
    formatted_price = f"${price}" if price else "Price not entered"
    caption = store_info["template"].format(
        emoji=emoji,
        item_name=item_name,
        price=formatted_price,
        date_range=date_range,
        location=store_info["location"],
        hashtags=store_info["hashtags"],
        sale_type=sale_type,
    )
    st.text_area("Generated Caption", value=caption, height=200)
