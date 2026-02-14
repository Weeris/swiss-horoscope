"""
Swiss Horoscope - Main Streamlit Application
Precision-powered horoscope using Swiss Ephemeris (pyswisseph)
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Dict, List
import matplotlib.pyplot as plt
from core.swiss_eph import SwissEphemerisCalculator
from core.chart_wheel import (
    create_chart_wheel, chart_to_image,
    get_current_transits, create_transit_overlay_chart,
    create_synastry_chart
)
from core.interactive_chart import create_interactive_chart_wheel
from core.birth_chart_reading import generate_birth_chart_reading
from core.fortune_reader import generate_detailed_daily_fortune, generate_monthly_outlook, generate_yearly_outlook


# ============== Page Config ==============
st.set_page_config(
    page_title="🔮 Swiss Horoscope",
    page_icon="🔮",
    layout="wide"
)


# ============== Custom CSS ==============
st.markdown("""
<style>
    /* Main theme - deep mystical purple */
    .stApp {
        background: linear-gradient(135deg, #0f0a1f 0%, #1a103c 50%, #0d1b2a 100%);
    }
    
    /* Card styling */
    .card {
        background: rgba(30, 27, 75, 0.6);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(147, 51, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Element color badges */
    .element-fire { 
        background: linear-gradient(135deg, #FF6B6B, #FF8E53); 
        color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold;
    }
    .element-earth { 
        background: linear-gradient(135deg, #4ECDC4, #44A08D); 
        color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold;
    }
    .element-air { 
        background: linear-gradient(135deg, #FFE66D, #F7DC6F); 
        color: #1a103c; padding: 4px 12px; border-radius: 20px; font-weight: bold;
    }
    .element-water { 
        background: linear-gradient(135deg, #74B9FF, #0984E3); 
        color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold;
    }
    
    /* Planet tooltips */
    .planet-info {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #9333ea;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }
    
    /* Animated stars background */
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(147, 51, 234, 0.2);
        border-top: 4px solid #9333ea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: #a78bfa;
        margin-top: 16px;
        font-size: 16px;
    }
    
    /* Glowing buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #9333ea);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(147, 51, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(147, 51, 234, 0.6);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 27, 75, 0.5);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: 1px solid rgba(147, 51, 234, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed, #9333ea);
        border: none;
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 27, 75, 0.5);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(147, 51, 234, 0.2);
    }
    
    /* Hide default header */
    header {visibility: hidden;}
    
    /* Custom title styling */
    .main-title {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #c084fc, #9333ea, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #a78bfa;
        font-size: 1.1rem;
    }
    
    /* Chart container hover effect */
    .chart-container:hover {
        transform: scale(1.02);
        transition: transform 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)


# ============== Language Support ==============
LANG = {
    "en": {
        "title": "🔮 Swiss Horoscope",
        "subtitle": "Precision Astrology with Swiss Ephemeris",
        "tab_input": "📋 Input",
        "tab_chart": "⭐ Birth Chart",
        "tab_prediction": "🔮 Prediction",
        "birth_info": "Birth Information",
        "birth_date": "Date of Birth",
        "birth_time": "Time of Birth",
        "hour": "Hour",
        "minute": "Minute",
        "location": "Birth Location",
        "select_city": "Select City",
        "calculate": "Calculate Birth Chart",
        "your_chart": "Your Birth Chart",
        "sun_sign": "Sun Sign",
        "planets": "Planetary Positions",
        "ascendant": "Rising Sign",
        "midheaven": "Midheaven",
        "houses": "House Cusps",
        "aspects": "Aspects",
        "sign": "Sign",
        "degree": "Degree",
        "house": "House",
        "retrograde": "Retrograde",
        "enter_birth": "Enter your birth details to see your chart",
        "elements": "Elements",
        "chart_viz": "Chart Summary",
        "daily_prediction": "Daily Prediction",
        "weekly_prediction": "Weekly Forecast",
        "birth_chart_reading": "Birth Chart Reading",
        "your_destiny": "Your Destiny",
        "sun_sign_reading": "Sun Sign Reading",
        "moon_sign_reading": "Moon Sign Reading",
        "rising_sign_reading": "Rising Sign Reading",
        "planetary_emphasis": "Planetary Emphasis",
        "life_themes": "Life Themes",
        "key_aspects": "Key Aspects",
        "life_theme": "Your Life Theme",
        "strengths": "Strengths",
        "challenges": "Challenges",
        "core_identity": "Core Identity",
        "element_dominant": "Element Dominant",
        "daily_fortune": "Daily Fortune",
        "monthly_outlook": "Monthly Outlook",
        "yearly_outlook": "Yearly Outlook",
        "today_overview": "Today's Overview",
        "key_transits": "Key Transits",
        "transit_aspects": "Transit Aspects",
        "lucky_elements": "Lucky Elements",
        "color": "Color",
        "number": "Number",
        "lucky_day": "Lucky Day",
        "month_theme": "Monthly Theme",
        "highlights": "Highlights",
        "advice": "Advice",
        "major_transits": "Major Transits",
        "quarters": "Quarterly Overview",
        "tab_transit": "🚀 Transits",
        "tab_synastry": "💕 Synastry",
        "chart_wheel": "Chart Wheel",
        "show_houses": "Show Houses",
        "show_aspects": "Show Aspects",
        "transit_overlay": "Transit Overlay",
        "current_transits": "Current Transits",
        "synastry": "Synastry Chart",
        "person1": "Person 1",
        "person2": "Person 2",
        "enter_person2": "Enter second person's birth details",
        "compare": "Compare Charts",
        # New keys for prediction sub-tabs
        "tab_sun": "☀️ Sun Sign",
        "tab_moon": "🌙 Moon Sign",
        "tab_rising": "↑ Rising Sign",
        "tab_planetary": "🪐 Planetary",
        # Synastry
        "element_compatibility": "Element Compatibility",
        "sign_compatibility": "Sign Compatibility",
        "compatibility_percentage": "Compatibility %",
        "love_potential": "Love Potential",
        "strong_match": "Strong Match",
        "balanced_match": "Balanced",
        "challenging_match": "Challenging",
        # Birth Chart UI
        "element_dist": "Element Distribution",
        "quick_summary": "Quick Summary",
        "chart_details": "Chart Details",
    },
    "th": {
        "title": "🔮 ดวงชะตาสวิส",
        "subtitle": "โหราศาสตร์แม่นยำสูงด้วย Swiss Ephemeris",
        "tab_input": "📋 ข้อมูล",
        "tab_chart": "⭐ ดวงชะตา",
        "tab_prediction": "🔮 คำทำนาย",
        "birth_info": "ข้อมูลการเกิด",
        "birth_date": "วันเกิด",
        "birth_time": "เวลาเกิด",
        "hour": "ชั่วโมง",
        "minute": "นาที",
        "location": "สถานที่เกิด",
        "select_city": "เลือกเมือง",
        "calculate": "คำนวณดวงชะตา",
        "your_chart": "ดวงชะตาของคุณ",
        "sun_sign": "ราศีเกิด",
        "planets": "ตำแหน่งดาวเคราห์",
        "ascendant": "ราศีขึ้น",
        "midheaven": "มิดฮีเวน",
        "houses": "ตำแหน่งเรือน",
        "aspects": "มุมระหว่างดาว",
        "sign": "ราศี",
        "degree": "องศา",
        "house": "เรือน",
        "retrograde": "ถอยหลัง",
        "enter_birth": "กรอกข้อมูลวันเกิดของคุณเพื่อดูดวงชะตา",
        "elements": "ธาตุ",
        "chart_viz": "สรุปดวงชะตา",
        "daily_prediction": "คำทำนายประจำวัน",
        "weekly_prediction": "คำทำนายประจำสัปดาห์",
        "birth_chart_reading": "การอ่านดวงชะตา",
        "your_destiny": "โชคชะตาของคุณ",
        "sun_sign_reading": "การอ่านราศีเกิด",
        "moon_sign_reading": "การอ่านดวงจันทร์",
        "rising_sign_reading": "การอ่านราศีขึ้น",
        "planetary_emphasis": "ดาวเคราห์ที่โดดเด่น",
        "life_themes": "ธีมชีวิต",
        "key_aspects": "มุมสำคัญ",
        "life_theme": "ธีมชีวิตของคุณ",
        "strengths": "จุดแข็ง",
        "challenges": "ความท้าทาย",
        "core_identity": "ตัวตนหลัก",
        "element_dominant": "ธาตุที่โดดเด่น",
        "daily_fortune": "ดวงประจำวัน",
        "monthly_outlook": "ดวงประจำเดือน",
        "yearly_outlook": "ดวงประจำปี",
        "today_overview": "ภาพรวมวันนี้",
        "key_transits": "ดาวเคราะห์สำคัญ",
        "transit_aspects": "มุมดาวปัจจุบัน",
        "lucky_elements": "องศาดี",
        "color": "สี",
        "number": "ตัวเลข",
        "lucky_day": "วันดี",
        "month_theme": "ธีมประจำเดือน",
        "highlights": "ไฮไลท์",
        "advice": "คำแนะนำ",
        "major_transits": "ดาวเคราะห์หลัก",
        "quarters": "ภาพรวมไตรมาส",
        "tab_transit": "🚀 ดาวเคราะห์ปัจจุบัน",
        "tab_synastry": "💕 ดวงคู่",
        "chart_wheel": "แผนภูมิดวงชะตา",
        "show_houses": "แสดงเรือน",
        "show_aspects": "แสดงมุมดาว",
        "transit_overlay": "ซ้อนดวงปัจจุบัน",
        "current_transits": "ดาวเคราะห์ปัจจุบัน",
        "synastry": "ดวงคู่เปรียบเทียบ",
        "person1": "คนที่ 1",
        "person2": "คนที่ 2",
        "enter_person2": "กรอกข้อมูลวันเกิดคนที่ 2",
        "compare": "เปรียบเทียบดวง",
        # New keys for prediction sub-tabs
        "tab_sun": "☀️ ราศีเกิด",
        "tab_moon": "🌙 ดวงจันทร์",
        "tab_rising": "↑ ราศีขึ้น",
        "tab_planetary": "🪐 ดาวเคราะห์",
        # Synastry
        "element_compatibility": "ความเข้ากันได้ของธาตุ",
        "sign_compatibility": "ความเข้ากันได้ของราศี",
        "compatibility_percentage": "เปอร์เซ็นต์ความเข้ากัน",
        "love_potential": "โอกาสความรัก",
        "strong_match": "เข้ากันดี",
        "balanced_match": "สมดุล",
        "challenging_match": "ท้าทาย",
        # Birth Chart UI
        "element_dist": "การกระจายตัวของธาตุ",
        "quick_summary": "สรุปโดยย่อ",
        "chart_details": "รายละเอียดดวงชะตา",
    }
}

# Cities with coordinates and timezone
CITIES = {
    "Bangkok, Thailand": {"lat": 13.7563, "lng": 100.5018, "tz": "Asia/Bangkok"},
    "Hong Kong": {"lat": 22.3193, "lng": 114.1694, "tz": "Asia/Hong_Kong"},
    "London, UK": {"lat": 51.5074, "lng": -0.1278, "tz": "Europe/London"},
    "New York, USA": {"lat": 40.7128, "lng": -74.0060, "tz": "America/New_York"},
    "Tokyo, Japan": {"lat": 35.6762, "lng": 139.6503, "tz": "Asia/Tokyo"},
    "Los Angeles, USA": {"lat": 34.0522, "lng": -118.2437, "tz": "America/Los_Angeles"},
    "Singapore": {"lat": 1.3521, "lng": 103.8198, "tz": "Asia/Singapore"},
    "Shanghai, China": {"lat": 31.2304, "lng": 121.4737, "tz": "Asia/Shanghai"},
    "Sydney, Australia": {"lat": -33.8688, "lng": 151.2093, "tz": "Australia/Sydney"},
    "Dubai, UAE": {"lat": 25.2048, "lng": 55.2708, "tz": "Asia/Dubai"},
}

# Western zodiac signs
WESTERN_SIGNS = {
    "Aries": {"element": "Fire", "quality": "Cardinal", "ruler": "Mars", "traits_en": "Bold, energetic, pioneering", "traits_th": "กล้าหาญ, มีพลัง, นำทัพ"},
    "Taurus": {"element": "Earth", "quality": "Fixed", "ruler": "Venus", "traits_en": "Patient, reliable, practical", "traits_th": "อดทน, ซื่อสัตย์, จริงจัง"},
    "Gemini": {"element": "Air", "quality": "Mutable", "ruler": "Mercury", "traits_en": "Curious, adaptable, communicative", "traits_th": "อยากรู้, ปรับตัวเก่ง, สื่อสารเก่ง"},
    "Cancer": {"element": "Water", "quality": "Cardinal", "ruler": "Moon", "traits_en": "Intuitive, emotional, protective", "traits_th": "มีสัญญาณที่ 6, อารมณ์อ่อนไหว, พร้อมปกป้อง"},
    "Leo": {"element": "Fire", "quality": "Fixed", "ruler": "Sun", "traits_en": "Confident, creative, generous", "traits_th": "มั่นใจ, สร้างสรรค์, ใจกว้าง"},
    "Virgo": {"element": "Earth", "quality": "Mutable", "ruler": "Mercury", "traits_en": "Analytical, practical, helpful", "traits_th": "วิเคราะห์, ช่างเหมาะ, ช่วยเหลือ"},
    "Libra": {"element": "Air", "quality": "Cardinal", "ruler": "Venus", "traits_en": "Diplomatic, fair, social", "traits_th": "สร้างสมดุล, ยุติธรรม, เข้ากับคน"},
    "Scorpio": {"element": "Water", "quality": "Fixed", "ruler": "Pluto", "traits_en": "Passionate, mysterious, determined", "traits_th": "หลงใหล, ลึกลับ, มุ่งมั่น"},
    "Sagittarius": {"element": "Fire", "quality": "Mutable", "ruler": "Jupiter", "traits_en": "Optimistic, adventurous, honest", "traits_th": "มองโลกในแง่ดี, ชอบผจญภัย, ซื่อสัตย์"},
    "Capricorn": {"element": "Earth", "quality": "Cardinal", "ruler": "Saturn", "traits_en": "Ambitious, disciplined, patient", "traits_th": "มีความทะเยอทะยาน, มีระเบียบ, อดทน"},
    "Aquarius": {"element": "Air", "quality": "Fixed", "ruler": "Uranus", "traits_en": "Independent, original, humanitarian", "traits_th": "เป็นตัวของตัวเอง, สร้างสรรค์, มีน้ำใจ"},
    "Pisces": {"element": "Water", "quality": "Mutable", "ruler": "Neptune", "traits_en": "Compassionate, artistic, intuitive", "traits_th": "เมตตา, มีศิลปะ, มีสัญชาตญาณ"},
}

# Element signs mapping for compatibility
ELEMENT_SIGNS = {
    "fire": ["Aries", "Leo", "Sagittarius"],
    "earth": ["Taurus", "Virgo", "Capricorn"],
    "air": ["Gemini", "Libra", "Aquarius"],
    "water": ["Cancer", "Scorpio", "Pisces"],
}

ELEMENTS = {
    "Fire": {"color": "🔴", "traits_en": "Energetic, passionate, impulsive", "traits_th": "มีพลัง, หลงใหล, กระตือรือร้น"},
    "Earth": {"color": "🟤", "traits_en": "Practical, stable, grounded", "traits_th": "จริงจัง, มั่นคง, หนักแน่น"},
    "Air": {"color": "💨", "traits_en": "Intellectual, social, flexible", "traits_th": "ฉลาด, เข้าสังคม, ยืดหยุ่น"},
    "Water": {"color": "💧", "traits_en": "Emotional, intuitive, compassionate", "traits_th": "อารมณ์, มีสัญชาตญาณ, เมตตา"},
}

# Thai day planets (Mahadara)
THAI_DAY_PLANETS = {
    0: {"planet": "Sun", "thai": "อาทิตย์", "color": "แดง", "day_en": "Sunday", "day_th": "วันอาทิตย์"},
    1: {"planet": "Moon", "thai": "จันทร์", "color": "ขาว", "day_en": "Monday", "day_th": "วันจันทร์"},
    2: {"planet": "Mars", "thai": "อังคาร", "color": "แดง", "day_en": "Tuesday", "day_th": "วันอังคาร"},
    3: {"planet": "Mercury", "thai": "พุธ", "color": "เขียว", "day_en": "Wednesday", "day_th": "วันพุธ"},
    4: {"planet": "Jupiter", "thai": "พฤหัส", "color": "เหลือง", "day_en": "Thursday", "day_th": "วันพฤหัสบดี"},
    5: {"planet": "Venus", "thai": "ศุกร์", "color": "ขาว", "day_en": "Friday", "day_th": "วันศุกร์"},
    6: {"planet": "Saturn", "thai": "เสาร์", "color": "ดำ", "day_en": "Saturday", "day_th": "วันเสาร์"},
}

# Chinese zodiac
CHINESE_ZODIAC = {
    0: {"animal_en": "Rat", "animal_th": "หนู", "element_en": "Wood", "element_th": "ไม้"},
    1: {"animal_en": "Ox", "animal_th": "วัว", "element_en": "Wood", "element_th": "ไม้"},
    2: {"animal_en": "Tiger", "animal_th": "เสือ", "element_en": "Fire", "element_th": "ไฟ"},
    3: {"animal_en": "Rabbit", "animal_th": "กระต่าย", "element_en": "Fire", "element_th": "ไฟ"},
    4: {"animal_en": "Dragon", "animal_th": "มังกร", "element_en": "Earth", "element_th": "ดิน"},
    5: {"animal_en": "Snake", "animal_th": "งู", "element_en": "Earth", "element_th": "ดิน"},
    6: {"animal_en": "Horse", "animal_th": "ม้า", "element_en": "Metal", "element_th": "ทอง"},
    7: {"animal_en": "Goat", "animal_th": "แพะ", "element_en": "Metal", "element_th": "ทอง"},
    8: {"animal_en": "Monkey", "animal_th": "ลิง", "element_en": "Metal", "element_th": "ทอง"},
    9: {"animal_en": "Rooster", "animal_th": "ไก่", "element_en": "Metal", "element_th": "ทอง"},
    10: {"animal_en": "Dog", "animal_th": "สุนัข", "element_en": "Earth", "element_th": "ดิน"},
    11: {"animal_en": "Pig", "animal_th": "หมู", "element_en": "Earth", "element_th": "ดิน"},
}


def get_lang(lang_code: str = "en") -> dict:
    """Get language dictionary"""
    return LANG.get(lang_code, LANG["en"])


# ============== UI Functions ==============
def render_header(lang: dict):
    """Render page header"""
    st.title(lang["title"])
    st.markdown(f"*{lang['subtitle']}*")


def render_birth_input(lang: dict, key_prefix: str = "") -> Optional[Dict]:
    """Render birth information input form"""
    st.subheader(lang["birth_info"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        birth_date = st.date_input(
            lang["birth_date"],
            value=datetime(1990, 1, 1),
            key=f"{key_prefix}date"
        )
    
    with col2:
        hour = st.number_input(lang["hour"], 0, 23, 12, key=f"{key_prefix}hour")
        minute = st.number_input(lang["minute"], 0, 59, 0, key=f"{key_prefix}minute")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_city = st.selectbox(
            lang["location"],
            options=list(CITIES.keys()),
            key=f"{key_prefix}city"
        )
    
    city_data = CITIES[selected_city]
    
    with col2:
        st.text_input("Timezone", value=city_data["tz"], disabled=True, key=f"{key_prefix}tz")
    
    return {
        "year": birth_date.year,
        "month": birth_date.month,
        "day": birth_date.day,
        "hour": hour,
        "minute": minute,
        "latitude": city_data["lat"],
        "longitude": city_data["lng"],
        "timezone": city_data["tz"]
    }


def render_birth_chart(result: Dict, lang: dict):
    """Render birth chart section with improved UI"""
    st.subheader(lang["your_chart"])
    
    # Date/time
    st.markdown(f"**{result['subject']['date_time']}** | {result['subject']['timezone']}")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Sun sign
    sun = result['planets']['Sun']
    with col1:
        st.metric(f"☀️ {lang['sun_sign']}", f"{sun['sign']}", f"{sun['degree']:.1f}°")
    
    # Moon sign (new)
    moon = result['planets'].get('Moon', {})
    with col2:
        st.metric(f"🌙 Moon Sign", f"{moon.get('sign', '-')}", f"{moon.get('degree', 0):.1f}°" if moon.get('degree') else None)
    
    # Ascendant
    asc = result["ascendant"]
    with col3:
        st.metric(f"↑ {lang['ascendant']}", f"{asc['sign']}", f"{asc['degree']:.1f}°")
    
    # Midheaven
    mc = result["midheaven"]
    with col4:
        st.metric(f"☰ {lang['midheaven']}", f"{mc['sign']}", f"{mc['degree']:.1f}°")
    
    # Element distribution
    st.markdown("---")
    elements = calculate_elements(result["planets"])
    
    # Visual element distribution with bar chart
    st.subheader(lang.get("element_dist", "Element Distribution"))
    
    # Create data for bar chart
    elem_data = {"Elements": [elements["Fire"], elements["Earth"], elements["Air"], elements["Water"]]}
    elem_df = {"Fire 🔥": elements["Fire"], "Earth 🌍": elements["Earth"], "Air 💨": elements["Air"], "Water 💧": elements["Water"]}
    
    # Display as metrics first
    cols = st.columns(4)
    for i, (elem, count) in enumerate(elements.items()):
        emoji = ELEMENTS[elem]["color"]
        with cols[i]:
            st.metric(f"{emoji} {elem}", f"{count}/10")
    
    # Show bar chart below
    import pandas as pd
    elem_df = pd.DataFrame({
        "Element": ["Fire 🔥", "Earth 🌍", "Air 💨", "Water 💧"],
        "Count": [elements["Fire"], elements["Earth"], elements["Air"], elements["Water"]]
    }).set_index("Element")
    st.bar_chart(elem_df)
    
    # Quick summary
    dominant_element = max(elements, key=elements.get)
    dominant_count = elements[dominant_element]
    st.info(f"✨ **{lang.get('quick_summary', 'Quick Summary')}**: Your dominant element is **{dominant_element}** ({dominant_count}/10 planets)")


def render_planets(planets: Dict, lang: dict):
    """Render planetary positions"""
    st.subheader(lang["planets"])
    
    planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", 
                    "Saturn", "Uranus", "Neptune", "Pluto", "North Node", "South Node"]
    
    cols = st.columns(3)
    
    for i, planet in enumerate(planet_order):
        if planet in planets:
            p = planets[planet]
            with cols[i % 3]:
                retro = " (R)" if p.get("retrograde") else ""
                st.metric(f"{planet}", f"{p['sign']} {p['degree']:.1f}°{retro}")


def render_houses(houses: Dict, lang: dict):
    """Render house cusps"""
    st.subheader(lang["houses"])
    
    cols = st.columns(4)
    for i, (house_num, house_data) in enumerate(sorted(houses.items())):
        with cols[i % 4]:
            st.metric(f"House {house_num}", f"{house_data['sign']} {house_data['degree']:.1f}°")


def render_aspects(aspects: List[Dict], lang: dict):
    """Render aspects"""
    st.subheader(lang["aspects"])
    
    aspect_emojis = {
        "CONJUNCTION": "☌", "OPPOSITION": "☍", "SQUARE": "□",
        "TRINE": "△", "SEXTILE": "⚹"
    }
    
    if not aspects:
        st.info("No major aspects detected")
        return
    
    for aspect in aspects[:15]:  # Limit to 15
        emoji = aspect_emojis.get(aspect["type"], "●")
        orb = "★" if aspect["exact"] else ""
        st.markdown(f"**{emoji} {aspect['p1']}** — **{aspect['p2']}** ({aspect['type']}{orb})")


def calculate_elements(planets: Dict) -> Dict:
    """Calculate element distribution"""
    elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
    
    planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", 
                    "Saturn", "Uranus", "Neptune", "Pluto"]
    
    for planet in planet_order:
        if planet in planets:
            sign = planets[planet]["sign"]
            if sign in WESTERN_SIGNS:
                elem = WESTERN_SIGNS[sign]["element"]
                elements[elem] += 1
    
    return elements


def get_chinese_zodiac(year: int) -> Dict:
    """Get Chinese zodiac for year"""
    cycle_year = (year - 4) % 12
    return CHINESE_ZODIAC[cycle_year]




def render_thai_prediction(year: int, month: int, day: int, planets: Dict, lang: dict):
    """Render Thai-style prediction"""
    # Thai day planet
    birth_date = datetime(year, month, day)
    weekday = birth_date.weekday()
    day_planet = THAI_DAY_PLANETS.get(weekday, THAI_DAY_PLANETS[0])
    
    # Chinese zodiac
    chinese = get_chinese_zodiac(year)
    
    # Moon sign (Thai astrology uses Moon)
    moon_sign = planets.get("Moon", {}).get("sign", "Aries")
    
    # Get Thai name for western sign
    sign_map_th = {
        "Aries": "เมษะ", "Taurus": "พฤษภะ", "Gemini": "มิถุนะ", "Cancer": "กรกฏะ",
        "Leo": "สิงหะ", "Virgo": "กันยะ", "Libra": "ตุลยะ", "Scorpio": "พิจิกะ",
        "Sagittarius": "ธนุ", "Capricorn": "มู่คัส", "Aquarius": "วัวป่า", "Pisces": "มีนะ"
    }
    
    moon_sign_th = sign_map_th.get(moon_sign, moon_sign)
    
    st.markdown(f"""
### 🇹🇭 {lang.get('thai_style', 'Thai Style Prediction')}

**🌅 วันเกิด:** {day_planet['day_th']} (ดาว{day_planet['thai']})
- **สี:** {day_planet['color']}
- **ดาวประจำวัน:** {day_planet['planet']}

**🐀 จีนสิงโต:** {chinese['animal_th']} ({chinese['element_th']})

**🌙 ดาวจันทร์ (Chandra):** {moon_sign_th}

**🧡 คำแนะนำ:**
- **{day_planet['color']}** {lang.get('lucky_color', 'is your lucky color today')}
- **{day_planet['planet']}** {lang.get('influence_planet', 'energy is strong')}
""")


def render_prediction_section(result: Dict, birth_data: Dict, lang: dict, lang_code: str):
    """Render prediction tab with sub-tabs"""
    planets = result["planets"]
    asc = result["ascendant"]
    houses = result.get("houses", {})
    aspects = result.get("aspects", [])
    year = birth_data["year"]
    month = birth_data["month"]
    day = birth_data["day"]
    
    # Create prediction sub-tabs - Daily/Weekly/Monthly/Yearly
    pred_tabs = st.tabs([
        "📅 " + lang.get("daily_fortune", "Daily"),
        "📆 " + lang.get("monthly_outlook", "Monthly"),
        "📊 " + lang.get("yearly_outlook", "Yearly"),
    ])
    
    # ===== TAB 1: DAILY FORTUNE =====
    with pred_tabs[0]:
        st.subheader("📅 " + lang.get("daily_fortune", "Daily Fortune"))
        
        with st.spinner("Reading your daily fortune..."):
            # Use detailed fortune generator
            fortune = generate_detailed_daily_fortune(
                planets, houses, asc, 
                birth_data["timezone"], lang_code
            )
            
            # Overview with more detail
            overview_label = lang.get('today_overview', "Today's Overview")
            st.markdown(f"### {overview_label}")
            st.markdown(f"_{fortune['overview']}_")
            st.markdown(f"**Day:** {fortune.get('day_name', '')}")
            
            # Lucky elements - enhanced display
            lucky = fortune.get("lucky", {})
            st.markdown("### 🍀 Lucky Elements")
            lucky_cols = st.columns(4)
            with lucky_cols[0]:
                st.markdown(f"**🎨 Color:** {lucky.get('color', '-')}")
            with lucky_cols[1]:
                st.markdown(f"**🔢 Number:** {lucky.get('number', '-')}")
            with lucky_cols[2]:
                st.markdown(f"**📅 Lucky Day:** {lucky.get('day', '-')}")
            with lucky_cols[3]:
                st.markdown(f"**💫 Element:** {lucky.get('element', '-')}")
            
            # Major transits with house positions
            st.markdown("### 🪐 Major Transits Today")
            for t in fortune.get("major_transits", []):
                rx_indicator = " 🔄" if t.get("retrograde") else ""
                with st.expander(f"**{t['planet']}** in {t['sign']} {t['degree']}{rx_indicator} → House {t['house']}"):
                    st.markdown(f"**House {t['house']}:** {t.get('house_meaning', '')}")
                    st.markdown(f"**In Sign:** {t.get('meaning', '')}")
                    if t.get('sabian'):
                        st.markdown(f"**✨ Sabian Symbol ({t['sign']} {t['degree']}):** _{t['sabian']}_")
            
            # Transit aspects - detailed interpretation
            if fortune.get("transit_aspects"):
                st.markdown("### 🔗 Transit-Natal Aspects")
                for asp in fortune.get("transit_aspects", [])[:6]:
                    exact_indicator = "🎯" if asp.get('exactness') == 'exact' else ""
                    with st.expander(f"**{asp['transiting']}** ({asp['transit_sign']}) **{asp['aspect']}** **{asp['natal']}** ({asp['natal_sign']}) {exact_indicator}"):
                        st.markdown(f"**Orb:** {asp['orb']}°")
                        st.markdown(f"**House Affected:** {asp['house_affected']} - {asp.get('house_meaning', '')}")
                        if asp.get('transit_sabian'):
                            st.markdown(f"**✨ Transit Sabian ({asp['transit_sign']} {asp['transit_degree']}°):** _{asp['transit_sabian']}_")
                        if asp.get('natal_sabian'):
                            st.markdown(f"**✨ Natal Sabian ({asp['natal_sign']} {asp['natal_degree']}°):** _{asp['natal_sabian']}_")
                        st.markdown(f"_{asp.get('interpretation', '')}_")
            
            # Retrograde effects
            if fortune.get("retrograde_effects"):
                st.markdown("### 🔄 Retrograde Planets")
                for rx in fortune.get("retrograde_effects", []):
                    st.markdown(f"**{rx['planet']}:** {rx.get('meaning', '')}")
            
            # House activations
            if fortune.get("house_activations"):
                st.markdown("### 🏠 Activated Houses")
                for ha in fortune.get("house_activations", []):
                    st.markdown(f"**House {ha['house']}:** {ha.get('meaning', '')}")
            
            # Personalized recommendations
            if fortune.get("recommendations"):
                st.markdown("### 💡 Recommendations")
                for rec in fortune.get("recommendations", []):
                    st.markdown(f"- {rec}")
    
    # ===== TAB 2: MONTHLY =====
    with pred_tabs[1]:
        st.subheader("📆 " + lang.get("monthly_outlook", "Monthly Outlook"))
        
        with st.spinner("Generating monthly outlook..."):
            now = datetime.now()
            monthly = generate_monthly_outlook(planets, asc, now.year, now.month, birth_data["timezone"], lang_code)
            
            # Overview
            st.markdown(f"### {lang.get('month_theme', 'Monthly Theme')}")
            st.write(monthly.get("theme", ""))
            
            # Key planetary movements this month
            themes = monthly.get("themes", [])
            if themes:
                st.markdown(f"### 🪐 {lang.get('key_transits', 'Key Transits')}")
                cols = st.columns(3)
                for i, t in enumerate(themes[:6]):
                    with cols[i % 3]:
                        st.metric(f"{t.get('planet', '')}", f"{t.get('sign', '')}", f"{t.get('element', '')}")
                        if t.get("meaning"):
                            st.caption(t["meaning"][:80] + "..." if len(t.get("meaning", "")) > 80 else t.get("meaning", ""))
            
            # Highlights
            highlights = monthly.get("highlights", [])
            if highlights:
                st.markdown(f"### ⭐ {lang.get('highlights', 'Highlights')}")
                for h in highlights[:5]:
                    st.markdown(f"• {h}")
            
            # Advice
            st.markdown(f"### 💡 {lang.get('advice', 'Advice')}")
            st.info(monthly.get("advice", ""))
    
    # ===== TAB 3: YEARLY =====
    with pred_tabs[2]:
        st.subheader("📊 " + lang.get("yearly_outlook", "Yearly Outlook"))
        
        with st.spinner("Generating yearly outlook..."):
            now = datetime.now()
            yearly = generate_yearly_outlook(planets, asc, now.year, birth_data["timezone"], lang_code)
            
            # Overview
            st.markdown(f"### 📅 {now.year} {lang.get('yearly_outlook', 'Yearly Outlook')}")
            st.write(yearly.get("overview", ""))
            
            # Major transits
            major = yearly.get("major_transits", [])
            if major:
                st.markdown(f"### 🪐 {lang.get('major_transits', 'Major Transits')}")
                cols = st.columns(4)
                for i, t in enumerate(major[:8]):
                    with cols[i % 4]:
                        st.metric(f"{t.get('planet', '')}", f"{t.get('sign', '')}")
            
            # Quarterly breakdown
            quarters = yearly.get("quarters", [])
            if quarters:
                st.markdown(f"### 📈 {lang.get('quarters', 'Quarterly Overview')}")
                
                # Q1
                q1 = [q for q in quarters if 'Q1' in q.get('period', '')]
                if q1:
                    st.markdown("**Q1 (Jan-Mar):** " + q1[0].get('theme', ''))
                
                # Q2
                q2 = [q for q in quarters if 'Q2' in q.get('period', '')]
                if q2:
                    st.markdown("**Q2 (Apr-Jun):** " + q2[0].get('theme', ''))
                
                # Q3
                q3 = [q for q in quarters if 'Q3' in q.get('period', '')]
                if q3:
                    st.markdown("**Q3 (Jul-Sep):** " + q3[0].get('theme', ''))
                
                # Q4
                q4 = [q for q in quarters if 'Q4' in q.get('period', '')]
                if q4:
                    st.markdown("**Q4 (Oct-Dec):** " + q4[0].get('theme', ''))
            
            # Advice
            st.markdown(f"### 💡 {lang.get('advice', 'Advice')}")
            st.info(yearly.get("advice", ""))
    
    # Thai prediction (if Thai lang)
    if lang_code == "th":
        render_thai_prediction(year, month, day, planets, lang)


# ============== Main App ==============
def main():
    """Main application"""
    # Language selector
    lang_code = st.sidebar.selectbox("Language", ["en", "th"], 
                                      format_func=lambda x: {"en": "English", "th": "ไทย"}[x])
    lang = get_lang(lang_code)
    
    render_header(lang)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        lang["tab_input"], lang["tab_chart"], lang["tab_prediction"],
        lang.get("tab_transit", "🚀 Transits"), lang.get("tab_synastry", "💕 Synastry")
    ])
    
    # === TAB 1: INPUT ===
    with tab1:
        birth_data = render_birth_input(lang)
        
        if st.button(lang["calculate"], type="primary", use_container_width=True):
            try:
                with st.spinner("Calculating..."):
                    calc = SwissEphemerisCalculator()
                    result = calc.calculate_all(
                        year=birth_data["year"],
                        month=birth_data["month"],
                        day=birth_data["day"],
                        hour=birth_data["hour"],
                        minute=birth_data["minute"],
                        latitude=birth_data["latitude"],
                        longitude=birth_data["longitude"],
                        timezone=birth_data["timezone"]
                    )
                
                # Store in session state
                st.session_state["birth_data"] = birth_data
                st.session_state["chart_result"] = result
                
                st.success(f"✅ {lang['your_chart']} - {birth_data['year']}-{birth_data['month']:02d}-{birth_data['day']:02d}")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.info(lang["enter_birth"])
    
    # === TAB 2: BIRTH CHART ===
    with tab2:
        if "chart_result" in st.session_state:
            result = st.session_state["chart_result"]
            
            # Chart wheel visualization
            st.subheader("🌀 " + lang.get("chart_wheel", "Chart Wheel"))
            
            # Options for the chart
            col_opts1, col_opts2 = st.columns([1, 1])
            with col_opts1:
                show_houses = st.checkbox(lang.get("show_houses", "Show Houses"), value=True)
            with col_opts2:
                show_aspects = st.checkbox(lang.get("show_aspects", "Show Aspects"), value=True)
            
            # Generate and display chart with loading animation
            with st.container():
                loading_placeholder = st.empty()
                with loading_placeholder:
                    st.markdown("""
                    <div class="loading-container">
                        <div class="loading-spinner"></div>
                        <div class="loading-text">✨ Reading the stars...</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Create interactive Plotly chart
                fig = create_interactive_chart_wheel(
                    planets=result["planets"],
                    houses=result["houses"],
                    ascendant=result["ascendant"],
                    midheaven=result["midheaven"],
                    aspects=result.get("aspects", []) if show_aspects else None,
                    show_aspects=show_aspects,
                    show_houses=show_houses,
                    width=600,
                    height=600
                )
                
                # Clear loading and show chart
                loading_placeholder.empty()
                
                # Display interactive chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Interactive Planet Details
            st.markdown("### ☀️ Planet Details")
            st.markdown("*Hover over planets in the chart above to learn more*")
            
            # Create expandable planet cards
            for planet, data in result["planets"].items():
                sign = data.get("sign", "Unknown")
                degree = data.get("degree", 0)
                house = data.get("house", "N/A")
                is_retrograde = data.get("retrograde", False)
                
                # Get element for color
                element = "Unknown"
                if sign in ["Aries", "Leo", "Sagittarius"]:
                    element = "Fire"
                elif sign in ["Taurus", "Virgo", "Capricorn"]:
                    element = "Earth"
                elif sign in ["Gemini", "Libra", "Aquarius"]:
                    element = "Air"
                elif sign in ["Cancer", "Scorpio", "Pisces"]:
                    element = "Water"
                
                with st.expander(f"🌟 {planet} in {sign} {int(degree)}° {'(Rx)' if is_retrograde else ''}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Sign:** {sign}")
                        st.markdown(f"**Degree:** {int(degree)}°{int((degree % 1) * 60)}'")
                        st.markdown(f"**House:** {house}")
                    with col2:
                        st.markdown(f"**Element:** <span class='element-{element.lower()}'>{element}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Retrograde:** {'Yes 🔄' if is_retrograde else 'No'}")
                    
                    # Planet description
                    planet_descriptions = {
                        'Sun': 'The core of your identity and life force.',
                        'Moon': 'Your emotional nature and inner needs.',
                        'Mercury': 'Your communication style and thinking.',
                        'Venus': 'Love, beauty, and what you value.',
                        'Mars': 'Energy, drive, and action.',
                        'Jupiter': 'Growth, luck, and expansion.',
                        'Saturn': 'Discipline, structure, and lessons.',
                        'Uranus': 'Innovation, change, and uniqueness.',
                        'Neptune': 'Dreams, intuition, and spirituality.',
                        'Pluto': 'Transformation and power.'
                    }
                    if planet in planet_descriptions:
                        st.markdown(f"_{planet_descriptions[planet]}_")
            
            st.markdown("---")
            
            st.markdown("---")
            
            # Text details below chart
            render_birth_chart(result, lang)
            render_planets(result["planets"], lang)
            render_houses(result["houses"], lang)
            render_aspects(result["aspects"], lang)
        else:
            st.info(lang["enter_birth"])
    
    # === TAB 3: PREDICTION ===
    with tab3:
        if "chart_result" in st.session_state and "birth_data" in st.session_state:
            result = st.session_state["chart_result"]
            birth_data = st.session_state["birth_data"]
            render_prediction_section(result, birth_data, lang, lang_code)
        else:
            st.info(lang["enter_birth"])
    
    # === TAB 4: TRANSITS ===
    with tab4:
        if "chart_result" in st.session_state:
            result = st.session_state["chart_result"]
            birth_data = st.session_state["birth_data"]
            
            st.subheader("🚀 " + lang.get("transit_overlay", "Transit Overlay"))
            
            # Options
            col_opts1, col_opts2 = st.columns([1, 1])
            with col_opts1:
                show_transit_houses = st.checkbox(lang.get("show_houses", "Show Houses"), value=True, key="trans_houses")
            with col_opts2:
                show_transit_aspects = st.checkbox(lang.get("show_aspects", "Show Aspects"), value=True, key="trans_aspects")
            
            with st.spinner("Calculating current transits..."):
                # Get current transits
                transits = get_current_transits(timezone=birth_data["timezone"])
                
                # Create transit overlay chart
                fig = create_transit_overlay_chart(
                    natal_planets=result["planets"],
                    natal_houses=result["houses"],
                    natal_ascendant=result["ascendant"],
                    natal_midheaven=result["midheaven"],
                    natal_aspects=result.get("aspects", []),
                    transit_planets=transits,
                    show_aspects=True,
                    show_houses=show_transit_houses,
                    show_transit_aspects=show_transit_aspects
                )
                chart_bytes = chart_to_image(fig)
                st.image(chart_bytes, use_container_width=True)
                plt.close(fig)
            
            # Show current transit positions
            st.markdown("---")
            st.subheader(lang.get("current_transits", "Current Transits"))
            
            transit_cols = st.columns(5)
            transit_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 
                              'Saturn', 'Uranus', 'Neptune', 'Pluto']
            for i, planet in enumerate(transit_planets):
                if planet in transits:
                    with transit_cols[i % 5]:
                        t = transits[planet]
                        st.metric(planet, f"{t['sign']} {t['degree']:.1f}°")
        else:
            st.info(lang["enter_birth"])
    
    # === TAB 5: SYNASTRY ===
    with tab5:
        if "chart_result" in st.session_state:
            result = st.session_state["chart_result"]
            birth_data = st.session_state["birth_data"]
            
            st.subheader("💕 " + lang.get("synastry", "Synastry Chart"))
            
            # Person 2 input
            st.markdown("### " + lang.get("enter_person2", "Enter second person's birth details"))
            
            birth_data_p2 = render_birth_input(lang, key_prefix="p2_")
            
            col_calc = st.columns([1])
            with col_calc[0]:
                if st.button(lang.get("compare", "Compare Charts"), type="primary", use_container_width=True, key="synastry_btn"):
                    try:
                        with st.spinner("Calculating synastry..."):
                            # Calculate Person 2 chart
                            calc = SwissEphemerisCalculator()
                            result_p2 = calc.calculate_all(
                                year=birth_data_p2["year"],
                                month=birth_data_p2["month"],
                                day=birth_data_p2["day"],
                                hour=birth_data_p2["hour"],
                                minute=birth_data_p2["minute"],
                                latitude=birth_data_p2["latitude"],
                                longitude=birth_data_p2["longitude"],
                                timezone=birth_data_p2["timezone"]
                            )
                            
                            # Store in session
                            st.session_state["chart_result_p2"] = result_p2
                            st.session_state["birth_data_p2"] = birth_data_p2
                            
                            # Options
                            col_opts1, col_opts2 = st.columns([1, 1])
                            with col_opts1:
                                show_syn_houses = st.checkbox(lang.get("show_houses", "Show Houses"), value=True, key="syn_houses")
                            with col_opts2:
                                show_syn_aspects = st.checkbox(lang.get("show_aspects", "Show Aspects"), value=True, key="syn_aspects")
                            
                            # Create synastry chart
                            fig = create_synastry_chart(
                                person1_planets=result["planets"],
                                person1_houses=result["houses"],
                                person1_ascendant=result["ascendant"],
                                person1_midheaven=result["midheaven"],
                                person2_planets=result_p2["planets"],
                                person2_houses=result_p2["houses"],
                                person2_ascendant=result_p2["ascendant"],
                                person2_midheaven=result_p2["midheaven"],
                                person1_name="You",
                                person2_name="Partner",
                                show_aspects=show_syn_aspects,
                                show_houses=show_syn_houses
                            )
                            chart_bytes = chart_to_image(fig)
                            st.image(chart_bytes, use_container_width=True)
                            plt.close(fig)
                            
                            # === SYNASTRY COMPATIBILITY ANALYSIS ===
                            st.markdown("---")
                            st.subheader("💕 " + lang.get("love_potential", "Love & Relationship Potential"))
                            
                            # Element compatibility - planets is already a dict
                            planets1 = {name: data["sign"] for name, data in result["planets"].items()}
                            planets2 = {name: data["sign"] for name, data in result_p2["planets"].items()}
                            
                            elements1 = [WESTERN_SIGNS.get(sign, {}).get("element", "") for sign in planets1.values()]
                            elements2 = [WESTERN_SIGNS.get(sign, {}).get("element", "") for sign in planets2.values()]
                            
                            # Count elements
                            from collections import Counter
                            elem1_count = Counter(elements1)
                            elem2_count = Counter(elements2)
                            
                            # Compatibility calculation
                            compat_score = 50  # Base score
                            
                            # Fire + Fire = strong
                            if elem1_count.get("Fire", 0) + elem2_count.get("Fire", 0) >= 3:
                                compat_score += 20
                                st.success("🔥 " + lang.get("strong_match", "Strong Match") + " - Fire energy flows well together!")
                            # Fire + Water = challenging
                            elif (elem1_count.get("Fire", 0) > 0 and elem1_count.get("Water", 0) > 0) or (elem2_count.get("Fire", 0) > 0 and elem2_count.get("Water", 0) > 0):
                                compat_score -= 10
                                st.warning("💧 " + lang.get("challenging_match", "Challenging") + " - Fire and Water need balance.")
                            # Earth + Water = deep connection
                            elif elem1_count.get("Earth", 0) + elem2_count.get("Earth", 0) >= 2 and elem1_count.get("Water", 0) + elem2_count.get("Water", 0) >= 2:
                                compat_score += 15
                                st.success("🌊 " + lang.get("balanced_match", "Balanced") + " - Deep emotional connection!")
                            # Air + Air = mental connection
                            elif elem1_count.get("Air", 0) + elem2_count.get("Air", 0) >= 3:
                                compat_score += 15
                                st.success("💨 " + lang.get("strong_match", "Strong Match") + " - Great mental connection!")
                            else:
                                compat_score += 10
                                st.info("⚖️ " + lang.get("balanced_match", "Balanced") + " - Complementary energies.")
                            
                            # Key aspects - simplified
                            aspects_list = []
                            if "Sun" in planets1 and "Moon" in planets2:
                                aspects_list.append(f"☀️+🌙 ({planets1['Sun']}→{planets2['Moon']})")
                            if "Venus" in planets1 and "Mars" in planets2:
                                aspects_list.append(f"♀️+♂️ ({planets1['Venus']}→{planets2['Mars']})")
                            if "Moon" in planets1 and "Venus" in planets2:
                                aspects_list.append(f"🌙+♀️ ({planets1['Moon']}→{planets2['Venus']})")
                            
                            # Compatibility percentage
                            st.markdown("---")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("💕 " + lang.get("compatibility_percentage", "Compatibility"), f"{min(compat_score, 99)}%")
                            with col2:
                                if aspects_list:
                                    st.write("**Aspects:** " + " | ".join(aspects_list))
                                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.info(lang["enter_birth"])


if __name__ == "__main__":
    main()
