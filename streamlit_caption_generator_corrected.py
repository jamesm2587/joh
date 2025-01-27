import streamlit as st
from datetime import datetime, timedelta

# Custom CSS for gradients, shadows, and glass effects
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f3f4f7, #e4e7ed);
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: White;
        padding: 35px 30px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.20);
    }
    .stTextArea textarea {
        background: rgba(255, 255, 200, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .input-icon {
        width: 20px;
        height: 20px;
        vertical-align: middle;
        margin-right: 10px;
    }
    .stTextInput, .stSelectbox, .stRadio, .stDateInput {
        display: inline-block;
        width: calc(100% - 40px);
    }
    .input-wrapper {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
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
    "salmon": "🐟", "tilapia": "🐟", "milk": "🥛", "cheese": "🧀", "butter": "🧈",
    "egg": "🥚", "yogurt": "🥄", "bread": "🍞", "rice": "🍚", "pasta": "🍝",
    "pizza": "🍕", "burger": "🍔", "taco": "🌮", "burrito": "🌯", "sushi": "🍣",
    "dessert": "🍰", "cake": "🎂", "cookie": "🍪", "ice cream": "🍦", "chocolate": "🍫"
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

def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"

def format_price(price, price_format):
    try:
        price = float(price)
        return f"{int(price)}¢" if price.is_integer() else f"${price:.2f}"
    except ValueError:
        return "Invalid price entered"

def generate_caption(store, item_name, price, price_format, date_range, sale_type=""):
    store_info = store_data[store]
    return store_info["template"].format(
        emoji=get_emoji(item_name),
        item_name=item_name,
        price=f"{price} {price_format}" if price else "Price not entered",
        date_range=date_range,
        location=store_info["location"] or "",
        hashtags=store_info["hashtags"],
        sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
    )

st.title("Enhanced Caption Generator")

with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        store = st.selectbox("Store", list(store_data.keys()))
        item_name = st.text_input("Item Name")
        price_format = st.radio("Price Format", ("x lb", "x ea"))
        
    with col2:
        price = st.text_input(f"Enter price {price_format}")
        selected_dates = st.date_input(
            "Select Start and End Dates",
            [datetime.today(), datetime.today() + timedelta(days=6)]
        )
        
        date_range = (
            f"{selected_dates[0].strftime('%m/%d')} - {selected_dates[1].strftime('%m/%d')}"
            if len(selected_dates) == 2 
            else "Please select both dates"
        )
        
        sale_type = ""
        if store in ["Ted's Fresh", "IFM Market"]:
            sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"])

    if st.button("Generate Caption"):
        formatted_price = format_price(price, price_format)
        caption = generate_caption(store, item_name, formatted_price, price_format, date_range, sale_type)
        
        # Add copy functionality using native Streamlit features
        st.markdown(f"""
        <div style='position: relative;'>
            <textarea id="captionText" style='position: absolute; left: -9999px;'>{caption}</textarea>
            <button onclick="copyToClipboard()" style='background: #2575fc; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;'>
                📋 Copy to Clipboard
            </button>
        </div>
        <script>
            function copyToClipboard() {{
                const textarea = document.getElementById('captionText');
                textarea.select();
                document.execCommand('copy');
            }}
        </script>
        """, unsafe_allow_html=True)
        
        st.text_area("Generated Caption", value=caption, height=200)
