import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io
import datetime
from dateutil.parser import parse as dateutil_parse
from dateutil.relativedelta import relativedelta
import re

# --- Load API Key and Configure Gemini ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# For deployed Streamlit apps, you would use st.secrets
# API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not API_KEY:
    st.error("🔴 GEMINI_API_KEY not found. Please set it in your .env file (for local) or Streamlit secrets (for deployment).")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    # Use a current multimodal model available in the SDK
    # 'gemini-1.5-flash-latest' is a good choice for speed and multimodal capabilities
    VISION_MODEL = genai.GenerativeModel('gemini-1.5-flash-latest')
    TEXT_MODEL = genai.GenerativeModel('gemini-1.5-flash-latest') # Can use the same or a text-specific one
except Exception as e:
    st.error(f"🔴 Error configuring Gemini API: {e}. Please check your API key and network connection.")
    st.stop()

# --- Constants (Ported from JavaScript) ---
INITIAL_BASE_CAPTIONS = {
    'TEDS_FRESH_MARKET': {
        'THREE_DAY': {'id': 'teds_3_day', 'name': "Ted's Fresh Market (3-Day Sale)", 'language': "english", 'original_example': "Fresh Eggplant or Broccoli 79¢ x lb.\n3 DAYS ONLY 05/13-05/15\n2840 W. Devon Ave.\n.\n.\n.\n#Sale #ShopLocal #Fresh #Groceries #Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats", 'defaultProduct': "Fresh Eggplant or Broccoli", 'defaultPrice': "79¢ x lb.", 'dateFormat': "MM/DD-MM/DD", 'durationTextPattern': "3 DAYS ONLY", 'location': "2840 W. Devon Ave.", 'baseHashtags': "#Sale #ShopLocal #Fresh #Groceries #Produce #USDA #Halal #TedsFreshMarket #GroceryDeals #WeeklyDeals #FreshProduce"},
        'FOUR_DAY': {'id': 'teds_4_day', 'name': "Ted's Fresh Market (4-Day Sale)", 'language': "english", 'original_example': "Sweet Minneola Orange 89¢ x lb.\n4 DAYS ONLY 05/09-05/12\n2840 W. Devon Ave.\n.\n.\n.\n#Sale #ShopLocal #Fresh #Groceries #Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats", 'defaultProduct': "Sweet Minneola Oranges", 'defaultPrice': "89¢ x lb.", 'dateFormat': "MM/DD-MM/DD", 'durationTextPattern': "4 DAYS ONLY", 'location': "2840 W. Devon Ave.", 'baseHashtags': "#Sale #ShopLocal #Fresh #Groceries #Produce #USDA #Halal #TedsFreshMarket #GroceryDeals #WeeklyDeals #CitrusLove"}
    },
    'LA_PRINCESA_MARKET': {
        'WEEK_LONG': {'id': 'laprincesa_week', 'name': "La Princesa Market (Week-Long)", 'language': "spanish", 'original_example': "Bistec de Bola o Bistec de Espaldilla $4.99 x lb.\nHasta 05/20/25\n1260 Main st.  1424 Freedom Blvd.", 'defaultProduct': "Bistec de Bola o Espaldilla", 'defaultPrice': "$4.99 x lb.", 'dateFormat': "Hasta DD/MM/YY", 'durationTextPattern': "Hasta el", 'location': "1260 Main st. & 1424 Freedom Blvd.", 'baseHashtags': "#Ofertas #LaPrincesaMarket #CarneFresca #Ahorra #ComidaLatina #TiendaLocal"}
    },
    'MI_TIENDITA': {
        'WEEKLY_SALE': {'id': 'mitiendita_weekly', 'name': "Mi Tiendita (Ahorros Semanales)", 'language': "spanish", 'original_example': "Trocitos de Puerco $3.49 x lb.\n Ahorros 05/14 - 05/20\n3145 Payne Ave. San Jose, CA 95117\n.\n.\n.\n#OfertasDeLaSemana #MiTiendita #Ahorra #Sabor #Carne #Verduras #ahorros #grocerydeal #weeklysavings #weeklydeals", 'defaultProduct': "Trocitos de Puerco", 'defaultPrice': "$3.49 x lb.", 'dateFormat': "MM/DD - MM/DD", 'durationTextPattern': "Ahorros", 'location': "3145 Payne Ave. San Jose, CA 95117", 'baseHashtags': "#OfertasDeLaSemana #MiTiendita #Ahorra #Sabor #Carne #Verduras #ahorros #grocerydeal #weeklysavings #weeklydeals"}
    },
    'VIVA_SUPERMARKET': {
        'DEAL_UNTIL': {'id': 'viva_deal', 'name': "Viva Supermarket (Weekly Deal)", 'language': "english", 'original_example': "All Natural Halal Chicken Leg Meat $2.49 x lb.\n Deal until from 05/14-05/20\n Only at Viva Supermarket\n.\n.\n.\n#vivasupermarket #grocerydeals #groceryspecials\n#weeklysavings #weeklyspecials #grocery #abarrotes\n#carniceria #mariscos #seafood #produce\n#frutasyverduras #ahorros #ofertas", 'defaultProduct': "All Natural Halal Chicken Leg Meat", 'defaultPrice': "$2.49 x lb.", 'dateFormat': "MM/DD-MM/DD", 'durationTextPattern': "Deal until from", 'location': "Viva Supermarket", 'baseHashtags': "#vivasupermarket #grocerydeals #groceryspecials #weeklysavings #weeklyspecials #grocery #abarrotes #carniceria #mariscos #seafood #produce #frutasyverduras #ahorros #ofertas"}
    },
    'INTERNATIONAL_FRESH_MARKET': {
        'THREE_DAY_SALE': {'id': 'ifm_3_day', 'name': "International Fresh Market (3 Day Sale)", 'language': "english", 'original_example': "3 DAY SALE\n 05/13 - 05/15\n Fresh Zucchini 35¢ x lb.\n.\n.\n#Naperville #Fresh #Market #Produce #Meat\n#internationalfreshmarket", 'defaultProduct': "Fresh Zucchini", 'defaultPrice': "35¢ x lb.", 'dateFormat': "MM/DD - MM/DD", 'durationTextPattern': "3 DAY SALE", 'location': "International Fresh Market, Naperville", 'baseHashtags': "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket"},
        'CUSTOMER_APPRECIATION_SALE': {'id': 'ifm_customer_appreciation', 'name': "International Fresh Market (Customer Appreciation Sale)", 'language': "english", 'original_example': "CUSTOMER APPRECIATION SALE \n Fresh Green Cabbage 25¢ x lb.\n4 Days Only 05/09-05/12\n.\n#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket", 'defaultProduct': "Fresh Green Cabbage", 'defaultPrice': "25¢ x lb.", 'dateFormat': "MM/DD-MM/DD", 'durationTextPattern': "4 Days Only", 'location': "International Fresh Market, Naperville", 'baseHashtags': "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket"}
    }
}
TONE_OPTIONS = [{'value': "Simple", 'label': "Simple & Clear"}, {'value': "Fun", 'label': "Fun & Engaging"}, {'value': "Excited", 'label': "Excited & Urgent"}, {'value': "Professional", 'label': "Professional & Direct"}, {'value': "Friendly", 'label': "Friendly & Warm"}, {'value': "Informative", 'label': "Informative & Detailed"}, {'value': "Humorous", 'label': "Humorous & Witty"}, {'value': "Seasonal", 'label': "Seasonal / Festive"}, {'value': "Elegant", 'label': "Elegant & Refined"}, {'value': "Bold", 'label': "Bold & Punchy"}, {'value': "Nostalgic", 'label': "Nostalgic & Heartfelt"}]
PREDEFINED_PRICES = [{'value': "¢ / lb.", 'label': "¢ / lb. (e.g., 69¢ / lb.)"}, {'value': "$ / lb.", 'label': "$X.XX / lb. (e.g., $4.99 / lb.)"}, {'value': "$ each", 'label': "$X.XX each (e.g., $1.50 each)"}, {'value': "¢ each", 'label': "¢ each (e.g., 99¢ each)"}, {'value': "X for $Y", 'label': "X for $Y.YY (e.g., 2 for $5.00)"}, {'value': "CUSTOM", 'label': "Enter Custom Price..."}]

