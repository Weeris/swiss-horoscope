"""
Birth Chart Reading - Destiny Analysis
Generates personalized natal chart readings based on Swiss Ephemeris data
"""

from typing import Dict, List, Optional


# ============== Planet Meanings ==============
PLANET_MEANINGS = {
    "Sun": {
        "en": {
            "core": "The Sun represents your core identity, life force, and vitality. It shows your basic nature and what makes you feel alive.",
            "strengths": "Confidence, creativity, leadership, warmth, generosity",
            "challenges": "Self-centeredness, pride, stubbornness, need for recognition"
        },
        "th": {
            "core": "ดวงอาทิตย์แทนตัวตนที่แท้จริง พลังชีวิต และความมีชีวิตชีวา แสดงธรรมชาติพื้นฐานและสิ่งที่ทำให้คุณมีชีวิตชีวา",
            "strengths": "ความมั่นใจ ความคิดสร้างสรรค์ ความเป็นผู้นำ ความอบอุ่น ความใจกว้าง",
            "challenges": "เห็นแก่ตัว หยิ่ง ดื้อรั้น ต้องการการยอมรับ"
        }
    },
    "Moon": {
        "en": {
            "core": "The Moon represents your emotional nature, instincts, and subconscious. It reveals how you feel and respond to situations.",
            "strengths": "Intuition, adaptability, nurturing, emotional intelligence",
            "challenges": "Mood swings, sensitivity, overthinking, dependency"
        },
        "th": {
            "core": "ดวงจันทร์แทนธรรมชาติทางอารมณ์ สัญชาตญาณ และจิตใต้สำนึก แสดงว่าคุณรู้สึกและตอบสนองต่อสถานการณ์อย่างไร",
            "strengths": "สัญชาตญาณ ความสามารถในการปรับตัว การดูแล ความฉลาดทางอารมณ์",
            "challenges": "อารมณ์แปรปรวน ความรู้สึกอ่อนไหว คิดมาก ต้องพึ่งพาผู้อื่น"
        }
    },
    "Mercury": {
        "en": {
            "core": "Mercury represents your communication style, thinking pattern, and how you process information.",
            "strengths": "Communication, analytical thinking, wit, learning ability",
            "challenges": "Nervousness, criticism, scattered thinking, superficiality"
        },
        "th": {
            "core": "ดาวพุธแทนรูปแบบการสื่อสาร การคิด และวิธีที่คุณประมวลผลข้อมูล",
            "strengths": "การสื่อสาร การคิดวิเคราะห์ อารมณ์ขัน ความสามารถในการเรียนรู้",
            "challenges": "ความกระวนกระวาย การวิจารณ์ ความคิดกระจัด ผิวเผิน"
        }
    },
    "Venus": {
        "en": {
            "core": "Venus represents your love nature, values, and what brings you pleasure and harmony.",
            "strengths": "Charm, diplomacy, artistic appreciation, romance",
            "challenges": "Indecision, vanity, overindulgence, people-pleasing"
        },
        "th": {
            "core": "ดาวศุกร์แทนธรรมชาติด้านความรัก คุณค่า และสิ่งที่ทำให้คุณมีความสุขและประสบการณ์ที่กลมกลืน",
            "strengths": "เสน่ห์ การทูต การเข้าใจศิลปะ ความโรแมนติก",
            "challenges": "ตัดสินใจไม่ได้ ความหยิ่งในความงาม การใช้มากเกินไป การทำให้ทุกคนพอใจ"
        }
    },
    "Mars": {
        "en": {
            "core": "Mars represents your energy, drive, and how you take action. It shows your assertiveness and sexual nature.",
            "strengths": "Courage, determination, passion, physical energy",
            "challenges": "Aggression, impatience, impulsiveness, conflict"
        },
        "th": {
            "core": "ดาวอังคารแทนพลังงาน ความขยัน และวิธีที่คุณลงมือทำ แสดงความกล้าหาญและธรรมชาติทางเพศ",
            "strengths": "ความกล้า ความมุ่งมั่น ความหลงใหล พลังทางกาย",
            "challenges": "ความก้าวร้าว ความใจร้อน ความหุนหันพลันแล่น ความขัดแย้ง"
        }
    },
    "Jupiter": {
        "en": {
            "core": "Jupiter represents your growth, expansion, and optimism. It shows your faith and philosophy of life.",
            "strengths": "Wisdom, optimism, generosity, travel, higher education",
            "challenges": "Excess, overconfidence, exaggeration, laziness"
        },
        "th": {
            "core": "ดาวพฤหัสบดีแทนการเติบโต การขยายตัว และความเชื่อมั่น แสดงศรัทธาและปรัชญาชีวิตของคุณ",
            "strengths": "ปัญญา ความเชื่อมั่น ความใจกว้าง การเดินทาง การศึกษาระดับสูง",
            "challenges": "การใช้มากเกินไป ความมั่นใจมากเกินไป การเกินจริง ความเกียจคร้าน"
        }
    },
    "Saturn": {
        "en": {
            "core": "Saturn represents your boundaries, structure, and life lessons. It shows your responsibilities and fears.",
            "strengths": "Discipline, patience, responsibility, wisdom through experience",
            "challenges": "Self-criticism, fear, restriction, feeling of inadequacy"
        },
        "th": {
            "core": "ดาวเสาร์แทนขอบเขต โครงสร้าง และบทเรียนชีวิต แสดงความรับผิดชอบและความกลัวของคุณ",
            "strengths": "วินัย ความอดทน ความรับผิดชอบ ปัญญาจากประสบการณ์",
            "challenges": "วิจารณ์ตัวเอง ความกลัว การจำกัด ความรู้สึกไม่เพียงพอ"
        }
    },
    "Uranus": {
        "en": {
            "core": "Uranus represents your uniqueness, innovation, and sudden changes. It shows your rebel spirit and humanitarian side.",
            "strengths": "Innovation, independence, originality, humanitarianism",
            "challenges": "Rebellion, unpredictability, detachment, eccentricity"
        },
        "th": {
            "core": "ดาวยูเรนัสแทนความเป็นเอกลักษณ์ นวัตกรรม และการเปลี่ยนแปลงอย่างกะทันหัน แสดงจิตวิญญาณกบฏและด้านมนุษยธรรม",
            "strengths": "นวัตกรรม ความเป็นอิสระ ความคิดริเริ่ม การทำมนุษยธรรม",
            "challenges": "การ rebel ความไม่แน่นอน ความเห็นอกเห็นใจ ความแปลก"
        }
    },
    "Neptune": {
        "en": {
            "core": "Neptune represents your dreams, spirituality, and subconscious. It shows your idealism and artistic sensitivity.",
            "strengths": "Compassion, intuition, spirituality, artistic talent, imagination",
            "challenges": "Illusion, escapism, confusion, addiction, deception"
        },
        "th": {
            "core": "ดาวเนปจูนแทนความฝัน จิตวิญญาณ และจิตใจ แสดงความเป็นอุดมคติและความอ่อนไหวทางศิลปะ",
            "strengths": "ความเมตตา สัญชาตญาณ จิตวิญญาณ พรสวรรค์ทางศิลปะ จินตนาการ",
            "challenges": "ภาพลวง การหลีกหนี ความสับสน การติดยา การหลอกลวง"
        }
    },
    "Pluto": {
        "en": {
            "core": "Pluto represents transformation, power, and rebirth. It shows your hidden talents and deepest desires.",
            "strengths": "Transformation, resilience, power, investigation, regeneration",
            "challenges": "Power struggles, obsession, control issues, hidden trauma"
        },
        "th": {
            "core": "ดาวพลูโตแทนการเปลี่ยนแปลง อำนาจ และการเกิดใหม่ แสดงพรสวรรค์ที่ซ่อนเร้นและความปรารถนาที่ลึกซึ้งที่สุด",
            "strengths": "การเปลี่ยนแปลง ความยืดหยุ่น อำนาจ การสืบสวน การฟื้นฟู",
            "challenges": "การต่อสู้เพื่ออำนาจ ความหมกมุ่น ปัญหาการควบคุม บาดแผลที่ซ่อนเร้น"
        }
    }
}

