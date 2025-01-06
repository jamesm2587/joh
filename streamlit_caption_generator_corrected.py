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
    .input-icon {
        width: 20px;
        height: 20px;
        vertical-align: middle;
        margin-right: 10px;
    }
    .stTextInput, .stSelectbox, .stRadio, .stDateInput {
        display: inline-block;
        width: calc(100% - 40px); /* Adjust width to make space for icons */
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
    "apple": "\ud83c\udf4e", "banana": "\ud83c\udf4c", "grape": "\ud83c\udf47", "mango": "\ud83e\udd6d", "watermelon": "\ud83c\udf49",
    "orange": "\ud83c\udf4a", "pear": "\ud83c\udf50", "peach": "\ud83c\udf51", "strawberry": "\ud83c\udf53", "cherry": "\ud83c\udf52",
    "kiwi": "\ud83e\udd5d", "pineapple": "\ud83c\udf4d", "blueberry": "\ud83e\udd67", "avocado": "\ud83e\udd51",
    "carrot": "\ud83e\udd55", "broccoli": "\ud83e\udd66", "corn": "\ud83c\udf3d", "lettuce": "\ud83e\udd6c", "tomato": "\ud83c\udf45",
    "potato": "\ud83e\udd54", "onion": "\ud83e\udd52", "garlic": "\ud83e\udd51", "pepper": "\ud83c\udf36\ufe0f", "cucumber": "\ud83e\udd52",
    "mushroom": "\ud83c\udf44", "beef": "\ud83e\uddc9", "chicken": "\ud83c\udf57", "pork": "\ud83d\udc17", "turkey": "\ud83e\udd83",
    "lamb": "\ud83d\udc11", "fish": "\ud83d\udc1f", "shrimp": "\ud83c\udf64", "crab": "\ud83e\udd80", "lobster": "\ud83e\udd9e",
    "salmon": "\ud83d\udc1f", "tilapia": "\ud83d\udc1f", "milk": "\ud83e\udd5b", "cheese": "\ud83e\uddc0", "butter": "\ud83e\uddc1",
    "egg": "\ud83e\udd5a", "yogurt": "\ud83c\udf7d", "bread": "\ud83c\udf5e", "rice": "\ud83c\udf5a", "pasta": "\ud83c\udf5d",
    "pizza": "\ud83c\udf55", "burger": "\ud83c\udf54", "taco": "\ud83c\udf2e", "burrito": "\ud83c\udf2f", "sushi": "\ud83c\udf63",
    "dessert": "\ud83c\udf70", "cake": "\ud83c\udf82", "cookie": "\ud83c\udf6a", "ice cream": "\ud83c\udf66", "chocolate": "\ud83c\udf6b"
}

# Function to fetch emoji
def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "\ud83c\udf72"

# Store-specific data
store_data = {
    "Ted's Fresh": {
        "template": "{sale_type} \u23f0\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    "IFM Market": {
        "template": "{sale_type} \u23f0\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket",
    },
    "Fiesta Market": {
        "template": "{emoji} {item_name} {price}.\n\u23f0 {date_range}\n\u27a1\ufe0f {location}\n.\n.\n{hashtags}",
        "location": "9710 Main St. Lamont, Ca.",
        "hashtags": "#fiestamarket #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Viva": {
        "template": "{emoji} {item_name} {price}.\n\u23f0 Deal from {date_range}\n\ud83c\udf1f Only at Viva Supermarket\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#vivasupermarket #grocerydeals #groceryspecials #weeklysavings #weeklyspecials #grocery #abarrotes #carniceria #mariscos #seafood #produce #frutasyverduras #ahorros #ofertas",
    },
    "La Princesa Watsonville": {
        "template": "{emoji} {item_name} {price}.\n\u23f0 {date_range}\n\u27a1\ufe0f {location}\n.\n.\n{hashtags}",
        "location": "123 Main St. Watsonville, Ca.",
        "hashtags": "#laprincesa #watsonville #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Sam's Food": {
        "template": "{emoji} {item_name} {price}.\n\u23f0 {date_range}\n\u27a1\ufe0f {location}\n.\n.\n{hashtags}",
        "location": "456 Elm St. Fresno, Ca.",
        "hashtags": "#samsfood #fresno #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Puesto Market": {
        "template": "{emoji} {item_name} {price}.\n\u23f0 {date_range}\n\u27a1\ufe0f {location}\n.\n.\n{hashtags}",
        "location": "789 Oak St. Bakersfield, Ca.",
        "hashtags": "#puestomarket #bakersfield #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Rranch": {
        "template": "{emoji} {item_name} {price}.\n\u23f0 {date_range}\n\u27a1\ufe0f {location}\n.\n.\n{hashtags}",
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
        # Item Name icon
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/shopping-cart.png" class="input-icon" />', unsafe_allow_html=True)
        store = st.selectbox("Store", list(store_data.keys()), key="store")
        item_name = st.text_input("Item Name", key="item_name")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Price icon
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/price-tag.png" class="input-icon" />', unsafe_allow_html=True)
        price_format = st.radio("Price Format", ("x lb", "x ea"), key="price_format")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Price input field
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/price-tag.png" class="input-icon" />', unsafe_allow_html=True)
        price = st.text_input(f"Enter price {price_format}", key="price")
        st.markdown('</div>', unsafe_allow_html=True)

        # Calendar icons for dates
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/calendar.png" class="input-icon" />', unsafe_allow_html=True)
        start_date = st.date_input("Start Date", datetime.today(), key="start_date")
        end_date = st.date_input("End Date", start_date + timedelta(days=6), key="end_date")
        date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
        st.markdown('</div>', unsafe_allow_html=True)

        # Sale Type icon (if necessary)
        sale_type = ""
        if store in ["Ted's Fresh", "IFM Market"]:
            st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
            st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/tag.png" class="input-icon" />', unsafe_allow_html=True)
            sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"], key="sale_type")
            st.markdown('</div>', unsafe_allow_html=True)

    # Format price
    if price:
        try:
            price = float(price)
            if price.is_integer():
                price = f"{int(price)}\u00a2"
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
