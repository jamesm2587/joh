import streamlit as st
from datetime import datetime, timedelta

# Import configurations
from config import emoji_mapping, store_data

def create_input_with_icon(icon_url, label, input_type, **kwargs):
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown(f'<img src="{icon_url}" class="input-icon" />', unsafe_allow_html=True)
    input_map = {
        "text_input": st.text_input,
        "date_input": st.date_input,
        "selectbox": st.selectbox,
        "radio": st.radio,
    }
    value = input_map[input_type](label, **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)
    return value

def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"

# Streamlit App
st.title("Enhanced Caption Generator")
st.markdown("<div class='container'>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    store = create_input_with_icon(
        "https://img.icons8.com/ios-filled/50/808080/shopping-cart.png",
        "Store",
        "selectbox",
        options=list(store_data.keys()),
        key="store"
    )
    item_name = create_input_with_icon(
        "https://img.icons8.com/ios-filled/50/808080/shopping-cart.png",
        "Item Name",
        "text_input",
        key="item_name"
    )
    price_format = create_input_with_icon(
        "https://img.icons8.com/ios-filled/50/808080/price-tag.png",
        "Price Format",
        "radio",
        options=["x lb", "x ea"],
        key="price_format"
    )

with col2:
    price = create_input_with_icon(
        "https://img.icons8.com/ios-filled/50/808080/price-tag.png",
        f"Enter price {price_format}",
        "text_input",
        key="price"
    )
    start_date = create_input_with_icon(
        "https://img.icons8.com/ios-filled/50/808080/calendar.png",
        "Start Date",
        "date_input",
        value=datetime.today(),
        key="start_date"
    )
    end_date = create_input_with_icon(
        "https://img.icons8.com/ios-filled/50/808080/calendar.png",
        "End Date",
        "date_input",
        value=start_date + timedelta(days=6),
        key="end_date"
    )
    date_range = f"{start_date.strftime('%m/%d')} - {end_date.strftime('%m/%d')}"

    sale_type = ""
    if store in ["Ted's Fresh", "IFM Market"]:
        sale_type = create_input_with_icon(
            "https://img.icons8.com/ios-filled/50/808080/tag.png",
            "Sale Type",
            "selectbox",
            options=["3 Day Sale", "4 Day Sale"],
            key="sale_type"
        )

# Price formatting
try:
    price = f"${float(price):.2f}" if price else "Invalid price entered"
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
        location=store_info["location"] or "",
        hashtags=store_info["hashtags"],
        sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
    )
    st.text_area("Generated Caption", value=caption, height=200)

st.markdown("</div>", unsafe_allow_html=True)