# --- Helper Functions (Ported and Adapted from JavaScript) ---
def get_current_day_for_teds():
    # JS: Sunday is 0, Monday is 1... Saturday is 6
    # Python: Monday is 0, Sunday is 6 (datetime.weekday())
    # To match JS getDay() for Ted's logic (Tuesday=2, Friday=5):
    py_weekday = datetime.date.today().weekday() # Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    if py_weekday == 1: return 2 # Tuesday
    if py_weekday == 4: return 5 # Friday
    return py_weekday # Return other days as is, though Ted's logic was specific

def get_nth_day_of_week(year, month, week_num, day_of_week_py): # day_of_week_py: Mon=0, Sun=6
    count = 0
    for day_val in range(1, 32):
        try:
            d = datetime.date(year, month, day_val)
            if d.weekday() == day_of_week_py:
                count += 1
                if count == week_num:
                    return d
        except ValueError: # Day out of range for month
            break
    return None

def get_last_day_of_week(year, month, day_of_week_py): # day_of_week_py: Mon=0, Sun=6
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1
    last_day_of_month = (datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)).day
    for day_val in range(last_day_of_month, 0, -1):
        try:
            d = datetime.date(year, month, day_val)
            if d.weekday() == day_of_week_py:
                return d
        except ValueError:
            continue # Should not happen if day_val is correct
    return None


