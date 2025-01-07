import streamlit as st
from datetime import datetime, timedelta

# Custom CSS for gradients, shadows, and glass effects
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #e6f0f9, #c3d9e3);
        font-family: 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
        color: #333;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .input-wrapper {
        display: flex;
        align-items: center;
        margin-bottom: 16px;
        position: relative;
    }
    .input-wrapper img {
        position: absolute;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
    }
    .stSelectbox, .stTextInput, .stRadio {
        padding-left: 35px; /* To make space for the icon */
        padding-right: 10px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 14px;
        width: 100%;
        background-color: #f9f9f9;
    }
    .stSelectbox select, .stTextInput input, .stRadio input {
        background-color: #f9f9f9;
    }
    .stSelectbox select:focus, .stTextInput input:focus, .stRadio input:focus {
        outline: none;
        border-color: #2575fc;
    }
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 10px;
        border: 1px solid #ccc;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 12px;
        font-size: 14px;
        font-family: 'Roboto', sans-serif;
    }
    .stTextArea textarea:focus {
        outline: none;
        border-color: #2575fc;
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
        # Item Name icon inside the input box
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/shopping-cart.png" class="input-icon" />', unsafe_allow_html=True)
        store = st.selectbox("Store", list(store_data.keys()), key="store")
        item_name = st.text_input("Item Name", key="item_name")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Price icon inside the input box
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/price-tag.png" class="input-icon" />', unsafe_allow_html=True)
        price_format = st.radio("Price Format", ("x lb", "x ea"), key="price_format")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # Price input field with icon inside the box
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/price-tag.png" class="input-icon" />', unsafe_allow_html=True)
        price = st.text_input(f"Enter price {price_format}", key="price")
        st.markdown('</div>', unsafe_allow_html=True)

        # Calendar icon inside the input box
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/calendar.png" class="input-icon" />', unsafe_allow_html=True)
        start_date = st.date_input("Start Date", datetime.today(), key="start_date")
        end_date = st.date_input("End Date", start_date + timedelta(days=6), key="end_date")
        date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
        st.markdown('</div>', unsafe_allow_html=True)

        # Sale Type icon inside the input box (optional)
        sale_type = ""
        if store in ["Ted's Fresh", "IFM Market"]:
            st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
            st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/tag.png" class="input-icon" />', unsafe_allow_html=True)
            sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"], key="sale_type")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
        # Ensure both dates are selected
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates
            date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
        else:
            start_date = end_date = datetime.today()
            date_range = "Please select both start and end dates."
        st.markdown('</div>', unsafe_allow_html=True)

        # Sale Type icon (if necessary)
        sale_type = ""
        if store in ["Ted's Fresh", "IFM Market"]:
            st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
            st.markdown('<img src="https://img.icons8.com/ios-filled/50/808080/discount--v1.png" class="input-icon" />', unsafe_allow_html=True)
            sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"], key="sale_type")
            st.markdown('</div>', unsafe_allow_html=True)

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