# ============== House Meanings ==============
HOUSE_MEANINGS = {
    1: {"en": "Self, Appearance, First Impressions", "th": "ตัวตน รูปลักษณา ความประทับใจแรก"},
    2: {"en": "Values, Possessions, Money", "th": "คุณค่า ทรัพย์สิน เงิน"},
    3: {"en": "Communication, Siblings, Short Travel", "th": "การสื่อสาร พี่น้อง การเดินทางใกล้"},
    4: {"en": "Home, Family, Roots", "th": "บ้าน ครอบครัว รากเหง้า"},
    5: {"en": "Creativity, Children, Romance", "th": "ความคิดสร้างสรรค์ เด็ก ความรัก"},
    6: {"en": "Work, Health, Service", "th": "การทำงาน สุขภาพ การรับใช้"},
    7: {"en": "Partnerships, Marriage, Relationships", "th": "หุ้นส่วน การแต่งงาน ความสัมพันธ์"},
    8: {"en": "Transformation, Shared Resources, Death", "th": "การเปลี่ยนแปลง ทรัพย์สินร่วม ความตาย"},
    9: {"en": "Philosophy, Travel, Higher Education", "th": "ปรัชญา การเดินทาง การศึกษาระดับสูง"},
    10: {"en": "Career, Reputation, Achievement", "th": "อาชีพ ชื่อเสียง ความสำเร็จ"},
    11: {"en": "Friendships, Groups, Hopes", "th": "มิตรภาพ กลุ่ม ความหวัง"},
    12: {"en": "Hidden Things, Subconscious, Isolation", "th": "สิ่งที่ซ่อนเร้น จิตใต้สำนึก ความโดดเดี่ยว"}
}

