import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Key Check (if using external API that requires a key)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found! Please set the GOOGLE_API_KEY environment variable.")

# Streamlit Configuration
st.set_page_config(page_title="Product Search Bot", page_icon=":shopping_cart:", layout="wide")

# Add custom CSS styling for the input field and button
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
    }
    .stTextInput>div>input {
        font-size: 16px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.header("Welcome to the **Product Search Bot**!")

# Function to fetch top 5 selling products for "Iron Man" (hardcoded for demonstration)
def fetch_ironman_products():
    # Actual product data for Iron Man (using mock data or external API)
    ironman_products = [
        {"name": "Iron Man Action Figure", "price": "₹1,424", "link": "https://www.amazon.in/RVM-Toys-Hulkbuster-Collectible-Decoration/dp/B0CDM4GNXQ?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&smid=A33DKVFB8Y6U9R&gQT=1&th=1", "image": "1.jpg"},
        {"name": "Ironman Rotating Shield with Head Metal Keychain", "price": "₹134", "link": "https://www.meesho.com/multicolour-ironman-rotating-shield-with-head-metal-keychain/p/1q951j?utm_source=google&utm_medium=cpc&utm_campaign=gmc&srsltid=AfmBOorVRUqx8sDOx1h_lUkAcSH3LSdfJIeIDjNIHAznqPZDUL02ynGwRbw", "image": "2.jpg"},
        {"name": "IronMan Bobble Head Action Figure", "price": "₹240", "link": "https://www.satyamstationers.com/products/ironman-bobblehead-with-mobile-holder?variant=47617815052569&country=IN&currency=INR&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOor2P0T6h421VjP5rDK6Z78aJfdSkvKlAC60nhdlOP8dgRRVyk55OeU&gQT=1", "image": "3.jpg"},
        {"name": "Iron man oversized sweatshirt", "price": "₹899", "link": "https://www.thesouledstore.com/product/iron-man-power-mode-men-oversize-sweatshirt?srsltid=AfmBOopTupPJVnDTWPtLgf4gNk1ImUscG7vf-02BwAKAtuiKjTVui0yDPBU&gQT=1", "image": "4.jpg"},
        {"name": "MARVEL CLASSIC Marvel Iron Man Action Figure", "price": "₹399", "link": "https://www.flipkart.com/marvel-classic-iron-man-action-figure-6-super-hero-toys-figures-kids-ages-4/p/itma5bd462bc768c?pid=AFGGZSSZZHGYWFYR&lid=LSTAFGGZSSZZHGYWFYRCVNIUL&marketplace=FLIPKART&q=iron+man&store=tng&srno=s_1_26&otracker=search&otracker1=search&fm=Search&iid=857780e0-aeeb-41fb-af43-bcacc7ff7edf.AFGGZSSZZHGYWFYR.SEARCH&ppt=sp&ppn=sp&ssid=hpkz79sg000000001735240358420&qH=698a077291520164", "image": "5.jpg"}
    ]
    return ironman_products

# Function to fetch dummy products for other searches
def fetch_dummy_products(product_name):
    # Dummy product data
    dummy_data = [
        {"name": f"Top {i+1} {product_name}", "price": f"₹{(i+1) * 500 + 10}", "link": f"https://example.com/product{i+1}", "image": "https://via.placeholder.com/150"}
        for i in range(5)
    ]
    return dummy_data

# Initialize session state for search history if not already done
if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []

# User Input Section for product name
product_input = st.text_input("Enter a product name:", key="product_name", placeholder="e.g., Iron Man, Laptop, Shoes")

submit_button = st.button("Get Top 5 Selling Products")

# # Sidebar: Search History Display
# with st.sidebar:
#     st.subheader("Search History:")
#     for product in st.session_state['search_history']:
#         st.write(f"**{product}**")

# Main Display: If the button is clicked and a product name is entered
if submit_button and product_input:
    with st.spinner('Fetching products...'):
        # Fetch products based on input
        if product_input.lower() == "iron man":
            top_products = fetch_ironman_products()
        else:
            top_products = fetch_dummy_products(product_input)
    
    # Add the search query to history
    st.session_state['search_history'].append(product_input)
    
    st.subheader(f"Top 5 Selling Products for '{product_input}':")
    
    # Display the top 5 products with images and links
    for idx, product in enumerate(top_products, 1):
        st.write(f"**{idx}. {product['name']}**")
        st.write(f"Price: {product['price']}")
        st.write(f"[View Product]({product['link']})")
        st.image(product['image'], width=150)
        st.write("---")
