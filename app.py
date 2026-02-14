"""
Swiss Horoscope - Main Streamlit Application
Precision-powered horoscope using Swiss Ephemeris (pyswisseph)
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Dict, List
from core.swiss_eph import SwissEphemerisCalculator


# ============== Page Config ==============
st.set_page_config(
    page_title="🔮 Swiss Horoscope",
    page_icon="🔮",
    layout="wide"
)


# ============== Language Support ==============
LANG = {
    "en": {
        "title": "🔮 Swiss Horoscope",
        "subtitle": "Precision Astrology with Swiss Ephemeris",
        "birth_info": "📅 Birth Information",
        "birth_date": "Birth Date",
        "birth_time": "Birth Time",
        "hour": "Hour",
        "minute": "Minute",
        "location": "📍 Birth Location",
        "select_city": "Select City",
        "calculate": "✨ Calculate Birth Chart",
        "your_chart": "Your Birth Chart",
        "sun_sign": "Sun Sign (Birth Sign)",
        "planets": "🪐 Planetary Positions",
        "ascendant": "Rising Sign (Ascendant)",
        "midheaven": "Midheaven (MC)",
        "houses": "🏠 House Cusps",
        "aspects": "🔗 Aspects",
        "sign": "Sign",
        "degree": "Degree",
        "house": "House",
        "retrograde": "Retrograde",
        "enter_birth": "Enter your birth details to see your chart",
        "prediction": "🔮 Daily Prediction",
        "elements": "🔥 Elements Distribution",
        "chart_viz": "📊 Birth Chart Visualization",
    },
    "th": {
        "title": "🔮 ดวงชะตาสวิส",
        "subtitle": "โหราศาสตร์แม่นยำสูงด้วย Swiss Ephemeris",
        "birth_info": "📅 ข้อมูลวันเกิด",
        "birth_date": "วันเกิด",
        "birth_time": "เวลาเกิด",
        "hour": "ชั่วโมง",
        "minute": "นาที",
        "location": "📍 สถานที่เกิด",
        "select_city": "เลือกเมือง",
        "calculate": "✨ คำนวณดวงชะตา",
        "your_chart": "ดวงชะตาของคุณ",
        "sun_sign": "ราศีเกิด (Sun Sign)",
        "planets": "🪐 ตำแหน่งดาวเคราะห์",
        "ascendant": "ราศีขึ้น (Ascendant)",
        "midheaven": "มิดฮีเวน (MC)",
        "houses": "🏠 ตำแหน่งเรือน",
        "aspects": "🔗 มุมระหว่างดาว",
        "sign": "ราศี",
        "degree": "องศา",
        "house": "เรือน",
        "retrograde": "ถอยหลัง",
        "enter_birth": "กรอกข้อมูลวันเกิดของคุณเพื่อดูดวงชะตา",
        "prediction": "🔮 คำทำนายประจำวัน",
        "elements": "🔥 ธาตุ",
        "chart_viz": "📊 ภาพดวงชะตา",
    },
    "zh": {
        "title": "🔮 瑞士星盘",
        "subtitle": "使用瑞士星历表的高精度占星术",
        "birth_info": "📅 出生信息",
        "birth_date": "出生日期",
        "birth_time": "出生时间",
        "hour": "小时",
        "minute": "分钟",
        "location": "📍 出生地点",
        "select_city": "选择城市",
        "calculate": "✨ 计算星盘",
        "your_chart": "你的星盘",
        "sun_sign": "太阳星座",
        "planets": "🪐 行星位置",
        "ascendant": "上升星座",
        "midheaven": "中天 (MC)",
        "houses": "🏠 宫位",
        "aspects": "🔗 相位",
        "sign": "星座",
        "degree": "度数",
        "house": "宫",
        "retrograde": "逆行",
        "enter_birth": "输入您的出生信息以查看星盘",
        "prediction": "🔮 每日预测",
        "elements": "🔥 元素分布",
        "chart_viz": "📊 星盘可视化",
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

# Zodiac signs with traits
SIGN_TRAITS = {
    "Aries": {"element": "Fire", "quality": "Cardinal", "traits": "Bold, energetic, pioneering, competitive"},
    "Taurus": {"element": "Earth", "quality": "Fixed", "traits": "Patient, reliable, practical, sensual"},
    "Gemini": {"element": "Air", "quality": "Mutable", "traits": "Curious, adaptable, communicative, witty"},
    "Cancer": {"element": "Water", "quality": "Cardinal", "traits": "Intuitive, emotional, protective, nurturing"},
    "Leo": {"element": "Fire", "quality": "Fixed", "traits": "Confident, creative, generous, proud"},
    "Virgo": {"element": "Earth", "quality": "Mutable", "traits": "Analytical, practical, helpful, perfectionist"},
    "Libra": {"element": "Air", "quality": "Cardinal", "traits": "Diplomatic, fair, social, artistic"},
    "Scorpio": {"element": "Water", "quality": "Fixed", "traits": "Passionate, mysterious, determined, intense"},
    "Sagittarius": {"element": "Fire", "quality": "Mutable", "traits": "Optimistic, adventurous, philosophical, honest"},
    "Capricorn": {"element": "Earth", "quality": "Cardinal", "traits": "Ambitious, disciplined, responsible, patient"},
    "Aquarius": {"element": "Air", "quality": "Fixed", "traits": "Independent, original, humanitarian, quirky"},
    "Pisces": {"element": "Water", "quality": "Mutable", "traits": "Compassionate, artistic, intuitive, escapist"},
}

ELEMENT_TRAITS = {
    "Fire": {"color": "🔴", "traits": "Energetic, passionate, impulsive, enthusiastic"},
    "Earth": {"color": "🟤", "traits": "Practical, stable, grounded, materialistic"},
    "Air": {"color": "💨", "traits": "Intellectual, social, communicative, flexible"},
    "Water": {"color": "💧", "traits": "Emotional, intuitive, compassionate, sensitive"},
}


def get_lang(lang_code: str = "en") -> dict:
    """Get language dictionary"""
    return LANG.get(lang_code, LANG["en"])


# ============== UI Functions ==============
def render_header(lang: dict):
    """Render page header"""
    st.title(lang["title"])
    st.markdown(f"*{lang['subtitle']}*")


def render_birth_input(lang: dict, lang_code: str = "en", key_prefix: str = "") -> Optional[Dict]:
    """Render birth information input form"""
    st.subheader(lang["birth_info"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        birth_date = st.date_input(
            lang["birth_date"],
            value=datetime(1990, 1, 1),
            key=f"{key_prefix}_date"
        )
    
    with col2:
        hour = st.number_input(lang["hour"], 0, 23, 12, key=f"{key_prefix}_hour")
        minute = st.number_input(lang["minute"], 0, 59, 0, key=f"{key_prefix}_minute")
    
    st.subheader(lang["location"])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_city = st.selectbox(
            lang["select_city"],
            options=list(CITIES.keys()),
            key=f"{key_prefix}_city"
        )
    
    city_data = CITIES[selected_city]
    
    with col2:
        st.text_input("Timezone", value=city_data["tz"], disabled=True)
    
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


def render_planets(planets: Dict, lang: dict):
    """Render planetary positions"""
    st.subheader(lang["planets"])
    
    # Planet display order
    planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", 
                    "Saturn", "Uranus", "Neptune", "Pluto", "North Node", "South Node"]
    
    cols = st.columns(3)
    
    for i, planet in enumerate(planet_order):
        if planet in planets:
            p = planets[planet]
            with cols[i % 3]:
                retro = " (R)" if p.get("retrograde") else ""
                house = f", H{p.get('house')}" if p.get("house") else ""
                st.metric(
                    f"{planet}",
                    f"{p['sign']} {p['degree']:.1f}°{retro}"
                )


def render_ascendant_midheaven(asc: Dict, mc: Dict, lang: dict):
    """Render Ascendant and Midheaven"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            f"↑ {lang['ascendant']}",
            f"{asc['sign']} {asc['degree']:.1f}°"
        )
    
    with col2:
        st.metric(
            f"☰ {lang['midheaven']}",
            f"{mc['sign']} {mc['degree']:.1f}°"
        )


