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
        "name": "Name",
        "birth_date": "Birth Date",
        "birth_time": "Birth Time",
        "hour": "Hour",
        "minute": "Minute",
        "location": "📍 Birth Location",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "timezone": "Timezone",
        "calculate": "✨ Calculate Birth Chart",
        "your_chart": "Your Birth Chart",
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
    },
    "th": {
        "title": "🔮 ดวงชะตาสวิส",
        "subtitle": "โหราศาสตร์แม่นยำสูงด้วย Swiss Ephemeris",
        "birth_info": "📅 ข้อมูลวันเกิด",
        "name": "ชื่อ",
        "birth_date": "วันเกิด",
        "birth_time": "เวลาเกิด",
        "hour": "ชั่วโมง",
        "minute": "นาที",
        "location": "📍 สถานที่เกิด",
        "latitude": "ละติจูด",
        "longitude": "ลองจิจูด",
        "timezone": "เขตเวลา",
        "calculate": "✨ คำนวณดวงชะตา",
        "your_chart": "ดวงชะตาของคุณ",
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
    },
    "zh": {
        "title": "🔮 瑞士星盘",
        "subtitle": "使用瑞士星历表的高精度占星术",
        "birth_info": "📅 出生信息",
        "name": "姓名",
        "birth_date": "出生日期",
        "birth_time": "出生时间",
        "hour": "小时",
        "minute": "分钟",
        "location": "📍 出生地点",
        "latitude": "纬度",
        "longitude": "经度",
        "timezone": "时区",
        "calculate": "✨ 计算星盘",
        "your_chart": "你的星盘",
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
    }
}

# Common locations (city: lat, lng)
COMMON_LOCATIONS = {
    "en": {
        "Bangkok, Thailand": (13.7563, 100.5018),
        "Hong Kong": (22.3193, 114.1694),
        "London, UK": (51.5074, -0.1278),
        "New York, USA": (40.7128, -74.0060),
        "Tokyo, Japan": (35.6762, 139.6503),
        "Los Angeles, USA": (34.0522, -118.2437),
        "Singapore": (1.3521, 103.8198),
    },
    "th": {
        "กรุงเทพฯ ประเทศไทย": (13.7563, 100.5018),
        "ฮ่องกง": (22.3193, 114.1694),
        "ลอนดอน อังกฤษ": (51.5074, -0.1278),
        "นิวยอร์ก สหรัฐฯ": (40.7128, -74.0060),
        "โตเกียว ญี่ปุ่น": (35.6762, 139.6503),
        "ลอสแองเจลิส สหรัฐฯ": (34.0522, -118.2437),
        "สิงคโปร์": (1.3521, 103.8198),
    },
    "zh": {
        "泰国曼谷": (13.7563, 100.5018),
        "香港": (22.3193, 114.1694),
        "伦敦": (51.5074, -0.1278),
        "纽约": (40.7128, -74.0060),
        "东京": (35.6762, 139.6503),
        "洛杉矶": (34.0522, -118.2437),
        "新加坡": (1.3521, 103.8198),
    }
}

