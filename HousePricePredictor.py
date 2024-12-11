import streamlit as st
import pickle
import json
import base64

# Load model
with open('banglore_home_price_model.pickle', 'rb') as file:
    model = pickle.load(file)

# Load locations from JSON
with open('columns.json', 'r') as file:
    all_coln = json.load(file)["data_columns"]
locations = all_coln[4:]
locations.insert(0, "Select a Location")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_png_as_page_bg('house.jpeg')

# Set custom CSS with adjusted container opacity and smaller size
st.markdown("""
    <style>
    .main {
        background-image: url("house.jpeg");
        background-size: contain;
        background-position: center;
        opacity: 0.8;
    }
    
    .block-container {
        background-color: rgba(0, 0, 0, 0.7);  /* Reduced opacity */
        padding: 2rem;
        border-radius: 10px;
        margin: 0 auto;
        width: 40%;  /* Adjusted container width */
        text-align: center;
    }
    
    h1 {
        color: white !important;
        font-size: 2rem !important;  /* Smaller title size */
        text-align: center !important;
    }
    
    label {
        color: white !important;
    }
    
    .stButton button {
        width: 100%;
        background-color: #2d85f0;
        color: white;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 5px;
    }
    
    .prediction-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #FFFFFF, #F0F2F5);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: popup 0.3s ease-out;
        text-align: center;
    }

    .close-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 20px;
        cursor: pointer;
        color: #FF6B6B;
        background: none;
        border: none;
    }

    @keyframes popup {
        0% { transform: translate(-50%, -60%); opacity: 0; }
        100% { transform: translate(-50%, -50%); opacity: 1; }
    }

    /* Style improvements for select boxes and sliders */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }

    .prediction-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 5px;
        margin-top: 2rem;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #2d85f0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🏠 Bangalore House Price Predictor")

# Inputs
location = st.selectbox("Location", locations)
area = st.text_input("Area (in square feet)")
bhk = st.slider("Bedrooms (BHK)", min_value=1, max_value=20, step=1)
bathrooms = st.slider("Number of Bathrooms", min_value=1, max_value=20, step=1)
balconies = st.slider("Number of Balconies", min_value=0, max_value=5, step=1)
predict_button = st.button("Predict Price")

if predict_button:
    try:
        if location == "Select a Location":
            st.error("Please select a valid location from the dropdown.")
        elif not area:
            st.error("Please enter the area of the house.")
        else:
            location = location.title()

            # Prepare input vector
            input_features = [0] * len(all_coln)
            if location in all_coln:
                input_features[all_coln.index(location)] = 1
            input_features[all_coln.index("total_sqft")] = float(area)
            input_features[all_coln.index("bhk")] = bhk
            input_features[all_coln.index("bath")] = bathrooms
            input_features[all_coln.index("balcony")] = balconies

            # Predict price
            prediction = model.predict([input_features])[0]
            prediction = round(prediction, 2)

            # Display popup with prediction
            popup_html = f"""
            <div class="prediction-popup">
                <button class="close-btn" onclick="this.parentElement.style.display='none'">×</button>
                <h2 style="color: #313A73; margin-bottom: 1rem;">Predicted Price</h2>
                <p style="font-size: 32px; color: #FF6B6B; font-weight: bold;">₹ {prediction} Lakhs</p>
                <p style="color: #666; font-size: 14px;">Based on current market trends</p>
            </div>
            """
            st.markdown(popup_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")