def get_holiday_context(start_date_str, end_date_str):
    if not start_date_str or not end_date_str:
        return ""
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return "" # Invalid date format

    # Python months are 1-12. Python weekdays Mon=0, Sun=6
    holidays = [
        {'name': "New Year's Day", 'type': 'fixed', 'month': 1, 'day': 1},
        {'name': "Martin Luther King Jr. Day", 'type': 'nthDayOfWeek', 'month': 1, 'week': 3, 'dayOfWeek': 0}, # 3rd Mon of Jan
        {'name': "Valentine's Day", 'type': 'fixed', 'month': 2, 'day': 14},
        {'name': "Presidents' Day", 'type': 'nthDayOfWeek', 'month': 2, 'week': 3, 'dayOfWeek': 0}, # 3rd Mon of Feb
        {'name': "St. Patrick's Day", 'type': 'fixed', 'month': 3, 'day': 17},
        {'name': "Easter Season", 'type': 'monthRange', 'startMonth': 3, 'endMonth': 4}, # Approx
        {'name': "Memorial Day", 'type': 'lastDayOfWeek', 'month': 5, 'dayOfWeek': 0}, # Last Mon of May
        {'name': "Juneteenth", 'type': 'fixed', 'month': 6, 'day': 19},
        {'name': "Independence Day (4th of July)", 'type': 'fixed', 'month': 7, 'day': 4},
        {'name': "Labor Day", 'type': 'nthDayOfWeek', 'month': 9, 'week': 1, 'dayOfWeek': 0}, # 1st Mon of Sep
        # Columbus Day is tricky due to varying observance; simplified:
        {'name': "Indigenous Peoples' Day/Columbus Day", 'type': 'nthDayOfWeek', 'month': 10, 'week': 2, 'dayOfWeek': 0}, # 2nd Mon of Oct
        {'name': "Halloween", 'type': 'fixed', 'month': 10, 'day': 31},
        {'name': "Veterans Day", 'type': 'fixed', 'month': 11, 'day': 11},
        {'name': "Thanksgiving Day", 'type': 'nthDayOfWeek', 'month': 11, 'week': 4, 'dayOfWeek': 3}, # 4th Thu of Nov
        {'name': "Christmas Day", 'type': 'fixed', 'month': 12, 'day': 25}
    ]

    current_date = start_date
    while current_date <= end_date:
        cY = current_date.year
        cM = current_date.month
        cDOM = current_date.day
        cDOW_py = current_date.weekday() # Mon=0, Sun=6

        for h in holidays:
            if h['type'] == 'fixed' and h['month'] == cM and h['day'] == cDOM:
                return h['name']
            elif h['type'] == 'nthDayOfWeek':
                holiday_date = get_nth_day_of_week(cY, h['month'], h['week'], h['dayOfWeek'])
                if holiday_date and holiday_date == current_date:
                    return h['name']
            elif h['type'] == 'lastDayOfWeek':
                holiday_date = get_last_day_of_week(cY, h['month'], h['dayOfWeek'])
                if holiday_date and holiday_date == current_date:
                    return h['name']
            elif h['type'] == 'monthRange' and h['startMonth'] <= cM <= h['endMonth']:
                 # This is a simplification; actual Easter date varies.
                 # For monthRange, we can just say it's in the season if the period overlaps.
                return h['name'] # Return first one found in range
        current_date += datetime.timedelta(days=1)
    return ""

def format_date_string_for_caption_display(date_obj, lang="english", is_hasta_format=False):
    if not date_obj: return ''
    day = f"{date_obj.day:02d}"
    month = f"{date_obj.month:02d}"
    year_yy = f"{date_obj.year % 100:02d}"
    year_yyyy = f"{date_obj.year:04d}"

    if is_hasta_format:
        if lang == "spanish": return f"{day}/{month}" # Potentially add /YY if format implies
        return f"{month}/{day}"
    return f"{month}/{day}"

def format_dates_for_caption_context(start_str, end_str, date_format_pattern, lang):
    if not start_str or not end_str: return "DATES_MISSING"
    try:
        start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        return "INVALID_DATES"

    is_hasta = date_format_pattern.lower().startswith("hasta")
    include_year = "YY" in date_format_pattern or "YYYY" in date_format_pattern

    start_formatted = format_date_string_for_caption_display(start_date, lang, is_hasta)
    end_formatted = format_date_string_for_caption_display(end_date, lang, is_hasta)

    if include_year and is_hasta: # e.g. Hasta DD/MM/YY
        year_part = f"/{end_date.year % 100:02d}" if "YY" in date_format_pattern else f"/{end_date.year:04d}"
        end_formatted += year_part
    elif include_year and not is_hasta: # e.g. MM/DD/YY - MM/DD/YY
        year_part_start = f"/{start_date.year % 100:02d}" if "YY" in date_format_pattern else f"/{start_date.year:04d}"
        year_part_end = f"/{end_date.year % 100:02d}" if "YY" in date_format_pattern else f"/{end_date.year:04d}"
        start_formatted += year_part_start
        end_formatted += year_part_end


    if is_hasta:
        return end_formatted
    separator = " - " if ' - ' in date_format_pattern else "-"
    return f"{start_formatted}{separator}{end_formatted}"


