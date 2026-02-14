"""
Enhanced Fortune Reader - Detailed & Precise Predictions
Based on house positions, exact aspects, and retrograde states
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import swisseph as swe
import pytz


# ============== House Meanings ==============
HOUSE_MEANINGS = {
    1: {"en": "Self, identity, appearance, new beginnings", "th": "ตัวตน, อัตลักษณ์, รูปลักษณ์, จุดเริ่มต้นใหม่"},
    2: {"en": "Money, possessions, values, self-worth", "th": "เงิน, ทรัพย์สิน, คุณค่า, คุณค่าในตัวเอง"},
    3: {"en": "Communication, siblings, short travel, learning", "th": "การสื่อสาร, พี่น้อง, การเดินทางใกล้, การเรียนรู้"},
    4: {"en": "Home, family, roots, emotional foundation", "th": "บ้าน, ครอบครัว, รากเหง้า, พื้นฐานทางอารมณ์"},
    5: {"en": "Creativity, romance, children, self-expression", "th": "ความคิดสร้างสรรค์, ความรัก, เด็ก, การแสดงออก"},
    6: {"en": "Work, health, daily routines, service", "th": "งาน, สุขภาพ, กิจวัตรประจำวัน, การรับใช้"},
    7: {"en": "Partnerships, marriage, relationships", "th": "หุ้นส่วน, การแต่งงาน, ความสัมพันธ์"},
    8: {"en": "Transformation, shared resources, intimacy", "th": "การเปลี่ยนแปลง, ทรัพย์สินร่วม, ความใกล้ชิด"},
    9: {"en": "Philosophy, travel, higher education, spirituality", "th": "ปรัชญา, การเดินทางไกล, การศึกษาระดับสูง, จิตวิญญาณ"},
    10: {"en": "Career, reputation, public image, authority", "th": "อาชีพ, ชื่อเสียง, ภาพลักษณ์, อำนาจ"},
    11: {"en": "Friendships, groups, hopes, wishes", "th": "มิตรภาพ, กลุ่ม, ความหวัง, ความปรารถนา"},
    12: {"en": "Subconscious, hidden things, solitude, healing", "th": "จิตใจ, สิ่งซ่อนเร้น, ความสันโดษ, การเยียวยา"}
}

# ============== Planet in Signs Meanings ==============
PLANET_IN_SIGN = {
    "Sun": {
        "Aries": {"en": "Natural leader, pioneering spirit, independent, energetic", "th": "ผู้นำตามธรรมชาติ, จิตวิญญาณผู้บุกเบิก, เป็นอิสระ, มีพลัง"},
        "Taurus": {"en": "Stable, reliable, enjoys pleasures, stubborn", "th": "มั่นคง, น่าเชื่อถือ, ชอบสุขสบาย, ดื้อรั้น"},
        "Gemini": {"en": "Curious, communicative, versatile, scattered", "th": "อยากรู้, สื่อสารเก่ง, หลากหลาย, คิดกระจัด"},
        "Cancer": {"en": "Nurturing, emotional, protective, moody", "th": "ดูแล, อารมณ์, ปกป้อง, อารมณ์แปรปรวน"},
        "Leo": {"en": "Confident, creative, dramatic, proud", "th": "มั่นใจ, สร้างสรรค์, โอ่อ่า, ภาคภูมิใจ"},
        "Virgo": {"en": "Analytical, practical, detail-oriented, critical", "th": "วิเคราะห์, จริงจัง, ใส่ใจรายละเอียด, ชอบวิจารณ์"},
        "Libra": {"en": "Diplomatic, balanced, social, indecisive", "th": "สร้างสมดุล, สมดุล, เข้าสังคม, ตัดสินใจยาก"},
        "Scorpio": {"en": "Intense, transformative, passionate, secretive", "th": "เข้มข้น, เปลี่ยนแปลง, หลงใหล, ลึกลับ"},
        "Sagittarius": {"en": "Optimistic, adventurous, philosophical, blunt", "th": "มองโลกในแง่ดี, ชอบผจญภัย, มีปรัชญา, พูดตรงๆ"},
        "Capricorn": {"en": "Ambitious, disciplined, responsible, reserved", "th": "มีความทะเยอทะยาน, มีวินัย, รับผิดชอบ, เข้มงวด"},
        "Aquarius": {"en": "Independent, innovative, humanitarian, detached", "th": "เป็นตัวของตัวเอง, นวัตกรรม, มีน้ำใจ, เห็นอกเห็นใจ"},
        "Pisces": {"en": "Intuitive, artistic, compassionate, escapist", "th": "มีสัญชาตญาณ, มีศิลปะ, เมตตา, หลีกหนี"}
    },
    "Moon": {
        "Aries": {"en": "Quick emotions, impulsive reactions, courageous feelings", "th": "อารมณ์เร็ว, ปฏิกิริยาหุนหัน, ความกล้าทางอารมณ์"},
        "Taurus": {"en": "Stable emotions, material security, stubborn feelings", "th": "อารมณ์มั่นคง, ความมั่นคงทางวัตถุ, ดื้อรั้น"},
        "Gemini": {"en": "Changeable moods, curious inner world, mental emotions", "th": "อารมณ์เปลี่ยนแปลง, จิตใจอยากรู้, อารมณ์ทางความคิด"},
        "Cancer": {"en": "Deeply emotional, nurturing, protective, sensitive", "th": "อารมณ์ลึก, ดูแล, ปกป้อง, อ่อนไหว"},
        "Leo": {"en": "Dramatic emotions, need recognition, warm-hearted", "th": "อารมณ์โอ่อ่า, ต้องการการยอมรับ, ใจอบอุ่น"},
        "Virgo": {"en": "Analyzing feelings, practical emotions, critical inner voice", "th": "วิเคราะห์อารมณ์, อารมณ์จริงจัง, เสียงวิจารณ์ภายใน"},
        "Libra": {"en": "Harmonious emotions, relationship-focused, indecisive", "th": "อารมณ์กลมกลืน, เน้นความสัมพันธ์, ตัดสินใจยาก"},
        "Scorpio": {"en": "Intense emotions, transformative, private, suspicious", "th": "อารมณ์เข้มข้น, เปลี่ยนแปลง, เป็นส่วนตัว, ช่างสงสัย"},
        "Sagittarius": {"en": "Optimistic emotions, adventurous spirit, restless", "th": "อารมณ์มองโลกในแง่ดี, จิตวิญญาณผจญภัย, ไม่อยู่นิ่ง"},
        "Capricorn": {"en": "Reserved emotions, ambitious, self-disciplined", "th": "อารมณ์เข้มงวด, มีความทะเยอทะยาน, มีวินัยในตัวเอง"},
        "Aquarius": {"en": "Detached emotions, unconventional, humanitarian", "th": "อารมณ์เห็นอกเห็นใจ, ไม่แบบแผน, มนุษย์"},
        "Pisces": {"en": "Highly sensitive, empathetic, intuitive, dreamy", "th": "อ่อนไหวมาก, เห็นอกเห็นใจ, มีสัญชาตญาณ, ฝันกลางวัน"}
    },
    "Mercury": {
        "Aries": {"en": "Direct communication, quick thinker, impatient speaker", "th": "สื่อสารตรงๆ, คิดเร็ว, พูดใจร้อน"},
        "Taurus": {"en": "Practical communication, stubborn opinions, slow but steady", "th": "สื่อสารจริงจัง, ความเห็นดื้อรั้น, ช้าแต่มั่น"},
        "Gemini": {"en": "Quick-witted, versatile, talkative, scattered", "th": "คิดเร็ว, หลากหลาย, พูดมาก, กระจัด"},
        "Cancer": {"en": "Emotional communication, intuitive, protective of ideas", "th": "สื่อสารทางอารมณ์, มีสัญชาตญาณ, ปกป้องความคิด"},
        "Leo": {"en": "Dramatic expression, confident, creative communicator", "th": "การแสดงออกโอ่อ่า, มั่นใจ, สื่อสารสร้างสรรค์"},
        "Virgo": {"en": "Analytical, detail-oriented, critical, practical", "th": "วิเคราะห์, ใส่ใจรายละเอียด, วิจารณ์, จริงจัง"},
        "Libra": {"en": "Diplomatic, balanced, harmonious, indecisive", "th": "สร้างสมดุล, สมดุล, กลมกลืน, ตัดสินใจยาก"},
        "Scorpio": {"en": "Intense communication, penetrating, secretive", "th": "สื่อสารเข้มข้น, ทะลุปรุงง, ลึกลับ"},
        "Sagittarius": {"en": "Honest, philosophical, blunt, optimistic", "th": "ซื่อสัตย์, มีปรัชญา, พูดตรง, มองโลกในแง่ดี"},
        "Capricorn": {"en": "Serious communication, ambitious, structured", "th": "สื่อสารจริงจัง, มีความทะเยอทะยาน, มีโครงสร้าง"},
        "Aquarius": {"en": "Original ideas, unconventional, humanitarian", "th": "ความคิดดั้งเดิม, ไม่แบบแผน, มนุษย์"},
        "Pisces": {"en": "Intuitive, artistic, dreamy, impressionable", "th": "มีสัญชาตญาณ, ศิลปะ, ฝันกลางวัน, ประทับใจง่าย"}
    },
    "Venus": {
        "Aries": {"en": "Passionate love, direct flirtation, quick romantic involvements", "th": "รักอย่างลึกซึ้ง, จีบตรงๆ, ความรักเร็ว"},
        "Taurus": {"en": "Sensual love, material comfort, loyal partner", "th": "รักอย่างเย้ายวน, ความสะดวกสบาย, คู่ครองซื่อสัตย์"},
        "Gemini": {"en": "Variety in love, intellectual connection, curious", "th": "ความหลากหลายในความรัก, ความเชื่อมโยงทางความคิด, อยากรู้"},
        "Cancer": {"en": "Nurturing love, emotional security, family-oriented", "th": "รักแบบดูแล, ความมั่นคงทางอารมณ์, เน้นครอบครัว"},
        "Leo": {"en": "Generous love, drama, needs to be admired", "th": "รักอย่างใจกว้าง, โอ่อ่า, ต้องการความชื่นชม"},
        "Virgo": {"en": "Practical love, service-oriented, critical partner", "th": "รักจริงจัง, เน้นการรับใช้, คู่ครองชอบวิจารณ์"},
        "Libra": {"en": "Harmonious relationships, artistic, social", "th": "ความสัมพันธ์กลมกลืน, ศิลปะ, เข้าสังคม"},
        "Scorpio": {"en": "Intense passion, transformative love, jealous", "th": "รักอย่างเข้มข้น, ความรักเปลี่ยนแปลง, หึงหวง"},
        "Sagittarius": {"en": "Adventurous love, freedom-seeking, honest", "th": "รักผจญภัย, ต้องการอิสระ, ซื่อสัตย์"},
        "Capricorn": {"en": "Reserved love, ambitious, long-term commitment", "th": "รักอย่างเข้มงวด, มีความทะเยอทะยาน, ความมุ่งมั่นระยะยาว"},
        "Aquarius": {"en": "Unconventional love, independent, humanitarian", "th": "รักไม่แบบแผน, เป็นอิสระ, มนุษย์"},
        "Pisces": {"en": "Romantic love, compassionate, escapist", "th": "รักโรแมนติก, เมตตา, หลีกหนี"}
    },
    "Mars": {
        "Aries": {"en": "Bold action, competitive, quick to anger", "th": "ลงมือทำกล้าหาญ, แข่งขัน, โกรธเร็ว"},
        "Taurus": {"en": "Steady energy, stubborn pursuit, sensual", "th": "พลังมั่นคง, ไล่ตามอย่างดื้อรั้น, เย้ายวน"},
        "Gemini": {"en": "Quick action, scattered energy, mental aggression", "th": "ลงมือทำเร็ว, พลังกระจัด, การก้าวร้าวทางความคิด"},
        "Cancer": {"en": "Defensive action, emotional energy, protective", "th": "ลงมือทำแบบป้องกัน, พลังทางอารมณ์, ปกป้อง"},
        "Leo": {"en": "Dramatic action, confident, generous energy", "th": "ลงมือทำโอ่อ่า, มั่นใจ, พลังใจกว้าง"},
        "Virgo": {"en": "Methodical action, practical, critical worker", "th": "ลงมือทำเป็นระบบ, จริงจัง, วิจารณ์งาน"},
        "Libra": {"en": "Balanced action, diplomatic, avoids conflict", "th": "ลงมือทำสมดุล, สร้างสมดุล, หลีกเลี่ยงความขัดแย้ง"},
        "Scorpio": {"en": "Intense action, determined, powerful", "th": "ลงมือทำเข้มข้น, มุ่งมั่น, ทรงพลัง"},
        "Sagittarius": {"en": "Adventurous action, optimistic, freedom-loving", "th": "ลงมือทำผจญภัย, มองโลกในแง่ดี, รักอิสระ"},
        "Capricorn": {"en": "Ambitious action, disciplined, patient", "th": "ลงมือทำมุ่งมั่น, มีวินัย, อดทน"},
        "Aquarius": {"en": "Rebellious action, innovative, independent", "th": "ลงมือทำแบบกบฏ, นวัตกรรม, เป็นอิสระ"},
        "Pisces": {"en": "Gentle action, intuitive, escapist", "th": "ลงมือทำอ่อนโยน, มีสัญชาตญาณ, หลีกหนี"}
    }
}

# ============== Aspect Meanings ==============
ASPECT_MEANINGS = {
    ("Sun", "Moon"): {
        "Conjunction": {"en": "Integration of your core identity with emotional nature. You feel balanced between being and feeling.", "th": "การบูรณาการตัวตนหลักกับธรรมชาติทางอารมณ์ คุณรู้สึกสมดุลระหว่างการเป็นและการรู้สึก"},
        "Square": {"en": "Tension between your identity and emotions. Inner conflict drives growth but can cause mood swings.", "th": "ความตึงเครียดระหว่างตัวตนและอารมณ์ ความขัดแย้งภายในผลักดันให้เติบโตแต่อาจทำให้อารมณ์แปรปรวน"},
        "Trine": {"en": "Harmonious flow between identity and emotions. Natural ease in expressing who you are.", "th": "การไหลอย่างกลมกลืนระหว่างตัวตนและอารมณ์ ความง่ายในการแสดงออกว่าคุณเป็นใคร"},
        "Opposition": {"en": "You seek balance between self and relationships. Can feel pulled in two directions.", "th": "คุณแสวงหาสมดุลระหว่างตัวเองและความสัมพันธ์ อาจรู้สึกถูกดึงไปสองทิศทาง"}
    },
    ("Sun", "Mercury"): {
        "Conjunction": {"en": "Your mind and identity work together. Expressive and articulate.", "th": "จิตใจและตัวตนของคุณทำงานร่วมกัน สามารถแสดงออกและพูดได้ชัดเจน"},
        "Square": {"en": "Tension between what you think and who you are. May struggle to communicate your true self.", "th": "ความตึงเครียดระหว่างสิ่งที่คุณคิดกับตัวตนของคุณ อาจต่อสู้เพื่อสื่อสารตัวตนที่แท้จริง"},
        "Trine": {"en": "Easy communication of your identity. You express yourself clearly.", "th": "การสื่อสารตัวตนอย่างง่าย คุณแสดงออกอย่างชัดเจน"}
    },
    ("Sun", "Venus"): {
        "Conjunction": {"en": "Charming personality, attracts others easily. Values harmony and beauty.", "th": "บุคลิกเสน่ห์, ดึงดูดคนอื่นได้ง่าย ให้คุณค่ากับความกลมกลืนและความงาม"},
        "Trine": {"en": "Natural grace and charm. Relationships flow easily.", "th": "มารยาทและเสน่ห์ตามธรรมชาติ ความสัมพันธ์ไหลลื่น"},
        "Square": {"en": "Tension between love and identity. May struggle between personal desires and relationship needs.", "th": "ความตึงเครียดระหว่างความรักและตัวตน อาจต่อสู้ระหว่างความปรารถนาส่วนตัวและความต้องการในความสัมพันธ์"}
    },
    ("Sun", "Mars"): {
        "Conjunction": {"en": "Energetic, assertive, natural leader. Your drive and identity are aligned.", "th": "มีพลัง, กล้าหาญ, ผู้นำตามธรรมชาติ ความขยันและตัวตนของคุณสอดคล้องกัน"},
        "Square": {"en": "Tension between aggression and identity. May struggle with anger or assertiveness.", "th": "ความตึงเครียดระหว่างความก้าวร้าวและตัวตน อามต่อสู้กับความโกรธหรือความกล้า"},
        "Trine": {"en": "Natural confidence and drive. You take action with ease.", "th": "ความมั่นใจและความขยันตามธรรมชาติ คุณลงมือทำได้ง่าย"}
    },
    ("Moon", "Venus"): {
        "Conjunction": {"en": "Emotional warmth in relationships. Nurturing and loving nature.", "th": "ความอบอุ่นทางอารมณ์ในความสัมพันธ์ ธรรมชาติดูแลและรักใคร่"},
        "Trine": {"en": "Natural emotional harmony. You attract love easily.", "th": "ความกลมกลืนทางอารมณ์ตามธรรมชาติ คุณดึงดูดความรักได้ง่าย"},
        "Square": {"en": "Tension between emotions and love. May struggle with emotional needs vs. relationship desires.", "th": "ความตึงเครียดระหว่างอารมณ์และความรัก อาจต่อสู้กับความต้องการทางอารมณ์ vs ความปรารถนาในความสัมพันธ์"}
    },
    ("Moon", "Mars"): {
        "Conjunction": {"en": "Passionate emotions, quick to act on feelings. Strong drive and desires.", "th": "อารมณ์เข้มข้น, ลงมือทำตามความรู้สึกเร็ว ความขยันและความปรารถนาที่แรงกล้า"},
        "Square": {"en": "Emotional tension, may have angry outbursts. Need to balance emotions and action.", "th": "ความตึงเครียดทางอารมณ์, อาจมีการระเบิดของความโกรธ ต้องสมดุลอารมณ์และการกระทำ"},
        "Trine": {"en": "Emotional drive and action work together. You take action based on your feelings.", "th": "ความขับเคลื่อนทางอารมณ์และการกระทำทำงานร่วมกัน คุณลงมือทำตามความรู้สึก"}
    }
}

# ============== Retrograde Meanings ==============
RETROGRADE_MEANINGS = {
    "Mercury": {"en": "Time for reflection, review, and reassessment. Communication may be misunderstood. Avoid signing contracts or starting new projects.", "th": "เวลาสำหรับการไตร่ตรอง ทบทวน และประเมินใหม่ การสื่อสารอาจถูกเข้าใจผิด หลีกเลี่ยงการลงนามสัญญาหรือเริ่มโครงการใหม่"},
    "Venus": {"en": "Reevaluating relationships and values. Past relationships may resurface. Focus on self-love.", "th": "การประเมินความสัมพันธ์และคุณค่าใหม่ ความสัมพันธ์ในอดีตอาจกลับมา มุ่งเน้นการรักตัวเอง"},
    "Mars": {"en": "Energy directed inward. Passive rather than active. Reassess your goals and desires.", "th": "พลังถูกชี้นำเข้าสู่ภายใน แบบรับมากกว่าทำ ประเมินเป้าหมายและความปรารถนาของคุณใหม่"},
    "Jupiter": {"en": "Reevaluating beliefs and philosophies. May feel limited in expansion. Review your long-term plans.", "th": "การประเมินความเชื่อและปรัชญาใหม่ อาจรู้สึกจำกัดในการขยายตัว ทบทวนแผนระยะยาวของคุณ"},
    "Saturn": {"en": "Lessons from the past resurface. Reassess responsibilities and structure. Delays bring hidden blessings.", "th": "บทเรียนจากอดีตกลับมา ประเมินความรับผิดชอบและโครงสร้างใหม่ ความล่าช้านำพาการอวยพรที่ซ่อนเร้น"},
    "Uranus": {"en": "Unexpected insights from within. Sudden changes in perspective. Embrace inner revolution.", "th": "ข้อมูลเชิงลึกที่ไม่คาดคิดจากภายใน มุมมองเปลี่ยนแปลงกะทันหัน ยอมรับการปฏิวัติภายใน"},
    "Neptune": {"en": "Confusion about dreams and reality. Time for inner spiritual work. Clarify illusions.", "th": "ความสับสนเกี่ยวกับความฝันและความเป็นจริง เวลาสำหรับงานจิตวิญญาณภายใน ชี้แจงภาพลวง"},
    "Pluto": {"en": "Deep inner transformation. Power dynamics being reassessed. Embrace personal power shifts.", "th": "การเปลี่ยนแปลงภายในอย่างลึกซึ้ง พลังถูกประเมินใหม่ ยอมรับการเปลี่ยนแปลงพลังส่วนบุคคล"}
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
        speed = result[0][3]  # Speed to detect retrograde
        sign_num = int(longitude / 30) % 12
        
        planets[name] = {
            'longitude': longitude,
            'sign': signs[sign_num],
            'degree': longitude % 30,
            'sign_num': sign_num,
            'retrograde': speed < 0  # Negative speed = retrograde
        }
    
    return planets


def calculate_transit_aspects(natal_planets: Dict, transit_planets: Dict) -> List[Dict]:
    """Calculate exact aspects between transiting planets and natal planets"""
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
                        'orb': round(abs(diff - deg), 2),
                        'exactness': 'exact' if abs(diff - deg) < 1 else 'close',
                        'transit_sign': t_data['sign'],
                        'natal_sign': n_data['sign'],
                        'transit_degree': round(t_data['degree'], 1),
                        'natal_degree': round(n_data['degree'], 1)
                    })
    
    # Sort by exactness (most exact first)
    aspects.sort(key=lambda x: x['orb'])
    return aspects


def get_house_position(longitude: float, houses: Dict) -> int:
    """Determine which house a planet is in"""
    # Simple house determination based on cusp positions
    cusps = sorted([(h, houses[h]['longitude']) for h in houses], key=lambda x: x[1])
    
    for i in range(len(cusps) - 1):
        if cusps[i][1] <= longitude < cusps[i+1][1]:
            return cusps[i][0]
    
    # Handle wrap-around (last house to first)
    if longitude >= cusps[-1][1] or longitude < cusps[0][1]:
        return cusps[-1][0]
    
    return 1


def generate_detailed_daily_fortune(
    natal_planets: Dict,
    natal_houses: Dict,
    natal_ascendant: Dict,
    timezone: str = "Asia/Bangkok",
    lang: str = "en"
) -> Dict:
    """Generate highly detailed daily fortune based on current transits"""
    
    now = datetime.now(pytz.timezone(timezone))
    today_transits = get_current_transits_for_date(
        now.year, now.month, now.day,
        now.hour, now.minute, timezone
    )
    
    # Calculate exact aspects
    aspects = calculate_transit_aspects(natal_planets, today_transits)
    
    fortune = {
        "date": now.strftime("%Y-%m-%d"),
        "day_name": now.strftime("%A"),
        "title": "Daily Fortune" if lang == "en" else "ดวงประจำวัน",
        "overview": "",
        "major_transits": [],
        "transit_aspects": [],
        "retrograde_effects": [],
        "house_activations": [],
        "lucky": {},
        "recommendations": []
    }
    
    # Get natal Sun sign for lucky elements
    natal_sun = natal_planets.get("Sun", {})
    natal_sign = natal_sun.get("sign", "Aries")
    element = SIGN_ELEMENTS.get(natal_sign, "Fire")
    ruler = SIGN_RULERS.get(natal_sign, "Mars")
    
    # Generate overview based on major transits
    overview_parts = []
    
    # Sun sign transit
    sun_transit = today_transits.get("Sun", {})
    sun_sign = sun_transit.get("sign", "Aries")
    sun_degree = sun_transit.get("degree", 0)
    overview_parts.append(f"Today the Sun is at **{sun_sign} {int(sun_degree)}°**, illuminating your {HOUSE_MEANINGS.get(get_house_position(sun_transit['longitude'], natal_houses), {}).get(lang, 'chart')} house.")
    
    fortune["overview"] = " ".join(overview_parts)
    
    # Major transits with house positions
    for planet in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        if planet in today_transits:
            p = today_transits[planet]
            house = get_house_position(p['longitude'], natal_houses)
            house_meaning = HOUSE_MEANINGS.get(house, {}).get(lang, "unknown area")
            
            planet_in_sign = PLANET_IN_SIGN.get(planet, {}).get(p['sign'], {}).get(lang, "")
            
            transit_info = {
                "planet": planet,
                "sign": p['sign'],
                "degree": f"{p['degree']:.1f}°",
                "house": house,
                "house_meaning": house_meaning,
                "meaning": planet_in_sign,
                "retrograde": p.get('retrograde', False)
            }
            fortune["major_transits"].append(transit_info)
    
    # Detailed aspect interpretations
    for asp in aspects[:8]:
        t_planet = asp['transiting']
        n_planet = asp['natal']
        
        # Get house position of the natal planet being aspected
        n_long = natal_planets.get(n_planet, {}).get('longitude', 0)
        house = get_house_position(n_long, natal_houses)
        house_meaning = HOUSE_MEANINGS.get(house, {}).get(lang, "unknown area")
        
        # Look for specific aspect meaning
        aspect_key = (t_planet, n_planet)
        aspect_meaning = ASPECT_MEANINGS.get(aspect_key, {}).get(asp['type'], {}).get(lang, "")
        
        # Fallback to generic if specific not found
        if not aspect_meaning:
            aspect_meaning = f"The transit of {t_planet} makes a {asp['type']} to your natal {n_planet}."
        
        fortune["transit_aspects"].append({
            "transiting": t_planet,
            "transit_sign": asp['transit_sign'],
            "transit_degree": asp['transit_degree'],
            "aspect": asp['type'],
            "orb": asp['orb'],
            "exactness": asp['exactness'],
            "natal": n_planet,
            "natal_sign": asp['natal_sign'],
            "house_affected": house,
            "house_meaning": house_meaning,
            "interpretation": aspect_meaning
        })
    
    # Retrograde effects
    for planet, data in today_transits.items():
        if data.get('retrograde', False) and planet in RETROGRADE_MEANINGS:
            fortune["retrograde_effects"].append({
                "planet": planet,
                "meaning": RETROGRADE_MEANINGS.get(planet, {}).get(lang, "")
            })
    
    # House activations (which natal houses are being touched by transits)
    activated_houses = set()
    for asp in aspects:
        if asp['natal'] in natal_planets:
            n_long = natal_planets[asp['natal']]['longitude']
            house = get_house_position(n_long, natal_houses)
            activated_houses.add(house)
    
    for house in sorted(activated_houses):
        fortune["house_activations"].append({
            "house": house,
            "meaning": HOUSE_MEANINGS.get(house, {}).get(lang, "")
        })
    
    # Lucky elements
    fortune["lucky"] = {
        "color": LUCKY_COLORS.get(element, {}).get(lang, "All colors"),
        "number": LUCKY_NUMBERS.get(element, {}).get(lang, "All numbers"),
        "day": now.strftime("%A"),
        "element": element
    }
    
    # Personalized recommendations
    recommendations = []
    
    # Based on major aspects
    if any(a['type'] == 'Square' for a in fortune['transit_aspects'][:3]):
        recommendations.append("Challenge aspect detected: This is a time for growth through克服困难. Don't avoid tension - use it as fuel." if lang == "en" else "ตรวจพบมุมท้าทาย: นี่คือเวลาสำหรับการเติบโตผ่านความยากลำบาก อย่าหลีกเลี่ยงความตึงเครียด - ใช้มันเป็นเชื้อเพลิง")
    
    if any(a['type'] == 'Trine' for a in fortune['transit_aspects'][:3]):
        recommendations.append("Harmonious aspect detected: Things flow easily. This is a good day for creative pursuits and relationships." if lang == "en" else "ตรวจพบมุมกลมกลืน: สิ่งต่างๆ ไหลลื่น เป็นวันที่ดีสำหรับการสร้างสรรค์และความสัมพันธ์")
    
    if fortune['retrograde_effects']:
        rec = "Retrograde planets indicate internal focus. Take time for reflection rather than external action." if lang == "en" else "ดาวเคราห์ถอยหลังบ่งชี้ถึงการมุ่งเน้นภายใน ใช้เวลาไตร่ตรองมากกว่าการกระทำภายนอก"
        recommendations.append(rec)
    
    # Based on house activations
    if 1 in activated_houses:
        recommendations.append("Your 1st house is activated: Focus on self-care and new beginnings today." if lang == "en" else "เรือนที่ 1 ของคุณถูกกระตุ้น: มุ่งเน้นการดูแลตัวเองและจุดเริ่มต้นใหม่วันนี้")
    if 7 in activated_houses:
        recommendations.append("Your 7th house is activated: Relationships need attention. Consider partnership dynamics." if lang == "en" else "เรือนที่ 7 ของคุณถูกกระตุ้น: ความสัมพันธ์ต้องการความสนใจ พิจารณาพลวัตของหุ้นส่วน")
    if 10 in activated_houses:
        recommendations.append("Your 10th house is activated: Career matters come forward. Your public image is highlighted." if lang == "en" else "เรือนที่ 10 ของคุณถูกกระตุ้น: เรื่องอาชีพมาโดดเด่น ภาพลักษณ์สาธารณะของคุณถูกเน้น")
    
    fortune["recommendations"] = recommendations
    
    return fortune