def render_houses(houses: Dict, lang: dict):
    """Render house cusps"""
    st.subheader(lang["houses"])
    
    cols = st.columns(4)
    for i, (house_num, house_data) in enumerate(sorted(houses.items())):
        with cols[i % 4]:
            st.metric(
                f"House {house_num}",
                f"{house_data['sign']} {house_data['degree']:.1f}°"
            )


def render_aspects(aspects: List[Dict], lang: dict):
    """Render aspects"""
    st.subheader(lang["aspects"])
    
    aspect_emojis = {
        "CONJUNCTION": "☌",
        "OPPOSITION": "☍",
        "SQUARE": "□",
        "TRINE": "△",
        "SEXTILE": "⚹"
    }
    
    if not aspects:
        st.info("No major aspects detected")
        return
    
    # Group by aspect type
    for aspect in aspects:
        emoji = aspect_emojis.get(aspect["type"], "●")
        orb_text = "★" if aspect["exact"] else ""
        st.markdown(f"**{emoji} {aspect['p1']}** — **{aspect['p2']}** ({aspect['type']}{orb_text})")


def render_elements(planets: Dict, lang: dict):
    """Render element distribution"""
    st.subheader(lang["elements"])
    
    elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
    
    planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", 
                    "Saturn", "Uranus", "Neptune", "Pluto"]
    
    for planet in planet_order:
        if planet in planets:
            sign = planets[planet]["sign"]
            if sign in SIGN_TRAITS:
                elem = SIGN_TRAITS[sign]["element"]
                elements[elem] += 1
    
    cols = st.columns(4)
    for i, (elem, count) in enumerate(elements.items()):
        emoji = ELEMENT_TRAITS[elem]["color"]
        with cols[i]:
            st.metric(f"{emoji} {elem}", f"{count}/10")