def get_final_price_string(price_format, price_value, custom_val):
    if price_format == "CUSTOM": return custom_val
    if price_format == "X for $Y": return price_value or "[Price Value]" # User inputs full string like "2 for $5"
    if not price_value: return f"[Price Value] {price_format.split(' ')[1] if len(price_format.split(' ')) > 1 else ''}"

    if price_format == "¢ / lb.": return f"{price_value}¢ / lb."
    if price_format == "$ / lb.": return f"${price_value} / lb."
    if price_format == "$ each": return f"${price_value} each"
    if price_format == "¢ each": return f"{price_value}¢ each"
    return price_value # Should not happen if format is one of above

def find_store_key_by_name(name_from_image, base_captions_data):
    if not name_from_image: return None
    normalized_name_from_image = re.sub(r'[^A-Z0-9]', '', name_from_image.upper())

    for key, store_variants in base_captions_data.items():
        first_variant_key = list(store_variants.keys())[0]
        store_display_name_raw = store_variants[first_variant_key].get('name', key).split('(')[0].strip()
        normalized_store_display_name = re.sub(r'[^A-Z0-9]', '', store_display_name_raw.upper())

        if normalized_store_display_name in normalized_name_from_image or \
           normalized_name_from_image in normalized_store_display_name:
            return key
    return None

def try_parse_date_from_image_text(text_from_image):
    if not text_from_image or not isinstance(text_from_image, str):
        return None
    
    text_from_image = text_from_image.strip()
    current_year = datetime.date.today().year
    
    # Attempt common formats using dateutil.parser for flexibility
    # Add common delimiters that might be misread from OCR
    text_to_parse = text_from_image.replace('.', '/').replace('-', '/')
    
    try:
        # Try parsing with dayfirst=False (common in US MM/DD/YY)
        dt_obj = dateutil_parse(text_to_parse, dayfirst=False, default=datetime.datetime(current_year, 1, 1))
        # Check if year seems reasonable (e.g., if year is 1, it means it used the default)
        if dt_obj.year == current_year or abs(dt_obj.year - current_year) <= 5: # Allow some flexibility
             # If only M/D was parsed, dateutil fills current year. Check if it makes sense.
            if text_to_parse.count('/') == 1 and dt_obj.year != current_year : # If M/D was given, it should use current year
                if not re.search(r'\b(19\d{2}|20\d{2})\b', text_to_parse): # if no year was in original string
                     dt_obj = dt_obj.replace(year=current_year)

            # Check if the parsed date is within a reasonable range for a sale
            if abs(dt_obj.year - current_year) <= 10: # More generous range for parsed years
                 return dt_obj.strftime("%Y-%m-%d")

    except (ValueError, TypeError):
        pass # Try other methods if dateutil fails

    # Fallback to regex for specific M/D or M/D/YY patterns if dateutil is not robust enough or gives odd years
    # Order matters: more specific first
    patterns = [
        r"(\d{1,2})[\/\.](\d{1,2})[\/\.](\d{2,4})", # MM/DD/YYYY or MM/DD/YY
        r"(\d{1,2})[\/\.](\d{1,2})"                 # MM/DD
    ]
    for pattern in patterns:
        match = re.match(pattern, text_from_image)
        if match:
            parts = match.groups()
            try:
                if len(parts) == 3: # M/D/Y
                    m, d, y_str = int(parts[0]), int(parts[1]), parts[2]
                    y = int(y_str)
                    if len(y_str) == 2:
                        y = 2000 + y if y < 70 else 1900 + y # Heuristic for 2-digit years
                    elif len(y_str) != 4 : # not a 4 digit year
                        continue # skip if year format is strange
                    return datetime.date(y, m, d).strftime("%Y-%m-%d")
                elif len(parts) == 2: # M/D
                    m, d = int(parts[0]), int(parts[1])
                    return datetime.date(current_year, m, d).strftime("%Y-%m-%d")
            except ValueError:
                continue # Invalid date parts
    return None


# --- Streamlit App State Initialization ---
if 'analyzed_image_data_set' not in st.session_state:
    st.session_state.analyzed_image_data_set = []
if 'global_selected_store_key' not in st.session_state:
    st.session_state.global_selected_store_key = list(INITIAL_BASE_CAPTIONS.keys())[0]
if 'global_selected_tone' not in st.session_state:
    st.session_state.global_selected_tone = TONE_OPTIONS[0]['value']
if 'uploaded_files_cache' not in st.session_state: # To store actual UploadedFile objects temporarily
    st.session_state.uploaded_files_cache = []
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""
if 'is_analyzing_images' not in st.session_state:
    st.session_state.is_analyzing_images = False

# --- Main App UI ---
st.set_page_config(layout="wide", page_title="Caption Generator")
st.title("✨ Social Media Caption Generator ✨")
st.caption(f"Powered by Gemini API. Current Date: {datetime.date.today().strftime('%A, %B %d, %Y')}")

if st.session_state.error_message:
    st.error(st.session_state.error_message)
    st.session_state.error_message = "" # Clear after displaying

