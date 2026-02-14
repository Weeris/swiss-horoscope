"""
Natal Chart Wheel Visualization using Matplotlib
Supports: Birth Chart, Transit Overlay, Synastry Comparison
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Optional, Tuple
import io
from datetime import datetime
import swisseph as swe
import pytz

# Planet glyphs and colors
PLANET_GLYPHS = {
    'Sun': '☉', 'Moon': '☽', 'Mercury': '☿', 'Venus': '♀', 'Mars': '♂',
    'Jupiter': '♃', 'Saturn': '♄', 'Uranus': '⛢', 'Neptune': '♆',
    'Pluto': '♇', 'North Node': '☊', 'South Node': '☋',
    'Chiron': '⚷', 'Ceres': '⚵', 'Pallas': '⚶', 'Juno': '⚳', 'Vesta': '⚴'
}

PLANET_COLORS = {
    'Sun': '#FFD700', 'Moon': '#C0C0C0', 'Mercury': '#A9A9A9', 'Venus': '#FFA500',
    'Mars': '#FF4500', 'Jupiter': '#DAA520', 'Saturn': '#D2691E', 'Uranus': '#40E0D0',
    'Neptune': '#4169E1', 'Pluto': '#8B4513', 'North Node': '#FF69B4', 'South Node': '#FFB6C1',
    'Chiron': '#9370DB', 'Ceres': '#98FB98', 'Pallas': '#DDA0DD', 'Juno': '#F0E68C', 'Vesta': '#E6E6FA'
}

# Sign colors
SIGN_COLORS = {
    'Aries': '#FF6B6B', 'Taurus': '#4ECDC4', 'Gemini': '#FFE66D', 'Cancer': '#95E1D3',
    'Leo': '#F38181', 'Virgo': '#AA96DA', 'Libra': '#FCBAD3', 'Scorpio': '#A8D8EA',
    'Sagittarius': '#FF9F43', 'Capricorn': '#6C5CE7', 'Aquarius': '#74B9FF', 'Pisces': '#DFE6E9'
}

ELEMENT_COLORS = {
    'Fire': '#FF6B6B', 'Earth': '#4ECDC4', 'Air': '#FFE66D', 'Water': '#74B9FF'
}

# Aspect colors and line styles
ASPECT_CONFIG = {
    'Conjunction': {'color': '#FFFFFF', 'width': 2, 'style': '-'},
    'Opposition': {'color': '#FF6B6B', 'width': 1.5, 'style': '-'},
    'Square': {'color': '#FF4500', 'width': 1.5, 'style': '-'},
    'Trine': {'color': '#4ECDC4', 'width': 1.5, 'style': '-'},
    'Sextile': {'color': '#95E1D3', 'width': 1, 'style': '--'},
}


def normalize_angle(angle: float) -> float:
    """Normalize angle to 0-360 degrees"""
    return angle % 360


def degree_to_chart_coords(longitude: float, radius: float) -> tuple:
    """Convert zodiac longitude to chart coordinates."""
    angle = np.radians(90 - longitude)
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return x, y


def create_chart_wheel(
    planets: Dict,
    houses: Dict,
    ascendant: Dict,
    midheaven: Dict,
    aspects: Optional[List[Dict]] = None,
    show_aspects: bool = True,
    show_houses: bool = True,
    size: tuple = (12, 12)
) -> plt.Figure:
    """Create a natal chart wheel"""
    
    fig, ax = plt.subplots(figsize=size, facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    outer_radius = 1.0
    house_radius = 0.85
    planet_radius = 0.55
    
    # Draw outer ring (signs)
    sign_glyphs = {'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
                   'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
                   'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'}
    
    for i, sign in enumerate(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']):
        start_angle = 90 - i * 30
        wedge = mpatches.Wedge((0, 0), outer_radius, start_angle - 30, start_angle,
                               width=outer_radius - house_radius,
                               facecolor=SIGN_COLORS.get(sign, '#333'),
                               edgecolor='#2d2d44', linewidth=1)
        ax.add_patch(wedge)
        
        angle_rad = np.radians(start_angle - 15)
        glyph_x = (outer_radius - 0.05) * np.cos(angle_rad)
        glyph_y = (outer_radius - 0.05) * np.sin(angle_rad)
        ax.text(glyph_x, glyph_y, sign_glyphs.get(sign, ''), 
                ha='center', va='center', fontsize=8, color='#fff', fontweight='bold')
    
    # Draw house cusps
    if show_houses and houses:
        for house_num in range(1, 13):
            if house_num in houses:
                cusp = houses[house_num]
                long = cusp['longitude']
                x1, y1 = degree_to_chart_coords(long, house_radius)
                x2, y2 = degree_to_chart_coords(long, outer_radius)
                ax.plot([x1, x2], [y1, y2], color='#4a4a6a', linewidth=1, alpha=0.7)
                
                mid_long = (long + 15) % 360
                hx, hy = degree_to_chart_coords(mid_long, (house_radius + outer_radius) / 2)
                ax.text(hx, hy, str(house_num), ha='center', va='center', 
                        fontsize=7, color='#888', fontweight='bold')
        
        circle = plt.Circle((0, 0), house_radius, fill=False, 
                            color='#3d3d5c', linewidth=2, linestyle='-')
        ax.add_patch(circle)
    
    # Draw aspects
    if show_aspects and aspects:
        planet_positions = {p: degree_to_chart_coords(planets[p]['longitude'], planet_radius) 
                           for p in planets if p in planets}
        
        for aspect in aspects[:20]:
            p1, p2 = aspect['p1'], aspect['p2']
            if p1 in planet_positions and p2 in planet_positions:
                config = ASPECT_CONFIG.get(aspect['type'], {'color': '#666', 'width': 1})
                x1, y1 = planet_positions[p1]
                x2, y2 = planet_positions[p2]
                ax.plot([x1, x2], [y1, y2], color=config['color'], 
                       linewidth=config['width'], linestyle=config['style'], alpha=0.6, zorder=1)
    
    # Draw planets
    for planet, data in planets.items():
        long = data['longitude']
        x, y = degree_to_chart_coords(long, planet_radius)
        
        color = PLANET_COLORS.get(planet, '#888')
        circle = plt.Circle((x, y), 0.04, color=color, ec='#fff', linewidth=1, zorder=3)
        ax.add_patch(circle)
        
        glyph = PLANET_GLYPHS.get(planet, '●')
        ax.text(x, y, glyph, ha='center', va='center', fontsize=10, 
                color='#000', fontweight='bold', zorder=4)
        
        name_x, name_y = degree_to_chart_coords(long, planet_radius - 0.12)
        ax.text(name_x, name_y, planet, ha='center', va='center', fontsize=6, color='#ccc', zorder=2)
    
    # Ascendant & Midheaven
    if ascendant:
        asc_long = ascendant['longitude']
        ax.annotate('ASC', xy=degree_to_chart_coords(asc_long, house_radius - 0.08),
                   fontsize=8, color='#00FF00', fontweight='bold', ha='center')
    
    if midheaven:
        mc_long = midheaven['longitude']
        ax.annotate('MC', xy=degree_to_chart_coords(mc_long, house_radius - 0.08),
                   fontsize=8, color='#FFD700', fontweight='bold', ha='center')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Natal Chart', fontsize=14, color='#fff', pad=20, fontweight='bold')
    
    plt.tight_layout()
    return fig


def chart_to_image(fig: plt.Figure) -> bytes:
    """Convert matplotlib figure to PNG bytes"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), 
                edgecolor='none', bbox_inches='tight', dpi=150)
    buf.seek(0)
    return buf.getvalue()