# ============== Aspect Interpretations ==============
ASPECT_MEANINGS = {
    ("Sun", "Moon", "Conjunction"): {
        "en": "Strong core identity with balanced emotional expression. You have clarity about who you are.",
        "th": "ตัวตนที่แข็งแกร่งพร้อมการแสดงอารมณ์ที่สมดุล คุณรู้ว่าตัวเองเป็นใคร"
    },
    ("Sun", "Moon", "Opposition"): {
        "en": "Tension between your identity and emotions. You may seek balance between your inner self and how you present to the world.",
        "th": "ความตึงเครียดระหว่างตัวตนและอารมณ์ คุณอาจแสวงหาความสมดุลระหว่างตัวเองภายในและการนำเสนอต่อโลก"
    },
    ("Sun", "Moon", "Square"): {
        "en": "Inner conflict between your identity and emotional needs. This creates drive but can cause frustration.",
        "th": "ความขัดแย้งภายในระหว่างตัวตนและความต้องการทางอารมณ์ สิ่งนี้สร้างแรงผลักดันแต่อาจทำให้หงุดหงิด"
    },
    ("Sun", "Moon", "Trine"): {
        "en": "Harmonious relationship between your core self and emotions. You understand yourself well and are emotionally mature.",
        "th": "ความสัมพันธ์ที่กลมกลืนระหว่างตัวตนหลักและอารมณ์ คุณเข้าใจตัวเองดีและโตเป็นทางอารมณ์"
    },
    ("Sun", "Mercury", "Conjunction"): {
        "en": "Sharp mind with clear communication. You express yourself well and think quickly.",
        "th": "จิตใจคมกริบพร้อมการสื่อสารที่ชัดเจน คุณแสดงออกได้ดีและคิดเร็ว"
    },
    ("Sun", "Venus", "Conjunction"): {
        "en": "Charming personality with love of beauty. You attract others with warmth and grace.",
        "th": "บุคลิกน่าหลงใหลพร้อมความรักในความงาม คุณดึงดูดผู้อื่นด้วยความอบอุ่นและความสง่างาม"
    },
    ("Sun", "Mars", "Conjunction"): {
        "en": "Dynamic energy with strong drive. You go after what you want with passion and courage.",
        "th": "พลังงานที่มีชีวิตชีวาพร้อมความขยันที่แข็งแกร่ง คุณไล่ตามสิ่งที่ต้องการด้วยความหลงใหลและความกล้า"
    },
    ("Sun", "Saturn", "Conjunction"): {
        "en": "Strong sense of responsibility and discipline. You achieve through hard work and perseverance.",
        "th": "ความรู้สึกที่แข็งแกร่งเรื่องความรับผิดชอบและวินัย คุณบรรลุเป้าหมายผ่านความขยันและความอดทน"
    },
    ("Moon", "Venus", "Conjunction"): {
        "en": "Nurturing nature with strong emotional values. You seek harmony in relationships.",
        "th": "ธรรมชาติที่ดูแลพร้อมคุณค่าทางอารมณ์ที่แข็งแกร่ง คุณแสวงหาความกลมกลืนในความสัมพันธ์"
    },
    ("Mars", "Venus", "Conjunction"): {
        "en": "Passionate romantic nature. You express love with energy and desire.",
        "th": "ธรรมชาติโรแมนติกที่หลงใหล คุณแสดงความรักด้วยพลังงานและความปรารถนา"
    },
    ("Jupiter", "Saturn", "Square"): {
        "en": "Tension between expansion and restriction. You struggle between growth and boundaries.",
        "th": "ความตึงเครียดระหว่างการขยายตัวและการจำกัด คุณดิ้นรนระหว่างการเติบโตและขอบเขต"
    }
}