# --- Image Upload Section ---
uploaded_file_objects = st.file_uploader(
    "Upload Image(s) for Analysis (PNG, JPG, WEBP)",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    key="image_uploader_widget" # Unique key for the widget itself
)

# Process newly uploaded files and add to a temporary cache if they are different from last upload
if uploaded_file_objects:
    # Basic way to check if the list of uploaded files has changed
    # This isn't perfect but avoids re-adding if the user just re-selects the same files
    new_upload_set = { (f.name, f.size) for f in uploaded_file_objects }
    current_cache_set = { (f.name, f.size) for f in st.session_state.uploaded_files_cache }

    if new_upload_set != current_cache_set:
        st.session_state.uploaded_files_cache = uploaded_file_objects
        st.session_state.analyzed_image_data_set = [] # Clear previous analysis results
        st.info(f"{len(uploaded_file_objects)} file(s) selected. Click 'Analyze' to process.")

if st.session_state.uploaded_files_cache:
    st.subheader("Uploaded Image Previews:")
    cols = st.columns(min(5, len(st.session_state.uploaded_files_cache)))
    for i, uploaded_file in enumerate(st.session_state.uploaded_files_cache):
        cols[i % 5].image(uploaded_file.getvalue(), caption=uploaded_file.name, width=120)

    if st.button("👁️ Analyze Selected Image(s)", disabled=st.session_state.is_analyzing_images, type="primary", use_container_width=True):
        st.session_state.is_analyzing_images = True
        st.session_state.analyzed_image_data_set = [] # Clear previous results before new analysis
        st.session_state.error_message = ""
        
        progress_bar = st.progress(0)
        total_files = len(st.session_state.uploaded_files_cache)

        for idx, uploaded_file_obj in enumerate(st.session_state.uploaded_files_cache):
            progress_text = f"Analyzing {uploaded_file_obj.name} ({idx+1}/{total_files})..."
            progress_bar.progress((idx + 1) / total_files, text=progress_text)
            
            analysis_data_item = {
                "id": f"image-{uploaded_file_obj.name}-{idx}",
                "original_filename": uploaded_file_obj.name,
                "image_bytes_for_preview": uploaded_file_obj.getvalue(),
                "itemProduct": "",
                "selectedStoreKey": st.session_state.global_selected_store_key,
                "selectedPriceFormat": PREDEFINED_PRICES[1]['value'], # Default to "$ / lb."
                "itemPriceValue": "",
                "customItemPrice": "",
                "dateRange": {
                    "start": datetime.date.today().strftime("%Y-%m-%d"),
                    "end": (datetime.date.today() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
                },
                "generatedCaption": "",
                "isLoadingCaption": False,
                "analysisError": None
            }
            try:
                pil_image = Image.open(uploaded_file_obj)
                
                image_analysis_prompt = f"""Analyze this grocery sale image. Extract:
Product Name: [Primary product name or names clearly featured for sale]
Price: [Price of the primary product, including currency and unit, e.g., $1.99/lb, 2 for $5.00, 99¢ each]
Sale Dates: [Sale period, e.g., MM/DD-MM/DD, Ends MM/DD, May 15-20. If year is present, include it.]
Store Name: [Visible store name, if any]
Promotional Text: [Any other relevant promotional phrases or taglines, like "3 Days Only", "Special Offer"]
If a field is not found or unclear, state "Not found" for that field."""

                response = VISION_MODEL.generate_content([image_analysis_prompt, pil_image])
                analysis_text = response.text
                
                # Parse analysis_text (Python regex)
                product_match = re.search(r"Product Name: (.*)", analysis_text, re.IGNORECASE)
                if product_match and product_match.group(1).lower().strip() != "not found":
                    analysis_data_item['itemProduct'] = product_match.group(1).strip()

                price_match = re.search(r"Price: (.*)", analysis_text, re.IGNORECASE)
                if price_match and price_match.group(1).lower().strip() != "not found":
                    extracted_price_str = price_match.group(1).strip()
                    # Attempt to map to predefined price formats
                    found_format = False
                    for p_format in PREDEFINED_PRICES:
                        if p_format['value'] == "CUSTOM" or p_format['value'] == "X for $Y": continue # Handle X for Y separately
                        unit_part = p_format['value'].split(" ", 1)[1] if " " in p_format['value'] else p_format['value']
                        if unit_part.lower() in extracted_price_str.lower():
                            analysis_data_item['selectedPriceFormat'] = p_format['value']
                            # Extract numeric part
                            price_val_match = re.search(r"([\d\.]+)", extracted_price_str)
                            if price_val_match:
                                analysis_data_item['itemPriceValue'] = price_val_match.group(1)
                            else: # If no number found but unit matches, store full string for custom review
                                analysis_data_item['selectedPriceFormat'] = "CUSTOM"
                                analysis_data_item['customItemPrice'] = extracted_price_str
                            found_format = True
                            break
                    if "for" in extracted_price_str.lower() and "$" in extracted_price_str: # Basic check for "X for $Y"
                        analysis_data_item['selectedPriceFormat'] = "X for $Y"
                        analysis_data_item['itemPriceValue'] = extracted_price_str # User to verify/edit this string
                        found_format = True

                    if not found_format:
                        analysis_data_item['selectedPriceFormat'] = "CUSTOM"
                        analysis_data_item['customItemPrice'] = extracted_price_str
                
                store_name_match = re.search(r"Store Name: (.*)", analysis_text, re.IGNORECASE)
                if store_name_match and store_name_match.group(1).lower().strip() != "not found":
                    detected_store_name = store_name_match.group(1).strip()
                    matched_key = find_store_key_by_name(detected_store_name, INITIAL_BASE_CAPTIONS)
                    if matched_key:
                        analysis_data_item['selectedStoreKey'] = matched_key
                    else:
                        analysis_data_item['analysisError'] = (analysis_data_item.get('analysisError') or "") + f"Store '{detected_store_name}' not in known list. "

                date_match = re.search(r"Sale Dates: (.*)", analysis_text, re.IGNORECASE)
                if date_match and date_match.group(1).lower().strip() != "not found":
                    dates_str = date_match.group(1).strip()
                    # Split by common range delimiters: "to", "-", "–"
                    date_parts = re.split(r'\s+to\s+|\s*-\s*|\s*–\s*', dates_str) 
                    
                    parsed_start_date_str = None
                    parsed_end_date_str = None

                    if len(date_parts) >= 1:
                        parsed_start_date_str = try_parse_date_from_image_text(date_parts[0])
                    if len(date_parts) >= 2:
                        # If the second part is just a day, assume same month/year as start
                        end_part_text = date_parts[1]
                        if re.match(r"^\d{1,2}$", end_part_text.strip()) and parsed_start_date_str:
                            start_dt = datetime.datetime.strptime(parsed_start_date_str, "%Y-%m-%d").date()
                            end_part_text = f"{start_dt.month}/{end_part_text.strip()}"
                            if start_dt.day > int(date_parts[1].strip()): # if end day is before start day, assume next month
                                end_part_text = f"{ (start_dt.month % 12) +1 }/{date_parts[1].strip()}"


                        parsed_end_date_str = try_parse_date_from_image_text(end_part_text)
                    
                    if parsed_start_date_str:
                        analysis_data_item['dateRange']['start'] = parsed_start_date_str
                        if not parsed_end_date_str: # If only start date found, default end date
                             analysis_data_item['dateRange']['end'] = (datetime.datetime.strptime(parsed_start_date_str, "%Y-%m-%d").date() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
                    if parsed_end_date_str:
                        analysis_data_item['dateRange']['end'] = parsed_end_date_str
                        if not parsed_start_date_str: # If only end date found (e.g. "Ends MM/DD"), set start to today or earlier
                            end_dt = datetime.datetime.strptime(parsed_end_date_str, "%Y-%m-%d").date()
                            analysis_data_item['dateRange']['start'] = min(datetime.date.today(), end_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")


                    # Final validation of date range
                    try:
                        s_final = datetime.datetime.strptime(analysis_data_item['dateRange']['start'], "%Y-%m-%d").date()
                        e_final = datetime.datetime.strptime(analysis_data_item['dateRange']['end'], "%Y-%m-%d").date()
                        if s_final > e_final: # If start is after end, reset to default range
                            analysis_data_item['analysisError'] = (analysis_data_item.get('analysisError') or "") + f"Parsed dates out of order ({s_final} > {e_final}). Check dates. "
                            analysis_data_item['dateRange']['start'] = datetime.date.today().strftime("%Y-%m-%d")
                            analysis_data_item['dateRange']['end'] = (datetime.date.today() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
                    except ValueError:
                         analysis_data_item['analysisError'] = (analysis_data_item.get('analysisError') or "") + "Date parsing resulted in invalid format. "
                         # Reset to default
                         analysis_data_item['dateRange']['start'] = datetime.date.today().strftime("%Y-%m-%d")
                         analysis_data_item['dateRange']['end'] = (datetime.date.today() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")


            except Exception as e:
                analysis_data_item['analysisError'] = (analysis_data_item.get('analysisError') or "") + f"Error during AI analysis: {str(e)}"
            
            st.session_state.analyzed_image_data_set.append(analysis_data_item)
        
        progress_bar.empty() # Clear progress bar
        st.session_state.is_analyzing_images = False
        st.success("Image analysis complete. Review and generate captions below.")
        st.experimental_rerun()


# --- Global Tone Selector ---
tone_labels_dict = {tone['value']: tone['label'] for tone in TONE_OPTIONS}
selected_tone_val = st.sidebar.selectbox(
    "Global Caption Tone",
    options=list(tone_labels_dict.keys()),
    format_func=lambda x: tone_labels_dict[x],
    index=list(tone_labels_dict.keys()).index(st.session_state.global_selected_tone),
    key="global_tone_selector"
)
if selected_tone_val: # To handle None if options are empty (should not happen here)
    st.session_state.global_selected_tone = selected_tone_val


# --- Display Analyzed Data and Generate Captions ---
if st.session_state.analyzed_image_data_set:
    st.markdown("---")
    st.header("Image Details & Caption Generation")
    
    for index, data_item_ref in enumerate(st.session_state.analyzed_image_data_set): # Iterate by reference
        item_id = data_item_ref['id'] # Unique ID for keys

        with st.container(): # Use st.container for better separation and borders
            st.markdown(f"#### Image: {data_item_ref.get('original_filename', item_id)}")
            if data_item_ref.get('analysisError'):
                st.warning(f"Notes/Errors: {data_item_ref['analysisError']}")

            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(data_item_ref['image_bytes_for_preview'], caption="Analyzed Image", use_column_width=True)
            
            with col2:
                data_item_ref['itemProduct'] = st.text_input("Product Name", value=data_item_ref.get('itemProduct', ''), key=f"product_{item_id}")

                store_names_map = {key: details[list(details.keys())[0]]['name'].split('(')[0].strip() or key.replace('_', ' ')
                                   for key, details in INITIAL_BASE_CAPTIONS.items()}
                
                # Find current index for selectbox
                current_store_key = data_item_ref.get('selectedStoreKey', st.session_state.global_selected_store_key)
                try:
                    store_index = list(store_names_map.keys()).index(current_store_key)
                except ValueError:
                    store_index = 0 # Default to first store if key not found
                
                selected_store_name_display = st.selectbox(
                    "Store",
                    options=list(store_names_map.values()), # Show names in selectbox
                    index=store_index,
                    key=f"store_{item_id}"
                )
                data_item_ref['selectedStoreKey'] = next(key for key, name_val in store_names_map.items() if name_val == selected_store_name_display)

                # Price Format
                price_format_labels_dict = {p['value']: p['label'] for p in PREDEFINED_PRICES}
                current_price_format = data_item_ref.get('selectedPriceFormat', PREDEFINED_PRICES[1]['value'])
                try:
                    price_format_idx = list(price_format_labels_dict.keys()).index(current_price_format)
                except ValueError:
                    price_format_idx = 1 # Default
                
                selected_price_format_val = st.selectbox("Price Format", 
                                                         options=list(price_format_labels_dict.keys()),
                                                         format_func=lambda x: price_format_labels_dict[x],
                                                         index=price_format_idx,
                                                         key=f"price_format_{item_id}")
                data_item_ref['selectedPriceFormat'] = selected_price_format_val

                if selected_price_format_val == "CUSTOM":
                    data_item_ref['customItemPrice'] = st.text_input("Custom Price Text", value=data_item_ref.get('customItemPrice', ''), key=f"custom_price_{item_id}")
                elif selected_price_format_val == "X for $Y":
                     data_item_ref['itemPriceValue'] = st.text_input("Price (e.g., 2 for $5.00)", value=data_item_ref.get('itemPriceValue', ''), key=f"price_value_xfory_{item_id}")
                else: # Standard formats like $ / lb.
                    data_item_ref['itemPriceValue'] = st.text_input("Price Value (e.g., 1.99 or 79)", value=data_item_ref.get('itemPriceValue', ''), key=f"price_value_{item_id}")

                # Dates
                date_col1, date_col2 = st.columns(2)
                with date_col1:
                    try:
                        start_dt_val = datetime.datetime.strptime(data_item_ref['dateRange']['start'], "%Y-%m-%d").date()
                    except ValueError:
                        start_dt_val = datetime.date.today() # Fallback
                    new_start_date = st.date_input("Start Date", value=start_dt_val, key=f"start_date_{item_id}")
                    data_item_ref['dateRange']['start'] = new_start_date.strftime("%Y-%m-%d")
                with date_col2:
                    try:
                        end_dt_val = datetime.datetime.strptime(data_item_ref['dateRange']['end'], "%Y-%m-%d").date()
                    except ValueError:
                        end_dt_val = datetime.date.today() + datetime.timedelta(days=6) # Fallback
                    new_end_date = st.date_input("End Date", value=end_dt_val, key=f"end_date_{item_id}")
                    data_item_ref['dateRange']['end'] = new_end_date.strftime("%Y-%m-%d")


            # Button to generate caption
            generate_key = f"generate_btn_{item_id}"
            caption_loading_key = f"caption_loading_{item_id}"

            if caption_loading_key not in st.session_state:
                 st.session_state[caption_loading_key] = False


            if st.button(f"✍️ Generate Caption for This Image", key=generate_key, disabled=st.session_state[caption_loading_key], type="primary", use_container_width=True):
                st.session_state[caption_loading_key] = True
                st.experimental_rerun() # Show loading state

            if st.session_state[caption_loading_key]: # If button was clicked and now it's loading
                with st.spinner("Generating caption..."):
                    data_item_ref['generatedCaption'] = "" # Clear previous before generating
                    store_details_key = data_item_ref['selectedStoreKey']
                    store_info = INITIAL_BASE_CAPTIONS.get(store_details_key)
                    
                    if not store_info:
                        data_item_ref['analysisError'] = (data_item_ref.get('analysisError') or "") + "Selected store details not found."
                        st.session_state[caption_loading_key] = False
                        st.experimental_rerun()
                    else:
                        # Determine sale detail key (e.g., THREE_DAY, WEEK_LONG)
                        # This logic might need refinement based on your store structures
                        sale_detail_key = list(store_info.keys())[0] # Default to first variant
                        if store_details_key == 'TEDS_FRESH_MARKET':
                            day_for_teds = get_current_day_for_teds()
                            sale_detail_key = 'THREE_DAY' if day_for_teds == 2 else 'FOUR_DAY' if day_for_teds == 5 else 'THREE_DAY'
                        
                        caption_structure = store_info.get(sale_detail_key)
                        if not caption_structure:
                            data_item_ref['analysisError'] = (data_item_ref.get('analysisError') or "") + f"Caption structure for '{sale_detail_key}' not found."
                            st.session_state[caption_loading_key] = False
                            st.experimental_rerun()

                        else:
                            final_price = get_final_price_string(data_item_ref['selectedPriceFormat'], data_item_ref['itemPriceValue'], data_item_ref['customItemPrice'])
                            if not final_price or "[Price Value]" in final_price:
                                data_item_ref['analysisError'] = (data_item_ref.get('analysisError') or "") + "Invalid price for caption. "
                            else:
                                display_dates = format_dates_for_caption_context(
                                    data_item_ref['dateRange']['start'], data_item_ref['dateRange']['end'],
                                    caption_structure['dateFormat'], caption_structure['language']
                                )
                                holiday_ctx = get_holiday_context(data_item_ref['dateRange']['start'], data_item_ref['dateRange']['end'])

                                prompt_list = [
                                    f"Generate a social media caption.\nStore & Sale Type: {caption_structure['name']}",
                                    f"Product on Sale: {data_item_ref['itemProduct']}",
                                    f"Price: {final_price}",
                                    f"Sale Dates (formatted for display): {display_dates}. The sale runs from {data_item_ref['dateRange']['start']} (YYYY-MM-DD) to {data_item_ref['dateRange']['end']} (YYYY-MM-DD)."
                                ]
                                if holiday_ctx: prompt_list.append(f"This period includes or is around {holiday_ctx}.")
                                
                                prompt_list.extend([
                                    f"Location: {caption_structure['location']} (Must be included exactly as written).",
                                    f"Language for caption: {caption_structure['language']}.",
                                    f"Desired Tone: {st.session_state.global_selected_tone}."
                                ])
                                if holiday_ctx and st.session_state.global_selected_tone == "Seasonal / Festive":
                                     prompt_list.append(f"Especially emphasize {holiday_ctx}.")
                                
                                prompt_list.extend([
                                    f"Original Caption Example (for style/content reference, make new one unique):\n\"{caption_structure['original_example']}\"",
                                    "The new caption should:",
                                    "- Be unique & engaging. Incorporate product, price, dates, location.",
                                    f"- Use appropriate emojis based on the product, tone, and the detected holiday context ({holiday_ctx or 'general period'}).",
                                    f"- Include relevant SEO hashtags (base: {caption_structure['baseHashtags']}, add new creative ones{f', related to {holiday_ctx}' if holiday_ctx else ''}).",
                                    "- For date ranges in the caption, primarily use month/day format (e.g., 05/14 - 05/20). For 'Hasta' or 'Until' type sales, if the original example included a year, you may include the year; otherwise, use month/day (e.g., 'Ends 05/20').",
                                    f"- The location \"{caption_structure['location']}\" must be present. If location is a city, ensure store name is also clear.",
                                    "- Well-formatted for social media (line breaks)."
                                ])
                                if caption_structure.get('durationTextPattern'):
                                    prompt_list.append(f"Pay close attention to the phrase \"{caption_structure['durationTextPattern']}\" from the original example when formatting the sale duration with the dates {display_dates}.\n")
                                
                                final_prompt_for_caption = "\n".join(prompt_list)

                                try:
                                    response = TEXT_MODEL.generate_content(final_prompt_for_caption)
                                    data_item_ref['generatedCaption'] = response.text.strip()
                                except Exception as e:
                                    data_item_ref['analysisError'] = (data_item_ref.get('analysisError') or "") + f"Caption API error: {str(e)}"
                            
                            st.session_state[caption_loading_key] = False
                            st.experimental_rerun() # Update UI with caption or error

            if data_item_ref.get('generatedCaption'):
                st.text_area("📝 Generated Caption:", value=data_item_ref['generatedCaption'], height=200, key=f"caption_output_{item_id}", help="Manually copy the text below.")
                st.code(data_item_ref['generatedCaption'], language=None)
            
            st.markdown("---") # Separator for each image item

else:
    st.info("☝️ Upload some images to get started!")

st.sidebar.markdown("---")
st.sidebar.markdown("Developed by You!")
st.sidebar.markdown(f"Caption Generator v3.0 Streamlit // Based on original by AI User // Today: {datetime.date.today().strftime('%Y-%m-%d')}")