def render_prediction(planets: Dict, asc: Dict, lang: dict) -> str:
    """Generate simple prediction based on chart"""
    st.subheader(lang["prediction"])
    
    # Get sun sign
    sun_sign = planets.get("Sun", {}).get("sign", "Aries")
    asc_sign = asc.get("sign", "Aries")
    
    # Get traits
    sun_traits = SIGN_TRAITS.get(sun_sign, {})
    sun_element = sun_traits.get("element", "Fire")
    sun_quality = sun_traits.get("quality", "Cardinal")
    
    # Simple prediction template
    prediction = f"""
### ☀️ Sun in {sun_sign}
*{sun_traits.get('traits', '')}*

**Element:** {sun_element} | **Quality:** {sun_quality}

### ↑ Rising Sign: {asc_sign}
Your rising sign represents how others see you initially and your approach to life.

---
*This is a basic prediction based on your birth chart. For detailed readings, consult a professional astrologer.*
"""
    
    st.markdown(prediction)
    return sun_sign


def render_chart_visualization(planets: Dict, houses: Dict, asc: Dict, lang: dict):
    """Render ASCII birth chart visualization"""
    st.subheader(lang["chart_viz"])
    
    # Create a simple wheel representation
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    # Build planet positions
    planet_positions = {}
    for planet, data in planets.items():
        sign = data.get("sign", "Aries")
        degree = data.get("degree", 0)
        sign_idx = signs.index(sign) if sign in signs else 0
        position = sign_idx * 30 + degree
        planet_positions[planet] = {"sign": sign, "degree": degree, "position": position}
    
    # Ascendant
    if asc:
        asc_sign = asc.get("sign", "Aries")
        asc_degree = asc.get("degree", 0)
        asc_idx = signs.index(asc_sign) if asc_sign in signs else 0
        planet_positions["ASC"] = {"sign": asc_sign, "degree": asc_degree, "position": asc_idx * 30 + asc_degree}
    
    # Display as a table
    data = []
    for planet, info in planet_positions.items():
        data.append({
            "Planet": planet,
            "Sign": info["sign"],
            "Degree": f"{info['degree']:.1f}°",
            "Position": "●" * 10
        })
    
    st.table(data)


# ============== Main App ==============
def main():
    """Main application"""
    # Language selector
    lang_code = st.sidebar.selectbox("Language", ["en", "th", "zh"], format_func=lambda x: {"en": "English", "th": "ไทย", "zh": "中文"}[x])
    lang = get_lang(lang_code)
    
    render_header(lang)
    
    # Birth input
    birth_data = render_birth_input(lang, lang_code)
    
    # Calculate button
    if st.button(lang["calculate"], type="primary"):
        try:
            with st.spinner("Calculating your birth chart..."):
                # Calculate chart
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
            
            st.success(f"✨ {lang['your_chart']}")
            
            # Display birth info
            st.markdown(f"**{result['subject']['date_time']}** | {result['subject']['timezone']}")
            
            # Sun sign prominently
            sun = result['planets']['Sun']
            st.info(f"### 🌟 {lang['sun_sign']}: {sun['sign']} {sun['degree']:.1f}°")
            
            # Ascendant & Midheaven
            render_ascendant_midheaven(result["ascendant"], result["midheaven"], lang)
            
            # Elements
            render_elements(result["planets"], lang)
            
            # Prediction
            sun_sign = render_prediction(result["planets"], result["ascendant"], lang)
            
            # Chart visualization
            render_chart_visualization(result["planets"], result["houses"], result["ascendant"], lang)
            
            # Planets
            render_planets(result["planets"], lang)
            
            # Houses
            render_houses(result["houses"], lang)
            
            # Aspects
            render_aspects(result["aspects"], lang)
            
        except Exception as e:
            st.error(f"Error calculating chart: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    else:
        st.info(lang["enter_birth"])


if __name__ == "__main__":
    main()