# ============== Transit Overlay ==============

TRANSIT_PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS,
    'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN,
    'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO
}

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


def get_current_transits(timezone: str = "Asia/Bangkok") -> Dict:
    """Calculate current planetary positions (transits)"""
    now = datetime.now(pytz.timezone(timezone))
    jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    
    transits = {}
    for name, planet_id in TRANSIT_PLANETS.items():
        result = swe.calc_ut(jd, planet_id, flags)
        longitude = result[0][0]
        sign_num = int(longitude / 30) % 12
        degree = longitude % 30
        
        transits[name] = {
            'longitude': longitude,
            'sign': SIGNS[sign_num],
            'degree': degree,
            'sign_num': sign_num,
            'speed': result[0][3]
        }
    
    return transits


def create_transit_overlay_chart(
    natal_planets: Dict,
    natal_houses: Dict,
    natal_ascendant: Dict,
    natal_midheaven: Dict,
    natal_aspects: List[Dict],
    transit_planets: Dict,
    show_aspects: bool = True,
    show_houses: bool = True,
    show_transit_aspects: bool = True,
    size: tuple = (14, 14)
) -> plt.Figure:
    """Natal chart with transit overlay. Natal: INNER, Transits: OUTER"""
    
    fig, ax = plt.subplots(figsize=size, facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    outer_radius = 1.0
    natal_radius = 0.5
    transit_radius = 0.75
    
    sign_glyphs = {'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
                   'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
                   'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'}
    
    # Draw signs
    for i, sign in enumerate(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']):
        start_angle = 90 - i * 30
        wedge = mpatches.Wedge((0, 0), outer_radius, start_angle - 30, start_angle,
                               width=outer_radius - transit_radius,
                               facecolor=SIGN_COLORS.get(sign, '#333'),
                               edgecolor='#2d2d44', linewidth=1)
        ax.add_patch(wedge)
        
        angle_rad = np.radians(start_angle - 15)
        glyph_x = (outer_radius - 0.03) * np.cos(angle_rad)
        glyph_y = (outer_radius - 0.03) * np.sin(angle_rad)
        ax.text(glyph_x, glyph_y, sign_glyphs.get(sign, ''), 
                ha='center', va='center', fontsize=7, color='#fff', fontweight='bold')
    
    # House cusps
    if show_houses and natal_houses:
        for house_num in range(1, 13):
            if house_num in natal_houses:
                cusp = natal_houses[house_num]
                long = cusp['longitude']
                x1, y1 = degree_to_chart_coords(long, natal_radius - 0.08)
                x2, y2 = degree_to_chart_coords(long, natal_radius)
                ax.plot([x1, x2], [y1, y2], color='#4a4a6a', linewidth=0.8, alpha=0.5)
    
    # Circles
    circle1 = plt.Circle((0, 0), natal_radius, fill=False, color='#666', linewidth=1.5)
    ax.add_patch(circle1)
    circle2 = plt.Circle((0, 0), transit_radius, fill=False, color='#888', linewidth=1, linestyle='--')
    ax.add_patch(circle2)
    
    # Natal planets
    for planet, data in natal_planets.items():
        long = data['longitude']
        x, y = degree_to_chart_coords(long, natal_radius)
        
        color = PLANET_COLORS.get(planet, '#888')
        circle = plt.Circle((x, y), 0.035, color=color, ec='#fff', linewidth=1, zorder=3)
        ax.add_patch(circle)
        
        glyph = PLANET_GLYPHS.get(planet, '●')
        ax.text(x, y, glyph, ha='center', va='center', fontsize=8, color='#000', fontweight='bold', zorder=4)
    
    # Transit planets
    transit_planet_list = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 
                          'Saturn', 'Uranus', 'Neptune', 'Pluto']
    for planet in transit_planet_list:
        if planet in transit_planets:
            data = transit_planets[planet]
            long = data['longitude']
            x, y = degree_to_chart_coords(long, transit_radius)
            
            color = PLANET_COLORS.get(planet, '#888')
            circle = plt.Circle((x, y), 0.05, color=color, ec='#FFD700', linewidth=2, zorder=3)
            ax.add_patch(circle)
            
            glyph = PLANET_GLYPHS.get(planet, '●')
            ax.text(x, y, glyph, ha='center', va='center', fontsize=10, color='#000', fontweight='bold', zorder=4)
            
            name_x, name_y = degree_to_chart_coords(long, transit_radius + 0.06)
            ax.text(name_x, name_y, planet, ha='center', va='center', fontsize=7, 
                    color='#FFD700', fontweight='bold', zorder=2)
    
    # Transit-Natal aspects
    if show_transit_aspects:
        planet_pos_natal = {p: degree_to_chart_coords(natal_planets[p]['longitude'], natal_radius) 
                          for p in natal_planets}
        planet_pos_transit = {p: degree_to_chart_coords(transit_planets[p]['longitude'], transit_radius) 
                            for p in transit_planets if p in transit_planets}
        
        for t_planet in transit_planet_list:
            if t_planet not in transit_planets or t_planet not in planet_pos_transit:
                continue
            for n_planet in natal_planets:
                if n_planet not in planet_pos_natal:
                    continue
                
                t_long = transit_planets[t_planet]['longitude']
                n_long = natal_planets[n_planet]['longitude']
                
                diff = abs(t_long - n_long)
                if diff > 180:
                    diff = 360 - diff
                
                # Check major aspects
                for aspect_deg, aspect_name, max_orb in [(0, 'Conjunction', 2), 
                                                          (180, 'Opposition', 2),
                                                          (90, 'Square', 2), 
                                                          (120, 'Trine', 2)]:
                    orb = abs(diff - aspect_deg)
                    if orb <= max_orb:
                        x1, y1 = planet_pos_transit[t_planet]
                        x2, y2 = planet_pos_natal[n_planet]
                        
                        colors = {'Conjunction': '#FF00FF', 'Opposition': '#FF6B6B',
                                 'Square': '#FF4500', 'Trine': '#4ECDC4'}
                        ax.plot([x1, x2], [y1, y2], color=colors.get(aspect_name, '#888'), 
                               linewidth=1.5, linestyle='--', alpha=0.7, zorder=1)
    
    # Labels
    if natal_ascendant:
        ax.annotate('ASC', xy=degree_to_chart_coords(natal_ascendant['longitude'], natal_radius - 0.12),
                   fontsize=7, color='#00FF00', fontweight='bold', ha='center')
    if natal_midheaven:
        ax.annotate('MC', xy=degree_to_chart_coords(natal_midheaven['longitude'], natal_radius - 0.12),
                   fontsize=7, color='#FFD700', fontweight='bold', ha='center')
    
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Transit Overlay Chart\n(Natal: Inner | Transits: Outer)', 
                 fontsize=12, color='#fff', pad=20, fontweight='bold')
    
    plt.tight_layout()
    return fig