# ============== Sign Traits ==============
SIGN_TRAITS = {
    "Aries": {"en": "Pioneering, brave, competitive", "th": "ผู้นำ กล้าหาญ แข่งขัน"},
    "Taurus": {"en": "Patient, reliable, enjoy pleasures", "th": "อดทน ซื่อสัตย์ ชอบสุข"},
    "Gemini": {"en": "Curious, communicative, adaptable", "th": "อยากรู้ สื่อสาร ปรับตัว"},
    "Cancer": {"en": "Nurturing, intuitive, protective", "th": "ดูแล มีสัญญาณ ปกป้อง"},
    "Leo": {"en": "Confident, generous, creative", "th": "มั่นใจ ใจกว้าง สร้างสรรค์"},
    "Virgo": {"en": "Analytical, practical, helpful", "th": "วิเคราะห์ จริงจัง ช่วยเหลือ"},
    "Libra": {"en": "Diplomatic, fair, artistic", "th": "ทูต ยุติธรรม ศิลปะ"},
    "Scorpio": {"en": "Passionate, resourceful, determined", "th": "หลงใหล มีไหวพริบ มุ่งมั่น"},
    "Sagittarius": {"en": "Optimistic, adventurous, honest", "th": "มองโลกในแง่ดี ชอบผจญภัย ซื่อสัตย์"},
    "Capricorn": {"en": "Ambitious, disciplined, patient", "th": "ทะเยอทะยาน มีวินัย อดทน"},
    "Aquarius": {"en": "Independent, original, humanitarian", "th": "เป็นตัวของตัวเอง สร้างสรรค์ มนุษย์"},
    "Pisces": {"en": "Compassionate, artistic, intuitive", "th": "เมตตา ศิลปะ สัญชาตญาณ"}
}


def get_planet_meaning(planet: str, lang: str = "en") -> Dict:
    """Get meaning for a planet"""
    return PLANET_MEANINGS.get(planet, {}).get(lang, PLANET_MEANINGS.get(planet, {}).get("en", {}))


def get_house_meaning(house: int, lang: str = "en") -> str:
    """Get meaning for a house"""
    return HOUSE_MEANINGS.get(house, {}).get(lang, HOUSE_MEANINGS.get(house, {}).get("en", ""))


def get_sign_traits(sign: str, lang: str = "en") -> str:
    """Get traits for a sign"""
    return SIGN_TRAITS.get(sign, {}).get(lang, SIGN_TRAITS.get(sign, {}).get("en", ""))


