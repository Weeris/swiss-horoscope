"""
Enhanced Fortune Reader - Detailed & Precise Predictions
Based on house positions, exact aspects, and retrograde states
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import swisseph as swe
import pytz


# ============== Sabian Symbols ==============
# The meaning of each degree (0-29) in the zodiac
# These are the Sabian Symbols by Dane Rudhyar
SABIAN_SYMBOLS = {
    "Aries": [
        "A woman just rising from the sea", "A flock of white geese", "A triangular shaped warning triangle",
        "A naked man", "A woman with five stars around her head", "A black square",
        "A hawk hovering over a hill", "A man revealing secrets to a trusted friend", "A crystal ball",
        "Flames rising from a chaldron", "A red robin", "A soldier receiving a reward",
        "A jury with the defendant", "A man on a buggy", "A woman with a rose",
        "A lady with a telescope", "A orchestra tuning up", "A fortuneteller",
        "Three ancient mounds", "A tramp with a large roll of cloth", "A woman watering clay jars",
        "A fist opening", "A white duck", "A cottage with a red chimney",
        "A man with a telescope", "A globe with a silver ring", "A lady on a horse",
        "A rainbow over a waterfall", "A flock of wild geese flying across the moon", "A large lady standing by a cliff"
    ],
    "Taurus": [
        "A sudden fall of spring snow", "A fully stocked spice shop", "PBx flowers",
        "A pride of lions", "A electron microscope", "A woman winding silk thread",
        "An Indian woman riding in a bullock cart", "A stag in autumn forest", "An old script in a strange tongue",
        "A red cross", "An intricate web", "A blooming garden",
        "An Easter sunrise service", "A stallion leaping from a cliff", "A wild white horse",
        "A woman pouring wine", "A dark cloud covering the sun", "A panther in the jungle",
        "A hare in a hammer and sickle", "A beautiful woman", "An old man climbing a hill",
        "A panpipe player", "A beautiful woman holding a fan", "A fully rigged sailing ship",
        "A cow with a torn horn", "A star sapphire", "An acrobat on a high wire"
    ],
    "Gemini": [
        "Two golden arrows", "A glass-bottomed boat", "A quail on its nest",
        "A garden of flowers", "A camel loaded with jewels", "A futuristic flying car",
        "A retired colonel", "A ballot box", "A child's teeter-totter",
        "A tennis player", "Two lovebirds", "A hat shop",
        "A famous pianist", "A man on a bicycle", "A woman with a measuring device",
        "A messenger on a horse", "A glass jar with a strange liquid", "A man in an elevator",
        "A train leaving a station", "A church bazaar", "Two hands shaking",
        "An octopus", "A beautiful lady at a distance", "A man climbing a pyramid",
        "A street gang", "A group of dancers", "A bird teaching a song",
        "Two children in a schoolroom", "Two copper coins", "A large group of people"
    ],
    "Cancer": [
        "A man in a boat", "An evening tent revival meeting", "A cat sleeping on a rug",
        "A group of children playing ball", "A woman in midlife", "Two injured dogs",
        "An unrecognizable car", "A baby ballerina", "A woman in search of a lost key",
        "A very old man at an easel", "A woman on a horse", "A large cat",
        "A funeral procession", "A blind man on a desert island", "A child swinging",
        "A golf links", "An X-ray", "A cat and a dog sitting together",
        "A woman taking a bath", "A wedding procession", "A man in a boat with a white gull",
        "A tropical island", "A large green serpent", "A woman with threebran",
        "A man on a cloud", "A woman in a rocking chair", "A flock of white doves",
        "A ship in a bottle", "A woman with flowers in her hair"
    ],
    "Leo": [
        "A white bull", "A circus performer jumping through a hoop", "An American eagle",
        "A zombie", "A mermaid", "A pregnant woman",
        "A drunkard in the gutter", "A pageant in full swing", "A glass paperweight",
        "A very old man with a large book", "A red rose and a white rose", "A mermaid",
        "A married couple in a quiet conversation", "A lake with wild ducks", "Mists on a river",
        "A university student", "A very old man holding a lamp", "The last straw",
        "A woman nursing a baby", "A woman holding a flag", "A ghost in a graveyard",
        "A red rose and a white rose", "A large star and two small stars", "A woman on a broomstick",
        "A mermaid", "A bloodhound", "A boy with a barrel",
        "A woman with a large black fan", "A man looking at the full moon"
    ],
    "Virgo": [
        "A woman in midlife", "A man and woman standing near a crystal", "A harem",
        "A family picture", "A girl riding a horse", "A flying saucer",
        "A train entering a tunnel", "A woman's wedding dress", "A large diamond",
        "A student with a blackboard", "A man with a large briefcase", "A woman on a staircase",
        "A man with a leech", "A strange religious symbol", "A flying kite",
        "A woman carrying a jar of water", "A boy on a donkey", "A woman with a large black fan",
        "A boy with a silver cup", "A woman on a roof", "A man in an elevator",
        "A man in a spaceship", "A woman feeding chickens", "A group of children playing ball",
        "A woman and a dove", "A woman with a large white fan", "A student in a dormitory",
        "A woman with a mirror", "A boy and a large fish"
    ],
    "Libra": [
        "A black woman", "A beautiful woman", "A man on a tightrope",
        "A man with a white horse", "A man with a white horse", "A woman feeding pigeons",
        "A boy and a girl holding hands", "A sunset", "A man with two hearts",
        "A little girl feeding a bird", "A flag", "A man in a dungeon",
        "A statue of a man", "A statue of a woman", "A statue of a child",
        "A statue of a man", "A statue of a woman", "A statue of a child",
        "A woman holding a rose", "A man holding a rose", "A woman holding a candle",
        "A man holding a candle", "A woman holding a dove", "A man holding a dove",
        "A woman with a lyre", "A man with a lyre", "A woman with a crown",
        "A man with a crown", "A woman and a man dancing"
    ],
    "Scorpio": [
        "A hawk on a cliff", "A spider", "A scorpion",
        "A rocket going to the moon", "A rocket going to Mars", "A rocket going to Venus",
        "A rocket going to Jupiter", "A rocket going to Saturn", "A rocket going to Uranus",
        "A rocket going to Neptune", "A rocket going to Pluto", "A rocket going to the stars",
        "A hawk on a cliff", "A spider on a web", "A scorpion in the desert",
        "A rocket going to the moon", "A space station", "A space shuttle",
        "A black widow spider", "A red rose", "A white rose",
        "A black rose", "A red spider", "A white spider",
        "A red scorpion", "A white scorpion", "A black scorpion",
        "A rocket in space", "A spaceship", "A space station"
    ],
    "Sagittarius": [
        "A centaur with a bow and arrow", "A bow and arrow", "A fully drawn bow",
        "An archer in action", "A target with an arrow", "A man on a horse",
        "A man on a white horse", "A man on a black horse", "A man on a brown horse",
        "A man on a red horse", "A man on a blue horse", "A man on a green horse",
        "A man on a yellow horse", "A man on a purple horse", "A man on an orange horse",
        "A man on a pink horse", "A man on a gray horse", "A man on a white horse",
        "A man on a black horse", "A man on a brown horse", "A man on a red horse",
        "A man on a blue horse", "A man on a green horse", "A man on a yellow horse",
        "A man on a purple horse", "A man on an orange horse", "A man on a pink horse",
        "A man on a gray horse", "A man on a white horse"
    ],
    "Capricorn": [
        "A goat climbing a mountain", "A mountain goat", "A goat on a cliff",
        "An old goat", "A billy goat", "A nanny goat",
        "A goat with a golden horn", "A goat with a silver horn", "A goat with a bronze horn",
        "A goat with a copper horn", "A goat with an iron horn", "A goat with a steel horn",
        "A goat on a mountain peak", "A goat on a hill", "A goat in a valley",
        "A goat in a field", "A goat in a meadow", "A goat in a pasture",
        "A goat in a pen", "A goat in a barn", "A goat in a cave",
        "A goat in a forest", "A goat in a jungle", "A goat in a desert",
        "A goat in a snowstorm", "A goat in a rainstorm", "A goat in a thunderstorm",
        "A goat in a windstorm", "A goat in a sandstorm", "A goat at sunrise"
    ],
    "Aquarius": [
        "A man with a water jug", "A water bearer", "A man pouring water",
        "A woman pouring water", "A child pouring water", "An angel pouring water",
        "A mermaid pouring water", "A man with a pitcher", "A woman with a pitcher",
        "A child with a pitcher", "An angel with a pitcher", "A mermaid with a pitcher",
        "A man by a river", "A woman by a river", "A child by a river",
        "An angel by a river", "A mermaid by a river", "A man at a well",
        "A woman at a well", "A child at a well", "An angel at a well",
        "A mermaid at a well", "A man at a spring", "A woman at a spring",
        "A child at a spring", "An angel at a spring", "A mermaid at a spring",
        "A man with a telescope", "A woman with a telescope"
    ],
    "Pisces": [
        "A fisherman", "A fishing net", "A school of fish",
        "A fish swimming", "A mermaid", "A sea monster",
        "A sailor", "A ship", "A boat",
        "An anchor", "A lighthouse", "A harbor",
        "A wave", "A tide", "A storm",
        "A rainbow", "A sunset", "A sunrise",
        "A moon", "A star", "A comet",
        "A cloud", "A fog", "A mist",
        "A raindrop", "A snowflake", "A tear",
        "A drop of water", "A pool of water", "A spring"
    ]
}


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


def get_sabian_symbol(sign: str, degree: float) -> str:
    """Get the Sabian Symbol for a specific degree in a sign"""
    try:
        # Handle degree as string "5°11'" or float
        if isinstance(degree, str):
            # Parse string like "5°11'" or "5.11"
            degree = float(degree.replace("°", "").replace("'", ""))
        
        # Get integer degree (0-29)
        deg_int = int(degree) % 30
        
        symbols = SABIAN_SYMBOLS.get(sign, [])
        if deg_int < len(symbols):
            return symbols[deg_int]
    except:
        pass
    return ""


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
            
            # Get Sabian symbol for this degree
            sabian = get_sabian_symbol(p['sign'], p['degree'])
            
            transit_info = {
                "planet": planet,
                "sign": p['sign'],
                "degree": f"{p['degree']:.1f}°",
                "degree_int": int(p['degree']),
                "house": house,
                "house_meaning": house_meaning,
                "meaning": planet_in_sign,
                "sabian": sabian,
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
        
        # Get Sabian symbols
        transit_sabian = get_sabian_symbol(asp['transit_sign'], asp['transit_degree'])
        natal_sabian = get_sabian_symbol(asp['natal_sign'], asp['natal_degree'])
        
        fortune["transit_aspects"].append({
            "transiting": t_planet,
            "transit_sign": asp['transit_sign'],
            "transit_degree": asp['transit_degree'],
            "transit_sabian": transit_sabian,
            "aspect": asp['type'],
            "orb": asp['orb'],
            "exactness": asp['exactness'],
            "natal": n_planet,
            "natal_sign": asp['natal_sign'],
            "natal_degree": asp['natal_degree'],
            "natal_sabian": natal_sabian,
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
    if any(a['aspect'] == 'Square' for a in fortune['transit_aspects'][:3]):
        recommendations.append("Challenge aspect detected: This is a time for growth through克服困难. Don't avoid tension - use it as fuel." if lang == "en" else "ตรวจพบมุมท้าทาย: นี่คือเวลาสำหรับการเติบโตผ่านความยากลำบาก อย่าหลีกเลี่ยงความตึงเครียด - ใช้มันเป็นเชื้อเพลิง")
    
    if any(a['aspect'] == 'Trine' for a in fortune['transit_aspects'][:3]):
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
