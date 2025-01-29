import streamlit as st
from datetime import datetime, timedelta

# Advanced CSS with animations and modern design
st.markdown("""
<style>
:root {
    --primary: #2563eb;
    --secondary: #7c3aed;
    --glass: rgba(255, 255, 255, 0.9);
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

body {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    font-family: 'Inter', sans-serif;
}

.stApp {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white !important;
    padding: 1rem 2rem;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.preview-card {
    background: var(--glass);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.emoji-preview {
    font-size: 2.5rem;
    animation: float 3s ease-in-out infinite;
}

.input-error {
    color: #dc2626;
    font-size: 0.875rem;
    margin-top: 0.25rem;
    display: none;
}

.input-error.show {
    display: block;
}

.price-badge {
    background: var(--primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Extended emoji mapping
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

# Complete store data
store_data = {
    "Ted's Fresh": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price}\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
    },
    "IFM Market": {
        "template": "{sale_type} ⏰\n{emoji} {item_name} {price}\nOnly {date_range}\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket",
    },
    "Fiesta Market": {
        "template": "{emoji} {item_name} {price}\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "9710 Main St. Lamont, Ca.",
        "hashtags": "#fiestamarket #grocerydeals #weeklyspecials #freshproduce #meats",
    },
    "Viva": {
        "template": "{emoji} {item_name} {price}\n⏰ Deal from {date_range}\n🌟 Only at Viva Supermarket\n.\n.\n{hashtags}",
        "location": "",
        "hashtags": "#vivasupermarket #grocerydeals #groceryspecials #weeklysavings #weeklyspecials #grocery #abarrotes #carniceria #mariscos #seafood #produce #frutasyverduras #ahorros #ofertas",
    },
    "La Princesa Watsonville": {
        "template": "{emoji} {item_name} {price}\n⏰ Hasta {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
        "location": "1260 Main St. ↔️ 1424 Freedom Blvd.",
        "hashtags": "#laprincesawatsonville #ahorrosdelasemana #ahorrosdeabarrotes #freshproduce #freshmeats #carniceria #frutasyverduras",
    },
    "Mi Rancho": {
        "template": "{emoji} {item_name} {price}\n⏰ {date_range}\n📍 {location}\n.\n.\n{hashtags}",
        "location": "400 W. Perkins, McFarland, California",
        "hashtags": "#miranchomarketmcfarland #miranchomarket #mcfarlandca #mcfarland #ahorrosdelasemana #ahorrosdeabarrotes #freshproduce #freshmeats #carniceria #frutasyverduras",
    },
    "Mi Tiendita": {
        "template": "{emoji} {item_name} {price}\n⏰ Ahorros {date_range}\n📍 {location}\n.\n.\n{hashtags}",
        "location": "3145 Payne Ave. San Jose, CA 95117",
        "hashtags": "#OfertasDeLaSemana #MiTiendita #Ahorra #Sabor #Carne #Verduras #ahorros #grocerydeal #weeklysavings #weeklydeals",
    },
    "Sam's Food": {
        "template": "{emoji} {item_name} {price}\n⏰ Pricing {date_range}\n📍 {location}\n.\n.\n{hashtags}",
        "location": "1805 Dairy Ave. Corcoran, CA.",
        "hashtags": "#samsfood #corcoranca #grocerydeals #weeklyspecials #freshproduce #meats",
    },
}

def validate_price(price_str):
    """Smart price validation that handles both dollar and cent formats"""
    if not price_str:
        return False, "Please enter a price"
    
    if '.' in price_str:
        try:
            float(price_str)
            return True, ""
        except ValueError:
            return False, "Invalid dollar format (e.g. 3.99)"
    else:
        try:
            int(price_str)
            return True, ""
        except ValueError:
            return False, "Invalid cents format (e.g. 99)"

def format_price(price_str, price_format):
    """Auto-format price with intelligent dollar/cent detection"""
    try:
        if '.' in price_str:  # Dollar format
            amount = float(price_str)
            formatted = f"${amount:.2f}"
        else:  # Cent format
            cents = int(price_str)
            formatted = f"{cents}¢"
        
        # Add measurement unit
        if price_format == "x lb":
            return f"{formatted}/lb"
        return f"{formatted} each"
    
    except ValueError:
        return "Invalid price format"

def get_emoji(item_name):
    item_lower = item_name.lower()
    for keyword, emoji in emoji_mapping.items():
        if keyword in item_lower:
            return emoji
    return "🛒"  # Default shopping cart emoji

def generate_caption(store, item_name, price, price_format, date_range, sale_type=""):
    store_info = store_data[store]
    return store_info["template"].format(
        emoji=get_emoji(item_name),
        item_name=item_name,
        price=price,
        date_range=date_range,
        location=store_info["location"],
        hashtags=store_info["hashtags"],
        sale_type=sale_type
    )

# Initialize session state
if 'preview' not in st.session_state:
    st.session_state.preview = ""

# App Header
st.title("🛒 Smart Social Media Caption Generator")
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <div style="font-size: 1.5rem; color: #4f46e5; margin-bottom: 1rem;">
        Create Perfect Grocery Store Posts Automatically
    </div>
    <div style="display: flex; justify-content: center; gap: 1rem;">
        <div style="animation: float 3s ease-in-out infinite;">💰</div>
        <div style="animation: float 3s ease-in-out infinite 0.5s;">📅</div>
        <div style="animation: float 3s ease-in-out infinite 1s;">📱</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Form
with st.form("caption_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        store = st.selectbox("🏪 Select Store", list(store_data.keys()))
        item_name = st.text_input("📦 Item Name", placeholder="e.g., Organic Strawberries")
        
    with col2:
        price_format = st.radio("📏 Price Format", ("x lb", "x ea"), horizontal=True)
        price = st.text_input("💵 Enter Price", placeholder="e.g., 3.99 or 99")
    
    date_col, sale_col = st.columns(2)
    with date_col:
        selected_dates = st.date_input(
            "📅 Sale Dates",
            [datetime.today(), datetime.today() + timedelta(days=6)],
            format="MM/DD/YYYY"
        )
    
    sale_type = ""
    if store in ["Ted's Fresh", "IFM Market"]:
        with sale_col:
            sale_type = st.selectbox("🎯 Sale Type", ["3 Day Sale", "4 Day Sale"])

    # Real-time Preview
    preview_emoji = get_emoji(item_name) if item_name else "🛒"
    preview_price = format_price(price, price_format) if price else "[Price]"
    date_range = (
        f"{selected_dates[0].strftime('%m/%d')} - {selected_dates[1].strftime('%m/%d')}"
        if len(selected_dates) == 2 
        else ""
    )
    
    if item_name or price or date_range:
        st.markdown(f"""
        <div class="preview-card">
            <div class="emoji-preview">{preview_emoji}</div>
            <h3>{item_name or '[Item Name]'}</h3>
            <div class="price-badge">{preview_price}</div>
            <p style="color: #64748b; margin-top: 1rem;">{date_range or '[Date Range]'}</p>
        </div>
        """, unsafe_allow_html=True)

    submit = st.form_submit_button("✨ Generate Caption")

# Handle form submission
if submit:
    if not all([item_name, price, len(selected_dates) == 2]):
        st.error("❌ Please fill all required fields")
    else:
        valid_price, error_msg = validate_price(price)
        if not valid_price:
            st.error(f"❌ {error_msg}")
        else:
            formatted_price = format_price(price, price_format)
            caption = generate_caption(
                store=store,
                item_name=item_name,
                price=formatted_price,
                price_format=price_format,
                date_range=date_range,
                sale_type=sale_type
            )
            st.session_state.preview = caption

# Display results
if st.session_state.preview:
    st.markdown("---")
    st.subheader("🎉 Your Caption Is Ready!")
    
    # Copy/Export Section
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="position: relative;">
            <textarea id="captionText" style="position: absolute; left: -9999px;">{st.session_state.preview}</textarea>
            <button onclick="copyToClipboard()" style="
                background: linear-gradient(135deg, #10b981, #3b82f6);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s ease;
            ">
                📋 Copy to Clipboard
            </button>
            <div id="copySuccess" style="display: none; color: #10b981; margin-top: 0.5rem;">✓ Copied!</div>
        </div>
        <script>
            function copyToClipboard() {{
                const textarea = document.getElementById('captionText');
                textarea.select();
                document.execCommand('copy');
                const success = document.getElementById('copySuccess');
                success.style.display = 'block';
                setTimeout(() => {{ success.style.display = 'none'; }}, 2000);
            }}
        </script>
        """, unsafe_allow_html=True)
    
    with col2:
        st.download_button(
            label="📥 Download as TXT",
            data=st.session_state.preview,
            file_name="social_caption.txt",
            mime="text/plain"
        )
    
    # Formatted Caption Display
    st.markdown(f"""
    ```markdown
    {st.session_state.preview}
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; margin-top: 2rem;">
    <div>Made with ❤️ using Streamlit</div>
    <div style="font-size: 0.875rem; margin-top: 0.5rem;">🔍 Smart Price Detection • Auto-Emoji Matching • Store Templates</div>
</div>
""", unsafe_allow_html=True)