def generate_birth_chart_reading(
    planets: Dict,
    houses: Dict,
    ascendant: Dict,
    aspects: List[Dict],
    lang: str = "en"
) -> Dict:
    """Generate comprehensive birth chart reading"""
    
    reading = {
        "title": "Your Birth Chart Reading" if lang == "en" else "การอ่านดวงชะตาของคุณ",
        "sections": []
    }
    
    # Section 1: Sun Sign Overview
    sun = planets.get("Sun", {})
    sun_sign = sun.get("sign", "Aries")
    sun_deg = sun.get("degree", 0)
    
    section1 = {
        "title": "☀️ Your Sun Sign" if lang == "en" else "☀️ ราศีเกิดของคุณ",
        "content": f"**{sun_sign}** ({int(sun_deg)}°)"
    }
    section1["traits"] = get_sign_traits(sun_sign, lang)
    section1["meaning"] = get_planet_meaning("Sun", lang)
    reading["sections"].append(section1)
    
    # Section 2: Moon Sign (Emotional Nature)
    moon = planets.get("Moon", {})
    moon_sign = moon.get("sign", "Aries")
    
    section2 = {
        "title": "🌙 Your Moon Sign" if lang == "en" else "🌙 ดวงจันทร์ของคุณ",
        "content": f"**{moon_sign}** ({moon.get('degree', 0):.1f}°)"
    }
    section2["meaning"] = get_planet_meaning("Moon", lang)
    reading["sections"].append(section2)
    
    # Section 3: Ascendant (First Impressions)
    asc_sign = ascendant.get("sign", "Aries")
    asc_deg = ascendant.get("degree", 0)
    
    section3 = {
        "title": "↑ Your Rising Sign" if lang == "en" else "↑ ราศีขึ้นของคุณ",
        "content": f"**{asc_sign}** ({asc_deg:.1f}°)"
    }
    section3["traits"] = get_sign_traits(asc_sign, lang)
    reading["sections"].append(section3)
    
    # Section 4: Planetary Dominance
    section4 = {
        "title": "🪐 Planetary Emphasis" if lang == "en" else "🪐 ดาวเคราห์ที่โดดเด่น",
        "content": [],
        "planets": []
    }
    
    # Find planets in angles (1st, 4th, 7th, 10th houses)
    angle_houses = {1, 4, 7, 10}
    for planet_name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if planet_name in planets:
            planet_sign = planets[planet_name].get("sign", "Aries")
            section4["planets"].append({
                "name": planet_name,
                "sign": planet_sign,
                "traits": get_planet_meaning(planet_name, lang)
            })
    reading["sections"].append(section4)
    
    # Section 5: House Themes
    section5 = {
        "title": "🏠 Life House Themes" if lang == "en" else "🏠 ธีมเรือนชีวิต",
        "content": [],
        "houses": []
    }
    
    # Find planets in houses
    for planet_name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if planet_name in planets:
            # Simplified: use sign to estimate house (not accurate but workable)
            section5["houses"].append({
                "planet": planet_name,
                "sign": planets[planet_name].get("sign", "Aries")
            })
    reading["sections"].append(section5)
    
    # Section 6: Key Aspects
    section6 = {
        "title": "🔗 Key Aspects" if lang == "en" else "🔗 มุมสำคัญ",
        "content": [],
        "aspects": []
    }
    
    major_aspects = ["Conjunction", "Opposition", "Square", "Trine"]
    for asp in aspects:
        if asp.get("type") in major_aspects:
            key = (asp.get("p1", ""), asp.get("p2", ""), asp.get("type", ""))
            asp_text = ASPECT_MEANINGS.get(key, {}).get(lang, ASPECT_MEANINGS.get(key, {}).get("en", ""))
            if asp_text:
                section6["aspects"].append({
                    "p1": asp.get("p1", ""),
                    "p2": asp.get("p2", ""),
                    "type": asp.get("type", ""),
                    "meaning": asp_text
                })
    reading["sections"].append(section6)
    
    # Section 7: Life Theme Summary
    section7 = {
        "title": "✨ Your Life Theme" if lang == "en" else "✨ ธีมชีวิตของคุณ",
        "content": "",
        "theme": ""
    }
    
    # Generate theme based on element distribution
    elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
    sign_elements = {
        "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
        "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
        "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
        "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
    }
    
    for planet_name in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if planet_name in planets:
            sign = planets[planet_name].get("sign", "Aries")
            elem = sign_elements.get(sign, "Fire")
            elements[elem] += 1
    
    dominant_element = max(elements, key=elements.get)
    
    element_messages = {
        "Fire": {
            "en": "You have a dynamic, enthusiastic spirit. Your life path involves taking initiative and expressing yourself boldly.",
            "th": "คุณมีวิญญาณที่มีชีวิตชีวาและกระตือรือร้น เส้นทางชีวิตของคุณเกี่ยวข้องกับการริเริ่มและการแสดงออกอย่างกล้าหาญ"
        },
        "Earth": {
            "en": "You are practical and grounded. Your life path involves building stability and achieving tangible results.",
            "th": "คุณเป็นคนจริงจังและหนักแน่น เส้นทางชีวิตของคุณเกี่ยวข้องกับการสร้างความมั่นคงและการบรรลุผลลัพธ์ที่จับต้องได้"
        },
        "Air": {
            "en": "You are intellectual and social. Your life path involves learning, communicating, and connecting with others.",
            "th": "คุณเป็นคนฉลาดและเข้าสังคม เส้นทางชีวิตของคุณเกี่ยวข้องกับการเรียนรู้ การสื่อสาร และการเชื่อมต่อกับผู้อื่น"
        },
        "Water": {
            "en": "You are emotional and intuitive. Your life path involves emotional growth and connecting on a deep level.",
            "th": "คุณเป็นคนอารมณ์และมีสัญชาตญาณ เส้นทางชีวิตของคุณเกี่ยวข้องกับการเติบโตทางอารมณ์และการเชื่อมต่อในระดับลึก"
        }
    }
    
    section7["theme"] = element_messages.get(dominant_element, {}).get(lang, element_messages["Fire"]["en"])
    reading["sections"].append(section7)
    
    return reading
