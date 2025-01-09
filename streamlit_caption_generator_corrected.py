import streamlit as st
from datetime import datetime, timedelta

# Custom CSS for a clean design
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .calculator-button {
        background: #f0f0f0;
        border: none;
        border-radius: 4px;
        padding: 10px 15px;
        margin: 5px;
        font-size: 18px;
        cursor: pointer;
    }
    .calculator-button:hover {
        background: #e0e0e0;
    }
    .calculator-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Store-specific data
store_data = {
    "Ted's Fresh": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    # Add other stores here...
}

# Function to fetch emoji
emoji_mapping = {"apple": "🍎", "banana": "🍌", "grape": "🍇"}
def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"

# Streamlit App
st.title("Caption Generator")

store = st.selectbox("Store", list(store_data.keys()))
item_name = st.text_input("Item Name")
price_format = st.radio("Price Format", ["x lb", "x ea"])
price = st.text_input(f"Enter price {price_format}")

# Calculator-style buttons for predefined prices
st.write("**Select a Price:**")
predefined_prices = [0.99, 1.49, 2.99, 3.99, 5.49, 7.99, 10.99]
selected_price = st.session_state.get("selected_price", "")

with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    for p in predefined_prices:
        if st.button(f"${p:.2f}", key=f"price_{p}"):
            st.session_state["selected_price"] = f"${p:.2f}"
            price = f"${p:.2f}"
    st.markdown('</div>', unsafe_allow_html=True)

# Date input
date_range = st.date_input(
    "Select Date Range", [datetime.today(), datetime.today() + timedelta(days=6)]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    formatted_date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"
else:
    formatted_date_range = "Please select both dates."

sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"]) if store in ["Ted's Fresh"] else ""

if st.button("Generate Caption"):
    store_info = store_data[store]
    emoji = get_emoji(item_name)
    caption = store_info["template"].format(
        emoji=emoji,
        item_name=item_name,
        price=price,
        date_range=formatted_date_range,
        location=store_info.get("location", ""),
        hashtags=store_info["hashtags"],
        sale_type=sale_type,
    )
    st.text_area("Generated Caption", value=caption, height=200)