# ============== Synastry Chart ==============

def calculate_synastry_aspects(person1_planets: Dict, person2_planets: Dict) -> List[Dict]:
    """Calculate synastry aspects between two people's planets"""
    aspects = []
    
    planets1 = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    
    for p1 in planets1:
        if p1 not in person1_planets:
            continue
        for p2 in planets1:
            if p2 not in person2_planets:
                continue
            
            long1 = person1_planets[p1]['longitude']
            long2 = person2_planets[p2]['longitude']
            
            diff = abs(long1 - long2)
            if diff > 180:
                diff = 360 - diff
            
            for aspect_deg, aspect_name, max_orb in [(0, "Conjunction", 8),
                                                      (60, "Sextile", 6),
                                                      (90, "Square", 8),
                                                      (120, "Trine", 8),
                                                      (180, "Opposition", 8)]:
                orb = abs(diff - aspect_deg)
                if orb <= max_orb:
                    aspects.append({
                        'p1': p1,
                        'p2': p2,
                        'type': aspect_name,
                        'orb': orb,
                        'exact': orb < 1.0
                    })
    
    aspects.sort(key=lambda x: x['orb'])
    return aspects


def create_synastry_chart(
    person1_planets: Dict,
    person1_houses: Dict,
    person1_ascendant: Dict,
    person1_midheaven: Dict,
    person2_planets: Dict,
    person2_houses: Dict,
    person2_ascendant: Dict,
    person2_midheaven: Dict,
    person1_name: str = "Person 1",
    person2_name: str = "Person 2",
    show_aspects: bool = True,
    show_houses: bool = True,
    size: tuple = (14, 14)
) -> plt.Figure:
    """Synastry chart. Person 1: INNER, Person 2: OUTER"""
    
    synastry_aspects = calculate_synastry_aspects(person1_planets, person2_planets)
    
    fig, ax = plt.subplots(figsize=size, facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    outer_radius = 1.0
    person1_radius = 0.45
    person2_radius = 0.72
    
    sign_glyphs = {'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
                   'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
                   'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'}
    
    # Draw signs
    for i, sign in enumerate(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']):
        start_angle = 90 - i * 30
        wedge = mpatches.Wedge((0, 0), outer_radius, start_angle - 30, start_angle,
                               width=outer_radius - person2_radius,
                               facecolor=SIGN_COLORS.get(sign, '#333'),
                               edgecolor='#2d2d44', linewidth=1)
        ax.add_patch(wedge)
        
        angle_rad = np.radians(start_angle - 15)
        glyph_x = (outer_radius - 0.03) * np.cos(angle_rad)
        glyph_y = (outer_radius - 0.03) * np.sin(angle_rad)
        ax.text(glyph_x, glyph_y, sign_glyphs.get(sign, ''), 
                ha='center', va='center', fontsize=7, color='#fff', fontweight='bold')
    
    # Circles
    circle1 = plt.Circle((0, 0), person1_radius, fill=False, color='#4169E1', linewidth=2)
    ax.add_patch(circle1)
    circle2 = plt.Circle((0, 0), person2_radius, fill=False, color='#FF69B4', linewidth=2)
    ax.add_patch(circle2)
    
    # House cusps
    if show_houses and person1_houses:
        for house_num in range(1, 13):
            if house_num in person1_houses:
                cusp = person1_houses[house_num]
                long = cusp['longitude']
                x1, y1 = degree_to_chart_coords(long, person1_radius - 0.05)
                x2, y2 = degree_to_chart_coords(long, person1_radius)
                ax.plot([x1, x2], [y1, y2], color='#4169E1', linewidth=0.8, alpha=0.5)
    
    # Person 1 planets (inner)
    for planet, data in person1_planets.items():
        long = data['longitude']
        x, y = degree_to_chart_coords(long, person1_radius)
        
        color = PLANET_COLORS.get(planet, '#888')
        circle = plt.Circle((x, y), 0.03, color=color, ec='#4169E1', linewidth=1, zorder=3)
        ax.add_patch(circle)
        
        glyph = PLANET_GLYPHS.get(planet, '●')
        ax.text(x, y, glyph, ha='center', va='center', fontsize=7, color='#000', fontweight='bold', zorder=4)
    
    # Person 2 planets (outer)
    for planet, data in person2_planets.items():
        long = data['longitude']
        x, y = degree_to_chart_coords(long, person2_radius)
        
        color = PLANET_COLORS.get(planet, '#888')
        circle = plt.Circle((x, y), 0.04, color=color, ec='#FF69B4', linewidth=1.5, zorder=3)
        ax.add_patch(circle)
        
        glyph = PLANET_GLYPHS.get(planet, '●')
        ax.text(x, y, glyph, ha='center', va='center', fontsize=9, color='#000', fontweight='bold', zorder=4)
        
        name_x, name_y = degree_to_chart_coords(long, person2_radius + 0.05)
        ax.text(name_x, name_y, f"{planet}2", ha='center', va='center', fontsize=6, 
                color='#FF69B4', fontweight='bold', zorder=2)
    
    # Synastry aspects
    if show_aspects:
        planet_pos_p1 = {p: degree_to_chart_coords(person1_planets[p]['longitude'], person1_radius) 
                        for p in person1_planets}
        planet_pos_p2 = {p: degree_to_chart_coords(person2_planets[p]['longitude'], person2_radius) 
                        for p in person2_planets}
        
        aspect_emojis = {'Conjunction': 'C', 'Opposition': 'O', 'Square': 'X',
                        'Trine': 'T', 'Sextile': 'S'}
        
        for asp in synastry_aspects[:12]:
            p1, p2 = asp['p1'], asp['p2']
            if p1 in planet_pos_p1 and p2 in planet_pos_p2:
                x1, y1 = planet_pos_p1[p1]
                x2, y2 = planet_pos_p2[p2]
                
                config = ASPECT_CONFIG.get(asp['type'], {'color': '#888', 'width': 1})
                ax.plot([x1, x2], [y1, y2], color=config['color'], 
                       linewidth=config['width'] + 0.5, linestyle='-', alpha=0.8, zorder=2)
                
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                emoji = aspect_emojis.get(asp['type'], '●')
                ax.text(mid_x, mid_y, emoji, ha='center', va='center', 
                       fontsize=10, color=config['color'], fontweight='bold', zorder=5)
    
    # Labels
    if person1_ascendant:
        ax.annotate('ASC1', xy=degree_to_chart_coords(person1_ascendant['longitude'], person1_radius - 0.1),
                   fontsize=6, color='#4169E1', fontweight='bold', ha='center')
    if person2_ascendant:
        ax.annotate('ASC2', xy=degree_to_chart_coords(person2_ascendant['longitude'], person2_radius + 0.08),
                   fontsize=6, color='#FF69B4', fontweight='bold', ha='center')
    
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    ax.axis('off')
    
    ax.text(0, -1.15, f"🔵 {person1_name} (Inner)  |  🔴 {person2_name} (Outer)", 
            ha='center', va='center', fontsize=10, color='#ccc')
    
    ax.set_title(f'Synastry Chart: {person1_name} & {person2_name}', 
                 fontsize=12, color='#fff', pad=20, fontweight='bold')
    
    plt.tight_layout()
    return fig
