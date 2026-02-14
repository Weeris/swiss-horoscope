"""
Core astrological calculations using pyswisseph (Swiss Ephemeris)
"""

import swisseph as swe
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import pytz


# Planet constants (Swiss Ephemeris)
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'North Node': swe.TRUE_NODE,
    'South Node': swe.TRUE_NODE,  # Calculated as opposite to North Node
}

# Signs
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGNS_TH = [
    "เมษะ", "พฤษภะ", "มิถุนะ", "กรกฏะ", "สิงหะ", "กันยะ",
    "ตุลยะ", "พิจิกะ", "ธนุ", "มู่คัส", "วัวป่า", "มีนะ"
]

# Aspects
ASPECTS = {
    0: ("Conjunction", 0),
    60: ("Sextile", 6),
    90: ("Square", 8),
    120: ("Trine", 10),
    180: ("Opposition", 12)
}


class SwissEphemerisCalculator:
    """High-precision astrological calculations using Swiss Ephemeris"""
    
    def __init__(self, ephe_path: str = None):
        """Initialize calculator"""
        if ephe_path:
            swe.set_ephe_path(ephe_path)
        else:
            # Try default path
            swe.set_ephe_path('/Users/weeris/.openclaw/workspace/projects/swiss_horoscope/data/ephe')
        
        # Set standard flags (high precision)
        self.flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    
    def jd_from_datetime(self, dt: datetime) -> float:
        """Convert datetime to Julian Day"""
        # If datetime is naive, assume UTC
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        
        # Convert to Unix time and then to JD
        unix = dt.timestamp()
        jd = 2440587.5 + unix / 86400.0
        return jd
    
    def get_planet_position(self, jd: float, planet_id: int) -> Dict:
        """Get position of a single planet"""
        result = swe.calc_ut(jd, planet_id, self.flags)
        
        longitude = result[0][0]  # Ecliptic longitude
        latitude = result[0][1]  # Ecliptic latitude
        distance = result[0][2]   # Distance in AU
        speed = result[0][3]     # Speed in longitude
        
        # Determine sign
        sign_index = int(longitude / 30) % 12
        degree_in_sign = longitude % 30
        
        # Retrograde
        retrograde = speed < 0
        
        return {
            'longitude': longitude,
            'latitude': latitude,
            'distance': distance,
            'speed': speed,
            'sign': SIGNS[sign_index],
            'sign_th': SIGNS_TH[sign_index],
            'degree': degree_in_sign,
            'sign_num': sign_index,
            'retrograde': retrograde
        }
    
    def get_ascendant(self, jd: float, latitude: float, longitude: float) -> Dict:
        """Calculate Ascendant using house cusps"""
        # Get house cusps
        hsys = b'P'  # Placidus
        cusps, ascmc = swe.houses(jd, latitude, longitude, hsys)
        
        asc_longitude = ascmc[0]  # Ascendant longitude
        
        sign_index = int(asc_longitude / 30) % 12
        degree_in_sign = asc_longitude % 30
        
        return {
            'longitude': asc_longitude,
            'sign': SIGNS[sign_index],
            'sign_th': SIGNS_TH[sign_index],
            'degree': degree_in_sign,
            'sign_num': sign_index
        }
    
    def get_midheaven(self, jd: float, latitude: float, longitude: float) -> Dict:
        """Calculate Midheaven (MC) using house cusps"""
        hsys = b'P'  # Placidus
        cusps, ascmc = swe.houses(jd, latitude, longitude, hsys)
        
        mc_longitude = ascmc[1]  # Midheaven longitude
        
        sign_index = int(mc_longitude / 30) % 12
        degree_in_sign = mc_longitude % 30
        
        return {
            'longitude': mc_longitude,
            'sign': SIGNS[sign_index],
            'sign_th': SIGNS_TH[sign_index],
            'degree': degree_in_sign,
            'sign_num': sign_index
        }
    
    def get_houses(self, jd: float, latitude: float, longitude: float) -> Dict:
        """Get all 12 house cusps"""
        hsys = b'P'  # Placidus
        cusps, ascmc = swe.houses(jd, latitude, longitude, hsys)
        
        houses = {}
        for i in range(12):
            cusp_longitude = cusps[i]
            sign_index = int(cusp_longitude / 30) % 12
            degree_in_sign = cusp_longitude % 30
            
            houses[i + 1] = {
                'longitude': cusp_longitude,
                'sign': SIGNS[sign_index],
                'sign_th': SIGNS_TH[sign_index],
                'degree': degree_in_sign,
                'sign_num': sign_index
            }
        
        return houses
    
    def get_aspects(self, positions: Dict, orb_limit: float = 8.0) -> List[Dict]:
        """Calculate aspects between planets"""
        aspects = []
        planets = list(positions.keys())
        
        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                long1 = positions[p1]['longitude']
                long2 = positions[p2]['longitude']
                
                # Calculate angular distance
                diff = abs(long1 - long2)
                if diff > 180:
                    diff = 360 - diff
                
                # Check each aspect
                for aspect_deg, (aspect_name, max_orb) in ASPECTS.items():
                    orb = abs(diff - aspect_deg)
                    if orb <= max_orb:
                        aspects.append({
                            'p1': p1,
                            'p2': p2,
                            'type': aspect_name,
                            'angle': aspect_deg,
                            'orb': orb,
                            'exact': orb < 1.0
                        })
        
        # Sort by orb (most exact first)
        aspects.sort(key=lambda x: x['orb'])
        
        return aspects
    
    def calculate_all(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        timezone: str = "Asia/Bangkok"
    ) -> Dict:
        """Calculate full birth chart"""
        # Create datetime
        dt = datetime(year, month, day, hour, minute)
        
        # Convert to UTC from timezone
        try:
            tz = pytz.timezone(timezone)
            dt_local = tz.localize(dt)
            dt_utc = dt_local.astimezone(pytz.utc)
        except:
            # Fallback: assume local = UTC offset
            dt_utc = dt
        
        # Get Julian Day
        jd = self.jd_from_datetime(dt_utc)
        
        # Calculate all planet positions
        positions = {}
        for name, planet_id in PLANETS.items():
            pos = self.get_planet_position(jd, planet_id)
            positions[name] = pos
        
        # Calculate North/South Node (opposite)
        if 'North Node' in positions:
            nn_long = positions['North Node']['longitude']
            positions['South Node'] = {
                'longitude': (nn_long + 180) % 360,
                'sign': SIGNS[int((nn_long + 180) / 30) % 12],
                'sign_th': SIGNS_TH[int((nn_long + 180) / 30) % 12],
                'degree': (nn_long + 180) % 30,
                'sign_num': int((nn_long + 180) / 30) % 12,
                'retrograde': True
            }
        
        # Calculate houses
        asc = self.get_ascendant(jd, latitude, longitude)
        mc = self.get_midheaven(jd, latitude, longitude)
        houses = self.get_houses(jd, latitude, longitude)
        
        # Calculate aspects
        aspects = self.get_aspects(positions)
        
        return {
            'subject': {
                'name': 'User',
                'date_time': f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
                'latitude': latitude,
                'longitude': longitude,
                'timezone': timezone,
                'jd': jd
            },
            'planets': positions,
            'ascendant': asc,
            'midheaven': mc,
            'houses': houses,
            'aspects': aspects
        }
    
    def get_zodiac_sign(self, month: int, day: int) -> Tuple[str, str]:
        """Quick Western zodiac lookup (for simple sun sign)"""
        dates = [
            (1, 19, 11), (2, 18, 0), (3, 20, 1), (4, 19, 2),
            (5, 20, 3), (6, 20, 4), (7, 22, 5), (8, 22, 6),
            (9, 22, 7), (10, 22, 8), (11, 21, 9), (12, 21, 10),
            (12, 31, 11)
        ]
        
        for m, d, sign_idx in dates:
            if (month == m and day >= d) or month < m:
                return SIGNS[sign_idx], SIGNS_TH[sign_idx]
        
        return SIGNS[0], SIGNS_TH[0]
