import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.pagesizes import letter
from datetime import datetime

# ---------------- PDF REPORT FUNCTION ----------------

def generate_pdf_report(
    stock,
    open_price,
    high_price,
    low_price,
    volume,
    prev_close,
    prediction,
    signal
):

    file_name = "stock_prediction_report.pdf"

    doc = SimpleDocTemplate(
        file_name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b>AI Stock Prediction Report</b>",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    report_text = f'''
    <b>Selected Stock:</b> {stock}<br/><br/>
    <b>Open Price:</b> ₹ {open_price}<br/><br/>
    <b>High Price:</b> ₹ {high_price}<br/><br/>
    <b>Low Price:</b> ₹ {low_price}<br/><br/>
    <b>Volume:</b> {volume}<br/><br/>
    <b>Previous Close:</b> ₹ {prev_close}<br/><br/>
    <b>Predicted Price:</b> ₹ {prediction:.2f}<br/><br/>
    <b>AI Signal:</b> {signal}
    '''

    paragraph = Paragraph(
        report_text,
        styles['BodyText']
    )

    elements.append(paragraph)

    elements.append(PageBreak())

    doc.build(elements)

    return file_name

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Stock Prediction Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------- STOCK SELECTOR --------
stock_symbol = st.sidebar.selectbox(

    
    "📌 Select Stock",
    [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "TATAMOTORS"
    ]
)

# ---------------- STOCK EXCHANGE ----------------

stock_exchange = {
    "RELIANCE": "NSE",
    "TCS": "NSE",
    "INFY": "NSE",
    "HDFCBANK": "NSE",
    "TATAMOTORS": "NSE"
}

selected_exchange = stock_exchange[stock_symbol]


# ---------------- LOAD MODEL ----------------
model = pickle.load(open("models/model.pkl", "rb"))

# Load stock dataset
df = pd.read_csv("data/raw/RELIANCE.csv")


# ---------------- LIVE STOCK DATA ----------------

API_KEY = "dbfb4c71ae8446508ed520cc8b939f7e"

symbol = stock_symbol

url = f"https://api.twelvedata.com/price?symbol={symbol}&exchange=NSE&apikey={API_KEY}"

response = requests.get(url)

data = response.json()

live_price = data.get("price")

# ---------------- MARKET STATUS ----------------

current_hour = datetime.now().hour
current_minute = datetime.now().minute

if (
    current_hour > 9 or
    (current_hour == 9 and current_minute >= 15)
) and (
    current_hour < 15 or
    (current_hour == 15 and current_minute <= 30)
):

    market_status = "ACTIVE"

else:

    market_status = "Closed"

# Moving Average
df["MA20"] = df["Close"].rolling(20).mean()

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>

    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .main {
        background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
    }

    .hero {
        padding: 35px;
        border-radius: 28px;
        background: linear-gradient(
            135deg,
            rgba(37,99,235,0.25),
            rgba(124,58,237,0.25)
        );
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 40px rgba(0,0,0,0.35);
        margin-bottom: 20px;
    }

    .title {
        font-size: 50px;
        font-weight: 500;
        color: black;
        text-align: center;
        letter-spacing: 1px;
    }

    .subtitle {
        text-align: center;
        color: #light blue;
        font-size: 22px;
        margin-top: 10px;
    }

    .metric-card {
        background: linear-gradient(
            135deg,
            #1d4ed8,
            #7c3aed,
            #ec4999
        );
        padding: 30px;
        border-radius: 22px;
        text-align: center;
        color: white;
        margin-top: 25px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.3);
    }

    .metric-price {
        font-size: 54px;
        font-weight: bold;
        margin-top: 10px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(to right,#2563eb,#7c3aed);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 14px;
        border-radius: 14px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(37,99,235,0.35);
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 30px rgba(124,58,237,0.4);
    }

    .stDownloadButton > button {

    width: 100%;
    background: transparent;
    color: #60a5fa;
    font-size: 18px;
    font-weight: bold;

    padding: 14px;

    border-radius: 14px;

    border: 2px solid #3b82f6;

    transition: all 0.3s ease;

    margin-top: 15px;
}

.stDownloadButton > button:hover {

    background: #2563eb;
    color: white;

    box-shadow: 0 0 20px rgba(59,130,246,0.5);

    transform: translateY(-2px);
}

    .sidebar .sidebar-content {
        background: #0f172a;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
#st.markdown("-")
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2784/2784487.png",
        width=120
    )

    st.title("📊 Dashboard")

    st.markdown("""
    ### Features
    - AI Stock Prediction
    - Machine Learning Model
    - Real-time Inputs
    - Professional Analytics UI
    - End-to-End ML Deployment
    """)


# ---------------- HERO SECTION ----------------

st.markdown(
    """
    <div class='hero'>
        <div class='title'>
            📈 AI Stock Analytics Platform
        </div>
        <div class='subtitle'>
            End-to-End ML Deployment & Stock Forecasting Dashboard
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- LIVE STOCK METRICS ----------------

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        label=f"📈 Live {stock_symbol} Price",
        value=f"₹ {live_price}"
    )

with metric2:
    st.metric(
        label=f"📊 {selected_exchange} Market",
        value=market_status
    )

with metric3:
    st.metric(
        label="🤖 AI Engine",
        value="Real-Time Analytics"
    )

# ---------------- MAIN LAYOUT ----------------
left_col, right_col = st.columns([1.1, 1])

# ---------------- INPUT PANEL ----------------
with left_col:

    st.subheader("📥 Market Input Parameters")

    open_price = st.number_input(
        "Open Price",
        min_value=0,
        step=1,
        help="Opening stock market price"
    )

    high_price = st.number_input(
        "High Price",
        min_value=0,
        step=1,
        help="Highest market price"
    )

    low_price = st.number_input(
        "Low Price",
        min_value=0,
        step=1,
        help="Lowest market price"
    )

    volume = st.number_input(
        "Trading Volume",
        min_value=0,
        step=1000,
        help="Total traded stock volume"
    )

    prev_close = st.number_input(
        "Previous Close",
        min_value=0,
        step=1,
        help="Previous day's closing price"
    )

    predict_button = st.button("🚀 Predict Market Price")
  

# ---------------- PREDICTION PANEL ----------------
with right_col:

    st.subheader("🤖 AI Prediction Engine")

    if predict_button:

        features = pd.DataFrame({
            "Open": [open_price],
            "High": [high_price],
            "Low": [low_price],
            "Volume": [volume],
            "Prev Close": [prev_close]
        })

        with st.spinner("Analyzing market data..."):
            prediction = model.predict(features)

        predicted_price = prediction[0]

        current_price = prev_close

        # AI Trading Signal
        if predicted_price > current_price:

            signal = "🟢 BUY SIGNAL"

        elif predicted_price < current_price:
            signal = "🔴 SELL SIGNAL"

        else:
            signal = "⚪ HOLD SIGNAL"

        # Generate PDF
        pdf_file = generate_pdf_report(
            stock_symbol,
            open_price,
            high_price,
            low_price,
            volume,
            prev_close,
            predicted_price,
            signal
        )

        # Download Button
        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download Prediction Report",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )

        st.success(
                f"Estimated Market Value: ₹ {prediction[0]:.2f}"
            )
        st.markdown(
            f"""
            <div style='
                background: rgba(255,255,255,0.08);
                padding:20px;
                border-radius:18px;
                text-align:center;
                margin-top:20px;
                border:1px solid rgba(255,255,255,0.1);
            '>
            <h2>{signal}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
                    f"""
                    <div class='metric-card'>
                        <h2>📊 Forecasted Stock Price</h2>
                        <div class='metric-price'>₹ {prediction[0]:.2f}</div>
                        <p>AI-powered estimated market closing price</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
    else:

        st.info("Enter stock market values to generate prediction")



st.markdown("## 📈 Live Stock Market Chart")

left_space, chart_col, right_space = st.columns([1, 6, 1])

with chart_col:

    st.components.v1.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol=NSE:{stock_symbol}&interval=D&theme=dark",
        height=500,
        scrolling=False
    )

