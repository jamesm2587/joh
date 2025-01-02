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

# Function to fetch emoji
def get_emoji(item_name):
    for key in emoji_mapping:
        if key in item_name.lower():
            return emoji_mapping[key]
    return "🍽️"  # Default emoji

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

# Streamlit layout optimization
with st.container():
    # Organize inputs into two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # Store Selection
        store = st.selectbox("Store", list(store_data.keys()), key="store")

        # Item Input
        item_name = st.text_input("Item Name", key="item_name")

        # Price Format Selection (Radio buttons for per lb or per each)
        price_format = st.radio("Price Format", ("x lb", "x ea"), key="price_format")

    with col2:
        # Price Input
        price = None
        if price_format:
            price = st.text_input(f"Enter price {price_format}", key="price")

        # Date range selection using a single calendar
        st.write("Select Date Range")
        date_range = st.date_input(
            "Date Range",
            value=(datetime.today(), datetime.today() + timedelta(days=6)),
            key="date_range",
            min_value=datetime.today(),
            max_value=datetime.today() + timedelta(days=30),
            help="Select the start and end date for the offer."
        )

        start_date = date_range[0].strftime('%m/%d')
        end_date = date_range[1].strftime('%m/%d')

        # Sale type dropdown for specific stores
        sale_type = ""
        if store in ["Ted's Fresh", "IFM Market"]:
            sale_type = st.selectbox("Sale Type", ["3 Day Sale", "4 Day Sale"], key="sale_type")

    # Automatically determine if the price is in dollars or cents
    if price:
        try:
            price = float(price)
            if price.is_integer():
                price = f"{int(price)}¢"  # Use the cent symbol (¢) if it's an integer
            else:
                price = f"${price:.2f}"  # Format as dollars if it's a decimal
        except ValueError:
            price = "Invalid price entered"

    # Generate caption
    if st.button("Generate Caption"):
        store_info = store_data[store]
        emoji = get_emoji(item_name)

        # Ensure price format reflects correctly in the caption
        formatted_price = f"{price} {price_format}" if price else "Price not entered"

        caption = store_info["template"].format(
            emoji=emoji,
            item_name=item_name,
            price=formatted_price,
            date_range=f"{start_date} - {end_date}",
            location=store_info["location"] if store_info["location"] else "",
            hashtags=store_info["hashtags"],
            sale_type=sale_type if "{sale_type}" in store_info["template"] else "",
        )

        st.text_area("Generated Caption", value=caption, height=200)
