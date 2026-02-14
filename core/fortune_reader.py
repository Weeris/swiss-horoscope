"""
Daily Fortune & Outlook Generator
Generates daily, monthly, and yearly predictions based on transits
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import swisseph as swe
import pytz


# ============== Transit Meanings ==============
TRANSIT_MEANINGS = {
    "Sun": {
        "en": "The Sun represents your vitality and core identity. Today brings focus on your self-expression and creativity.",
        "th": "ดวงอาทิตย์แทนพลังชีวิตและตัวตนหลัก วันนี้นำมาซึ่งความสนใจในการแสดงออกและความคิดสร้างสรรค์ของคุณ"
    },
    "Moon": {
        "en": "The Moon governs your emotions. Today is sensitive - trust your instincts and nurture yourself.",
        "th": "ดวงจันทร์ปกครองอารมณ์ของคุณ วันนี้เป็นวันที่อ่อนไหว - ไว้วางใจสัญชาตญาณและดูแลตัวเอง"
    },
    "Mercury": {
        "en": "Mercury influences communication. Today is good for conversations, negotiations, and learning.",
        "th": "ดาวพุธมีอิทธิพลต่อการสื่อสาร วันนี้เหมาะสำหรับการสนทนา การเจรจา และการเรียนรู้"
    },
    "Venus": {
        "en": "Venus brings love and harmony. Focus on relationships, beauty, and things that bring pleasure.",
        "th": "ดาวศุกร์นำมาซึ่งความรักและความกลมกลืน มุ่งเน้นความสัมพันธ์ ความงาม และสิ่งที่ทำให้มีความสุข"
    },
    "Mars": {
        "en": "Mars fuels your energy and drive. Today is great for taking action and pursuing your goals.",
        "th": "ดาวอังคารเป็นเชื้อเพลิงพลังงานและความขยันของคุณ วันนี้เหมาะสำหรับการลงมือทำและไล่ตามเป้าหมาย"
    },
    "Jupiter": {
        "en": "Jupiter expands and brings optimism. Today brings opportunities for growth and adventure.",
        "th": "ดาวพฤหัสบดีขยายตัวและนำความเชื่อมั่นมา วันนี้นำมาซึ่งโอกาสสำหรับการเติบโตและการผจญภัย"
    },
    "Saturn": {
        "en": "Saturn brings structure and lessons. Today calls for patience and responsibility.",
        "th": "ดาวเสาร์นำโครงสร้างและบทเรียนมา วันนี้ต้องการความอดทนและความรับผิดชอบ"
    },
    "Uranus": {
        "en": "Uranus sparks change and innovation. Expect unexpected insights or sudden changes.",
        "th": "ดาวยูเรนัสจุดประกายการเปลี่ยนแปลงและนวัตกรรม คาดหวังข้อมูลเชิงลึกที่ไม่คาดคิดหรือการเปลี่ยนแปลงกะทันหัน"
    },
    "Neptune": {
        "en": "Neptune enhances intuition and creativity. Today is good for spiritual pursuits and artistic expression.",
        "th": "ดาวเนปจูนเสริมสัญชาตญาณและความคิดสร้างสรรค์ วันนี้เหมาะสำหรับการแสวงหาจิตวิญญาณและการแสดงออกทางศิลปะ"
    },
    "Pluto": {
        "en": "Pluto brings transformation. Today may bring deep insights or powerful changes.",
        "th": "ดาวพลูโตนำการเปลี่ยนแปลงมา วันนี้อาจนำข้อมูลเชิงลึกหรือการเปลี่ยนแปลงที่ทรงพลังมา"
    }
}

# ============== Lucky Elements ==============
LUCKY_COLORS = {
    "Fire": {"en": "Red, Orange, Gold", "th": "แดง ส้ม ทอง"},
    "Earth": {"en": "Brown, Green, Tan", "th": "น้ำตาล เขียว เหลืองดิน"},
    "Air": {"en": "Yellow, White, Silver", "th": "เหลือง ขาว เงิน"},
    "Water": {"en": "Blue, Navy, Teal", "th": "น้ำเงิน กรมท่า เขียวแกมน้ำเงิน"}
}

LUCKY_NUMBERS = {
    "Fire": {"en": "1, 9", "th": "1, 9"},
    "Earth": {"en": "2, 8", "th": "2, 8"},
    "Air": {"en": "3, 7", "th": "3, 7"},
    "Water": {"en": "4, 6", "th": "4, 6"}
}

LUCKY_DAYS = {
    "Sun": {"en": "Sunday", "th": "วันอาทิตย์"},
    "Moon": {"en": "Monday", "th": "วันจันทร์"},
    "Mars": {"en": "Tuesday", "th": "วันอังคาร"},
    "Mercury": {"en": "Wednesday", "th": "วันพุธ"},
    "Jupiter": {"en": "Thursday", "th": "วันพฤหัสบดี"},
    "Venus": {"en": "Friday", "th": "วันศุกร์"},
    "Saturn": {"en": "Saturday", "th": "วันเสาร์"}
}

# ============== Sign Rulers ==============
SIGN_RULERS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Pluto", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Uranus", "Pisces": "Neptune"
}

SIGN_ELEMENTS = {
    "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air",
    "Cancer": "Water", "Leo": "Fire", "Virgo": "Earth",
    "Libra": "Air", "Scorpio": "Water", "Sagittarius": "Fire",
    "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water"
}


def get_current_transits_for_date(
    year: int, month: int, day: int,
    hour: int = 12, minute: int = 0,
    timezone: str = "Asia/Bangkok"
) -> Dict:
    """Calculate transits for a specific date"""
    tz = pytz.timezone(timezone)
    dt = tz.localize(datetime(year, month, day, hour, minute))
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
    flags = swe.FLG_SWIEPH
    
    planets = {}
    planet_ids = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
        'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO
    }
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    for name, planet_id in planet_ids.items():
        result = swe.calc_ut(jd, planet_id, flags)
        longitude = result[0][0]
        sign_num = int(longitude / 30) % 12
        
        planets[name] = {
            'longitude': longitude,
            'sign': signs[sign_num],
            'degree': longitude % 30,
            'sign_num': sign_num
        }
    
    return planets


def calculate_transit_aspects(natal_planets: Dict, transit_planets: Dict) -> List[Dict]:
    """Calculate aspects between transiting planets and natal planets"""
    aspects = []
    
    major_aspects = [
        (0, "Conjunction", 8),
        (60, "Sextile", 5),
        (90, "Square", 7),
        (120, "Trine", 7),
        (180, "Opposition", 8)
    ]
    
    for t_planet, t_data in transit_planets.items():
        for n_planet, n_data in natal_planets.items():
            diff = abs(t_data['longitude'] - n_data['longitude'])
            if diff > 180:
                diff = 360 - diff
            
            for deg, name, orb in major_aspects:
                if abs(diff - deg) <= orb:
                    aspects.append({
                        'transiting': t_planet,
                        'natal': n_planet,
                        'type': name,
                        'orb': abs(diff - deg),
                        'transit_sign': t_data['sign'],
                        'natal_sign': n_data['sign']
                    })
    
    return aspects


def generate_daily_fortune(
    natal_planets: Dict,
    natal_ascendant: Dict,
    timezone: str = "Asia/Bangkok",
    lang: str = "en"
) -> Dict:
    """Generate daily fortune based on current transits"""
    
    now = datetime.now(pytz.timezone(timezone))
    today_transits = get_current_transits_for_date(
        now.year, now.month, now.day,
        now.hour, now.minute, timezone
    )
    
    # Calculate aspects
    aspects = calculate_transit_aspects(natal_planets, today_transits)
    
    fortune = {
        "date": now.strftime("%Y-%m-%d"),
        "title": "Daily Fortune" if lang == "en" else "ดวงประจำวัน",
        "overview": "",
        "transits": [],
        "aspects": [],
        "lucky": {}
    }
    
    # Overview based on Sun sign transit
    sun_transit = today_transits.get("Sun", {})
    sun_sign = sun_transit.get("sign", "Aries")
    ruler = SIGN_RULERS.get(sun_sign, "Mars")
    element = SIGN_ELEMENTS.get(sun_sign, "Fire")
    
    fortune["overview"] = f"Today the Sun transits **{sun_sign}**. {TRANSIT_MEANINGS.get(ruler, {}).get(lang, '')}"
    
    # Key transits
    for planet in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if planet in today_transits:
            p = today_transits[planet]
            meaning = TRANSIT_MEANINGS.get(planet, {}).get(lang, "")
            fortune["transits"].append({
                "planet": planet,
                "sign": p["sign"],
                "degree": f"{p['degree']:.1f}°",
                "meaning": meaning
            })
    
    # Key aspects
    for asp in aspects[:5]:
        fortune["aspects"].append({
            "transiting": asp['transiting'],
            "natal": asp['natal'],
            "type": asp['type'],
            "description": f"{asp['transiting']} in {asp['transit_sign']} {asp['type']} {asp['natal']} in {asp['natal_sign']}"
        })
    
    # Lucky elements based on natal Sun
    natal_sun = natal_planets.get("Sun", {})
    natal_sign = natal_sun.get("sign", "Aries")
    element = SIGN_ELEMENTS.get(natal_sign, "Fire")
    
    fortune["lucky"] = {
        "color": LUCKY_COLORS.get(element, {}).get(lang, "All colors"),
        "number": LUCKY_NUMBERS.get(element, {}).get(lang, "All numbers"),
        "day": LUCKY_DAYS.get(ruler, {}).get(lang, "Every day"),
        "element": element
    }
    
    return fortune


def generate_monthly_outlook(
    natal_planets: Dict,
    natal_ascendant: Dict,
    year: int,
    month: int,
    timezone: str = "Asia/Bangkok",
    lang: str = "en"
) -> Dict:
    """Generate monthly outlook based on planetary movements"""
    
    tz = pytz.timezone(timezone)
    first_day = tz.localize(datetime(year, month, 1))
    
    # Get mid-month transits
    mid_month = 15
    mid_transits = get_current_transits_for_date(year, month, mid_month, 12, 0, timezone)
    
    # Get end of month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = (next_month - timedelta(days=1)).day
    
    outlook = {
        "month": first_day.strftime("%B %Y"),
        "title": "Monthly Outlook" if lang == "en" else "ดวงประจำเดือน",
        "themes": [],
        "highlights": [],
        "advice": ""
    }
    
    # Key transits for the month
    for planet in ["Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if planet in mid_transits:
            p = mid_transits[planet]
            sign = p["sign"]
            element = SIGN_ELEMENTS.get(sign, "Fire")
            
            outlook["themes"].append({
                "planet": planet,
                "sign": sign,
                "element": element,
                "meaning": TRANSIT_MEANINGS.get(planet, {}).get(lang, "")
            })
    
    # Major aspects
    aspects = calculate_transit_aspects(natal_planets, mid_transits)
    for asp in aspects[:3]:
        outlook["highlights"].append({
            "aspect": f"{asp['transiting']} {asp['type']} {asp['natal']}",
            "description": f"{asp['transiting']} in {asp['transit_sign']} makes {asp['type']} to natal {asp['natal']}"
        })
    
    # General advice
    jupiter_sign = mid_transits.get("Jupiter", {}).get("sign", "Sagittarius")
    saturn_sign = mid_transits.get("Saturn", {}).get("sign", "Capricorn")
    
    if lang == "en":
        outlook["advice"] = f"This month, focus on growth ({jupiter_sign}) while maintaining structure ({saturn_sign})."
    else:
        outlook["advice"] = f"เดือนนี้ ให้มุ่งเน้นการเติบโต ({jupiter_sign}) ขณะที่รักษาโครงสร้าง ({saturn_sign})"
    
    return outlook


def generate_yearly_outlook(
    natal_planets: Dict,
    natal_ascendant: Dict,
    year: int,
    timezone: str = "Asia/Bangkok",
    lang: str = "en"
) -> Dict:
    """Generate yearly outlook based on major transits (Jupiter & Saturn)"""
    
    outlook = {
        "year": str(year),
        "title": "Yearly Outlook" if lang == "en" else "ดวงประจำปี",
        "overview": "",
        "quarters": [],
        "major_transits": []
    }
    
    # Get transits for key dates in the year
    quarters = [
        (year, 2, "Q1"),   # February
        (year, 5, "Q2"),   # May
        (year, 8, "Q3"),   # August  
        (year, 11, "Q4")   # November
    ]
    
    for q_year, q_month, q_name in quarters:
        transits = get_current_transits_for_date(q_year, q_month, 15, 12, 0, timezone)
        
        jupiter = transits.get("Jupiter", {})
        saturn = transits.get("Saturn", {})
        
        outlook["quarters"].append({
            "quarter": q_name,
            "month": f"{q_month}/{q_year % 100}",
            "jupiter": jupiter.get("sign", "Unknown"),
            "saturn": saturn.get("sign", "Unknown"),
            "theme": f"Jupiter in {jupiter.get('sign')}, Saturn in {saturn.get('sign')}" if lang == "en" else f"ดาวพฤหัสใน{jupiter.get('sign')} ดาวเสาร์ใน{saturn.get('sign')}"
        })
    
    # Get Jupiter and Saturn positions for the year
    year_mid = get_current_transits_for_date(year, 6, 15, 12, 0, timezone)
    jupiter_sign = year_mid.get("Jupiter", {}).get("sign", "Sagittarius")
    saturn_sign = year_mid.get("Saturn", {}).get("sign", "Capricorn")
    
    outlook["major_transits"] = [
        {"planet": "Jupiter", "sign": jupiter_sign, "meaning": "Growth and expansion opportunities"},
        {"planet": "Saturn", "sign": saturn_sign, "meaning": "Lessons and structure building"}
    ]
    
    # Overview
    if lang == "en":
        outlook["overview"] = f"""This year, Jupiter transits **{jupiter_sign}** bringing growth and opportunities, 
while Saturn in **{saturn_sign}** emphasizes structure and responsibility."""
    else:
        outlook["overview"] = f"""ปีนี้ ดาวพฤหัสบดีเดินผ่าน **{jupiter_sign}** นำมาซึ่งการเติบโตและโอกาส 
ในขณะที่ดาวเสาร์ใน **{saturn_sign}** เน้นโครงสร้างและความรับผิดชอบ"""
    
    return outlook
