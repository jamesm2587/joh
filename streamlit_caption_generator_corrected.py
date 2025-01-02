import streamlit as st
from datetime import datetime, timedelta

# Custom CSS for gradients, shadows, and glass effects
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f3f4f7, #e4e7ed);
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .container {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }
    .input-icon {
        width: 20px;
        height: 20px;
        vertical-align: middle;
        margin-right: 10px;
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

# Streamlit layout with styled container
with st.container():
    st.markdown("<div class='container'>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://img.icons8.com/ios-filled/50/808080/shopping-cart.png", width=20, use_container_width=False)  # Item Name icon
        store = st.selectbox("Store", list(store_data.keys()), key="store")
        item_name = st.text_input("Item Name", key="item_name")
        
        st.image("https://img.icons8.com/ios-filled/50/808080/price-tag.png", width=20, use_container_width=False)  # Price icon
        price_format = st.radio("Price Format", ("x lb", "x ea"), key="price_format")
    with col2:
        price = st.text_input(f"Enter price {price_format}", key="price")
        
        st.image("https://img.icons8.com/ios-filled/50/808080/calendar.png", width=20, use_container_width=False)  # Calendar icon
        start_date = st.date_input("Start Date", datetime.today(), key="start_date")
        end_date = st.date_input("End Date", start_date + timedelta(days=6), key="end_date")
        date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
        
        sale_type = ""
        if store in ["Ted's Fresh", "IFM Market"]:
            st.image("https://img.icons8.com/ios-filled/50/808080/tag.png", width=20, use_container_width=False)  # Sale Type icon
            sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"], key="sale_type")

    # Format price
    if price:
        try:
            price = float(price)
            if price.is_integer():
                price = f"{int(price)}¢"
            else:
                price = f"${price:.2f}"
        except ValueError:
            price = "Invalid price entered"

    # Generate caption
    if st.button("Generate Caption"):
        store_info = store_data[store]
        emoji = get_emoji(item_name)
        formatted_price = f"{price} {price_format}" if price else "Price not entered"
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

    st.markdown("</div>", unsafe_allow_html=True)