TIMEZONES = [
    "Asia/Bangkok",
    "Asia/Hong_Kong",
    "Asia/Singapore",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Asia/Seoul",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
    "America/New_York",
    "America/Los_Angeles",
    "America/Chicago",
    "UTC",
]


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
        name = st.text_input(lang["name"], key=f"{key_prefix}_name")
        birth_date = st.date_input(
            lang["birth_date"],
            value=datetime(1990, 1, 1),
            key=f"{key_prefix}_date"
        )
    
    with col2:
        hour = st.number_input(lang["hour"], 0, 23, 12, key=f"{key_prefix}_hour")
        minute = st.number_input(lang["minute"], 0, 59, 0, key=f"{key_prefix}_minute")
    
    st.subheader(lang["location"])
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        location_options = list(COMMON_LOCATIONS.get(lang_code, COMMON_LOCATIONS["en"]).keys())
        selected_location = st.selectbox(
            lang["location"],
            options=location_options,
            key=f"{key_prefix}_location"
        )
    
    with col4:
        latitude = st.number_input(
            lang["latitude"],
            -90.0, 90.0,
            COMMON_LOCATIONS.get(lang_code, COMMON_LOCATIONS["en"])[selected_location][0],
            step=0.1,
            key=f"{key_prefix}_lat"
        )
    
    with col5:
        longitude = st.number_input(
            lang["longitude"],
            -180.0, 180.0,
            COMMON_LOCATIONS.get(lang_code, COMMON_LOCATIONS["en"])[selected_location][1],
            step=0.1,
            key=f"{key_prefix}_lng"
        )
    
    timezone = st.selectbox(
        lang["timezone"],
        options=TIMEZONES,
        index=0,
        key=f"{key_prefix}_tz"
    )
    
    return {
        "name": name or "User",
        "year": birth_date.year,
        "month": birth_date.month,
        "day": birth_date.day,
        "hour": hour,
        "minute": minute,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone
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
                house = f", {p.get('house')}th House" if p.get("house") else ""
                st.metric(
                    f"♈ {planet}",
                    f"{p['sign']} {p['degree']:.2f}°{retro}",
                    help=f"House {house}"
                )


def render_ascendant_midheaven(asc: Dict, mc: Dict, lang: dict):
    """Render Ascendant and Midheaven"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            f"↑ {lang['ascendant']}",
            f"{asc['sign']} {asc['degree']:.2f}°"
        )
    
    with col2:
        st.metric(
            f"☰ {lang['midheaven']}",
            f"{mc['sign']} {mc['degree']:.2f}°"
        )


def render_houses(houses: Dict, lang: dict):
    """Render house cusps"""
    st.subheader(lang["houses"])
    
    cols = st.columns(4)
    for i, (house_num, house_data) in enumerate(sorted(houses.items())):
        with cols[i % 4]:
            st.metric(
                f"House {house_num}",
                f"{house_data['sign']} {house_data['degree']:.2f}°"
            )


def render_aspects(aspects: List[Dict], lang: dict):
    """Render aspects"""
    st.subheader(lang["aspects"])
    
    aspect_emojis = {
        "CONJUNCTION": "Conj",
        "OPPOSITION": "Opp",
        "SQUARE": "Sq",
        "TRINE": "Trine",
        "SEXTILE": "Sxt"
    }
    
    if not aspects:
        st.info("No major aspects detected")
        return
    
    for aspect in aspects:
        emoji = aspect_emojis.get(aspect["type"], "-")
        st.markdown(f"**{emoji} {aspect['p1']}** {aspect['type']} **{aspect['p2']}** (orb: {aspect['orb']:.2f})")


# ============== Main App ==============
def main():
    """Main application"""
    # Language selector
    lang_code = st.sidebar.selectbox("Language", ["en", "th", "zh"], format_func=lambda x: {"en": "English", "th": "ไทย", "zh": "中文"}[x])
    lang = get_lang(lang_code)
    
    render_header(lang)
    
    # Birth input
    birth_data = render_birth_input(lang)
    
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
            
            st.success(f"✨ {lang['your_chart']} - {birth_data['name']}")
            
            # Display results
            st.markdown(f"**{result['subject']['date_time']}** | {result['subject']['timezone']}")
            
            # Ascendant & Midheaven
            render_ascendant_midheaven(result["ascendant"], result["midheaven"], lang)
            
            # Planets
            render_planets(result["planets"], lang)
            
            # Houses
            render_houses(result["houses"], lang)
            
            # Aspects
            render_aspects(result["aspects"], lang)
            
        except Exception as e:
            st.error(f"Error calculating chart: {str(e)}")
            st.info("Make sure you have installed immanuel: pip install immanuel")
    
    else:
        st.info(lang["enter_birth"])


if __name__ == "__main__":
    main()
