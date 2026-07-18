import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Import our feature configuration mapping arrays
from model_config import FEATURE_NAMES, NEIGHBORHOODS, MS_ZONING, HOUSE_STYLE, GARAGE_TYPE

# --- CONFIGURATION VARIABLES ---
USD_TO_PKR = 278.0  # Adjust this rate to match current market conditions if needed

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="House Valuation Engine", 
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM DARK/BLACK DESIGN SYSTEM CSS ---
st.markdown("""
    <style>
    /* Root Design Tokens Overridden for True Dark Theme */
    :root {
        --primary: #3b82f6;
        --primary-light: #60a5fa;
        --primary-dark: #1d4ed8;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --surface: #1e293b;
        --surface-dark: #0f172a;
        --border: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }
    
    /* Global Styling to Force Pure Black / Dark Charcoal Gradient background */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #020408 100%) !important;
        color: var(--text-primary) !important;
    }
    
    /* Typography Hierarchy & Strict Color Enforcement */
    h1, h2, h3, h4, h5, h6, label, p, span, .stMarkdown p {
        color: #ffffff !important;
    }
    
    /* Card Design System */
    .card {
        background: #111827;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
    }
    
    .card-highlight {
        background: linear-gradient(135deg, #0f172a 0%, #064e3b 100%);
        border: 1px solid #10b981;
    }
    
    /* Metrics Cards Custom Adjustments */
    div[data-testid="stMetricBlock"] {
        background: #0f172a !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stMetricBlock"]:hover {
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.25) !important;
        border-color: var(--primary) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.025em !important;
        text-transform: uppercase !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important; /* Slightly smaller to prevent text bleed with longer numbers */
        font-weight: 700 !important;
    }
    
    /* Navigation / Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 500;
        border: 1px solid var(--border);
        background: #0f172a;
        color: var(--text-secondary) !important;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] [data-baseweb="tab"] {
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
    }
    
    /* Buttons Custom Dark UI Look */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: 600;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white !important;
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
    }
    
    /* Form Inputs Custom Dark Theme Styling */
    .stNumberInput div div input,
    .stSelectbox div div select,
    .stSlider div div div input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: 1px solid var(--border) !important;
    }
    
    /* Sidebar Overhaul */
    [data-testid="stSidebar"] {
        background: #070a12 !important;
        border-right: 1px solid var(--border);
    }
    
    /* Banner/Notification System Overrides */
    .stInfo, .stSuccess, .stWarning {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 16px;
    }
    
    .stInfo {
        border-left-color: var(--primary) !important;
        background-color: #0c4a6e !important;
        color: #e0f2fe !important;
    }
    
    .stSuccess {
        border-left-color: var(--success) !important;
        background-color: #064e3b !important;
        color: #d1fae5 !important;
    }
    
    /* Custom Badges for Dark UI */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px 4px 4px 0;
    }
    
    .badge-primary { background: #1e3a8a; color: #3b82f6; }
    .badge-success { background: #064e3b; color: #10b981; }
    .badge-warning { background: #78350f; color: #f59e0b; }
    
    /* Line Break Divider styling */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 32px 0;
    }
    
    /* Text Helpers */
    .text-muted { color: var(--text-secondary) !important; font-size: 0.9rem; }
    .text-center { text-align: center; }
    .text-sm { font-size: 0.875rem; }
    
    /* Hero Display Section */
    .hero-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 32px;
        border: 1px solid var(--border);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 8px 0;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- MODEL LOADING LOGIC ---
@st.cache_resource
def load_housing_model():
    model_path = "house_model.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    else:
        class MockModel:
            def predict(self, df):
                base = 65000
                area_value = df["GrLivArea"].iloc[0] * 82
                qual_multiplier = 1 + (df["OverallQual"].iloc[0] * 0.15)
                age_penalty = df["HouseAge"].iloc[0] * 320
                return [(base + area_value) * qual_multiplier - age_penalty]
        return MockModel()

model = load_housing_model()

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.markdown("### 🎯 Quick Stats")
    st.divider()
    sidebar_placeholder = st.empty()

# --- HERO HEADER SECTION ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🏡 House Valuation Engine</div>
            <div class="hero-subtitle">AI-powered real estate valuation analysis</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("")

# --- MAIN CONTENT TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📝 Property Details", "💰 Valuation", "📊 Analysis", "ℹ️ About"])

# ============================================================================
# TAB 1: PROPERTY DETAILS
# ============================================================================
with tab1:
    st.markdown("<h3 style='margin-bottom: 20px;'>Property Information</h3>", unsafe_allow_html=True)
    
    # Create three organized sections
    tab1a, tab1b, tab1c = st.tabs(["📐 Size & Space", "🏗️ Structure", "📍 Location"])
    
    # --- TAB 1A: SIZE & SPACE ---
    with tab1a:
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("#### Living Area")
            gr_liv_area = st.number_input(
                "Above Ground Living Area",
                min_value=300,
                max_value=6000,
                value=1650,
                step=50,
                help="Main living space in square feet"
            )
            st.caption("sq ft")
        
        with col2:
            st.markdown("#### Basement")
            total_bsmt_sf = st.number_input(
                "Total Basement Area",
                min_value=0,
                max_value=4000,
                value=950,
                step=50,
                help="Finished and unfinished basement space"
            )
            st.caption("sq ft")
        
        with col3:
            st.markdown("#### Lot Size")
            lot_area = st.number_input(
                "Total Lot Area",
                min_value=500,
                max_value=100000,
                value=9450,
                step=250,
                help="Total land size of the property"
            )
            st.caption("sq ft")
        
        st.divider()
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            lot_frontage = st.number_input(
                "Lot Frontage",
                min_value=0,
                max_value=300,
                value=75,
                step=5,
                help="Street frontage length"
            )
            st.caption("linear ft")
        
        with col2:
            full_bath = st.selectbox("Full Bathrooms", [0, 1, 2, 3, 4], index=2)
        
        with col3:
            half_bath = st.selectbox("Half Bathrooms", [0, 1, 2], index=1)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            bedroom = st.slider("Bedrooms (Above Grade)", 0, 6, 3)
        
        with col2:
            kitchen = st.slider("Kitchens", 0, 3, 1)
    
    # --- TAB 1B: STRUCTURE ---
    with tab1b:
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("#### Construction Timeline")
            year_built = st.number_input(
                "Year Built",
                min_value=1800,
                max_value=2026,
                value=2002,
                step=1
            )
        
        with col2:
            year_remod = st.number_input(
                "Year Remodeled",
                min_value=1800,
                max_value=2026,
                value=2010,
                step=1
            )
        
        with col3:
            st.markdown("#### Quality & Condition")
            overall_qual = st.slider(
                "Overall Material Quality",
                1, 10, 7,
                help="1 = Poor, 10 = Excellent"
            )
        
        st.divider()
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            overall_cond = st.slider(
                "Current Condition",
                1, 10, 5,
                help="1 = Poor, 10 = Excellent"
            )
        
        with col2:
            st.markdown("#### Garage")
            garage_cars = st.selectbox("Garage Capacity", [0, 1, 2, 3, 4], index=2)
        
        with col3:
            garage_area = st.number_input(
                "Garage Size",
                min_value=0,
                max_value=1500,
                value=510,
                step=10,
                help="sq ft"
            )
    
    # --- TAB 1C: LOCATION ---
    with tab1c:
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("#### Zoning & Neighborhood")
            neighborhood = st.selectbox(
                "Neighborhood",
                NEIGHBORHOODS,
                index=4,
                help="Select the neighborhood zone"
            )
            ms_zoning = st.selectbox(
                "Zoning Classification",
                MS_ZONING,
                index=2
            )
        
        with col2:
            st.markdown("#### Property Type")
            house_style = st.selectbox(
                "House Style",
                HOUSE_STYLE,
                index=1
            )
            garage_type = st.selectbox(
                "Garage Type",
                GARAGE_TYPE,
                index=0
            )
        
        st.divider()
        
        st.markdown("#### Sale Timing")
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            mo_sold = st.slider("Month Sold", 1, 12, 5)
            months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            st.caption(f"📅 {months[mo_sold]}")
        
        with col2:
            yr_sold = st.slider("Year Sold", 2006, 2026, 2025)

# ============================================================================
# TAB 2: VALUATION
# ============================================================================
with tab2:
    st.markdown("<h3 style='margin-bottom: 20px;'>Price Prediction</h3>", unsafe_allow_html=True)
    
    # Build input data
    input_data = {feat: 0.0 for feat in FEATURE_NAMES}
    
    # Raw UI inputs injection
    input_data["MSSubClass"] = 20
    input_data["LotFrontage"] = float(lot_frontage)
    input_data["LotArea"] = float(lot_area)
    input_data["OverallQual"] = int(overall_qual)
    input_data["OverallCond"] = int(overall_cond)
    input_data["YearBuilt"] = int(year_built)
    input_data["YearRemodAdd"] = int(year_remod)
    input_data["TotalBsmtSF"] = float(total_bsmt_sf)
    input_data["GrLivArea"] = float(gr_liv_area)
    input_data["FullBath"] = int(full_bath)
    input_data["HalfBath"] = int(half_bath)
    input_data["BedroomAbvGr"] = int(bedroom)
    input_data["KitchenAbvGr"] = int(kitchen)
    input_data["GarageCars"] = int(garage_cars)
    input_data["GarageArea"] = float(garage_area)
    input_data["MoSold"] = int(mo_sold)
    input_data["YrSold"] = int(yr_sold)
    input_data["ExterQual"] = 3
    input_data["KitchenQual"] = 3
    
    # Feature engineering
    house_age = max(0, int(yr_sold - year_built))
    remod_age = max(0, int(yr_sold - year_remod))
    total_baths = float(full_bath + (0.5 * half_bath))
    total_liv_area = float(gr_liv_area + total_bsmt_sf)
    
    input_data["HouseAge"] = house_age
    input_data["RemodelAge"] = remod_age
    input_data["TotalBathrooms"] = total_baths
    input_data["TotalLivingArea"] = total_liv_area
    input_data["HasGarage"] = 1 if garage_cars > 0 else 0
    input_data["HasBasement"] = 1 if total_bsmt_sf > 0 else 0
    
    # Encode categorical variables
    if f"Neighborhood_{neighborhood}" in input_data:
        input_data[f"Neighborhood_{neighborhood}"] = 1
    if f"MSZoning_{ms_zoning}" in input_data:
        input_data[f"MSZoning_{ms_zoning}"] = 1
    if f"HouseStyle_{house_style}" in input_data:
        input_data[f"HouseStyle_{house_style}"] = 1
    if f"GarageType_{garage_type}" in input_data:
        input_data[f"GarageType_{garage_type}"] = 1
    
    # Create dataframe
    input_df = pd.DataFrame([input_data])[FEATURE_NAMES]
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_btn = st.button("🚀 Calculate Valuation", use_container_width=True)
    
    if predict_btn:
        with st.spinner("Analyzing property data..."):
            raw_prediction = model.predict(input_df)
            
            if isinstance(raw_prediction, pd.Series):
                predicted_price = float(raw_prediction.iloc[0])
            elif isinstance(raw_prediction, (np.ndarray, list)):
                predicted_price = float(raw_prediction[0])
            else:
                predicted_price = float(raw_prediction)
            
            predicted_price = max(10000.0, predicted_price)
            
            # Currency conversions
            predicted_price_pkr = predicted_price * USD_TO_PKR
            price_per_sqft_usd = predicted_price / total_liv_area if total_liv_area > 0 else 0
            price_per_sqft_pkr = predicted_price_pkr / total_liv_area if total_liv_area > 0 else 0
            
            # Update sidebar (Showing both USD and PKR)
            with sidebar_placeholder.container():
                st.metric("💰 Estimated Price (USD)", f"${predicted_price:,.0f}")
                st.metric("🇵🇰 Estimated Price (PKR)", f"₨ {predicted_price_pkr:,.0f}")
                st.metric("📊 Price / SqFt (PKR)", f"₨ {price_per_sqft_pkr:,.2f}")
                st.metric("📏 Total Area", f"{total_liv_area:,.0f} sq ft")
            
            # Display results
            st.success("Valuation complete!")
            st.divider()
            
            # Metrics rows split up cleanly
            st.markdown("#### Real-Time Metric Valuation Dashboard")
            m_col1, m_col2 = st.columns(2, gap="large")
            with m_col1:
                st.metric(
                    "Estimated Market Value (USD)",
                    f"${predicted_price:,.0f}",
                    delta=f"Quality: {overall_qual}/10"
                )
            with m_col2:
                st.metric(
                    "Estimated Market Value (PKR)",
                    f"₨ {predicted_price_pkr:,.0f}",
                    delta=f"Exchange Rate: 1$ = {USD_TO_PKR} Rs"
                )
                
            st.divider()
            
            unit_col1, unit_col2, unit_col3 = st.columns(3, gap="large")
            with unit_col1:
                st.metric("Price per SqFt (USD)", f"${price_per_sqft_usd:,.2f}", delta="USD Rate")
            with unit_col2:
                st.metric("Price per SqFt (PKR)", f"₨ {price_per_sqft_pkr:,.2f}", delta="PKR Rate")
            with unit_col3:
                age_category = "New" if house_age < 5 else ("Modern" if house_age < 20 else "Mature")
                st.metric("Property Age", f"{house_age} years", delta=age_category)
            
            st.divider()
            
            # Value breakdown visualization
            st.markdown("<h4 style='margin-top: 24px;'>Value Composition</h4>", unsafe_allow_html=True)
            
            # Create pie chart for value breakdown
            breakdown_labels = ['Living Area', 'Basement', 'Garage', 'Age & Condition', 'Location']
            breakdown_values = [
                gr_liv_area * price_per_sqft_usd * 0.5,
                total_bsmt_sf * price_per_sqft_usd * 0.2,
                garage_area * 15,
                predicted_price * 0.15,
                predicted_price * 0.15
            ]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=breakdown_labels,
                values=breakdown_values,
                marker=dict(colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'])
            )])
            fig_pie.update_layout(
                height=350,
                showlegend=True,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    else:
        st.info("👆 Fill in the property details in the **Property Details** tab, then click **Calculate Valuation** to see the estimated price.")

# ============================================================================
# TAB 3: ANALYSIS
# ============================================================================
with tab3:
    st.markdown("<h3 style='margin-bottom: 20px;'>Property Analysis</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### Key Property Metrics")
        metrics_data = {
            "Total Living Area": f"{total_liv_area:,.0f} sq ft",
            "House Age": f"{house_age} years",
            "Total Bathrooms": f"{total_baths}",
            "Bedrooms": f"{bedroom}",
            "Garage Spaces": f"{garage_cars}",
            "Overall Quality": f"{overall_qual}/10"
        }
        
        for label, value in metrics_data.items():
            st.write(f"**{label}:** {value}")
    
    with col2:
        st.markdown("#### Property Features")
        
        features = []
        if total_bsmt_sf > 0:
            features.append(f"✓ Basement ({total_bsmt_sf:,} sq ft)")
        if garage_cars > 0:
            features.append(f"✓ Garage ({garage_cars} cars)")
        if year_remod > year_built:
            features.append(f"✓ Remodeled ({year_remod})")
        if overall_qual >= 8:
            features.append("✓ Premium Quality")
        if overall_cond >= 7:
            features.append("✓ Excellent Condition")
        
        if features:
            for feature in features:
                st.write(feature)
        else:
            st.write("Basic property features")
    
    st.divider()
    
    # Feature comparison radar chart
    st.markdown("#### Property Profile Comparison")
    
    categories = ['Living Area', 'Quality', 'Condition', 'Garage', 'Bathrooms', 'Age']
    
    # Normalize values to 0-10 scale
    values = [
        min(10, (total_liv_area / 1000)),  # Normalize to 10 = 10,000 sq ft
        overall_qual,
        overall_cond,
        min(10, garage_cars * 3),
        min(10, total_baths * 2),
        max(0, 10 - (house_age / 10))  # Newer = higher score
    ]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker=dict(color='rgba(59, 130, 246, 0.5)'),
        line=dict(color='#3b82f6', width=2)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor='#334155'),
            angularaxis=dict(gridcolor='#334155'),
            bgcolor='#0f172a'
        ),
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff')
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

# ============================================================================
# TAB 4: ABOUT
# ============================================================================
with tab4:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### About This Valuation Engine")
        
        st.markdown("""
        This AI-powered house valuation engine uses gradient boosting regression to estimate property values based on:
        
        **Key Features Analyzed:**
        - 📐 Property dimensions and living space
        - 🏗️ Building quality and condition
        - 📍 Location and neighborhood factors
        - 🏠 Structural features and amenities
        - ⏰ Age and renovation history
        
        **Model Capabilities:**
        - Analyzes 222+ engineered features
        - Provides dual currency valuation estimations (USD / PKR)
        - Compares properties across multiple dimensions
        - Delivers results in seconds
        
        **Accuracy Notes:**
        The valuation is an estimate based on historical data. For precise valuations, 
        consult with a professional real estate appraiser.
        """)
    
    with col2:
        st.markdown("### Quick Tips")
        st.info("""
        **For Best Results:**
        
        ✓ Provide accurate square footage
        ✓ Update recent renovations
        ✓ Include all amenities
        ✓ Verify property age
        ✓ Note garage/basement details
        """)

# --- FOOTER ---
st.divider()
st.markdown(
    "<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>"
    "Built with Streamlit & Machine Learning | Accurate property valuations powered by AI"
    "</p>",
    unsafe_allow_html=True
)